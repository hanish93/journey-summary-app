from app.celery import celery_app
import torch
import numpy as np
from .utils import adaptive_frame_sampling, preprocess_frame, post_process, generate_enhanced_summary
from .models import load_model

@celery_app.task
def process_video(video_path, comments):
    # Import OpenCV inside the task to avoid initialization conflicts
    import cv2
    
    # Adaptive frame sampling based on motion
    frames = adaptive_frame_sampling(video_path)
    
    # Preprocess frames
    frame_tensors = [preprocess_frame(frame) for frame in frames]
    
    # Load model with mixed precision
    model = load_model().half().to('cuda')
    
    # Batch processing
    batch_size = 16
    predictions = []
    for i in range(0, len(frame_tensors), batch_size):
        batch = torch.stack(frame_tensors[i:i+batch_size]).half().to('cuda')
        with torch.no_grad(), torch.cuda.amp.autocast():
            preds = model(batch)
            predictions.append(preds)
    
    # Post-process predictions
    analysis = post_process(predictions, video_path)
    
    # Generate summary
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    generate_enhanced_summary(analysis, comments, os.path.join("exports", base_name))
    
    # Cleanup
    if os.path.exists(video_path):
        os.remove(video_path)