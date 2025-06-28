import cv2
import numpy as np
import torch
from .utils import adaptive_frame_sampling

def process_video(video_path, comments):
    # Adaptive frame sampling based on motion
    frames = adaptive_frame_sampling(video_path)
    
    # Preprocess frames
    frames = [preprocess_frame(frame) for frame in frames]
    
    # Load model with mixed precision
    model = load_model().half().to('cuda')
    
    # Batch processing
    batch_size = 16
    predictions = []
    for i in range(0, len(frames), batch_size):
        batch = torch.stack(frames[i:i+batch_size]).half().to('cuda')
        with torch.no_grad(), torch.cuda.amp.autocast():
            preds = model(batch)
            predictions.append(preds)
    
    # Post-process predictions
    analysis = post_process(predictions, video_path)
    
    # Generate summary
    generate_enhanced_summary(analysis, comments)