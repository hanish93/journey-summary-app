import cv2
import os
from celery import Celery
from .utils import extract_key_frames, get_video_duration, aggregate_predictions, detect_events
from .models import load_model, predict_frame

celery = Celery('video_processor', broker='redis://redis:6379/0')

@celery.task
def process_video(video_path, comments):
    # Extract key frames
    frames = extract_key_frames(video_path)
    
    # Load current model
    model = load_model()
    
    # Process frames
    predictions = []
    for frame in frames:
        pred = predict_frame(model, frame)
        predictions.append(pred)
    
    # Generate analysis
    duration = get_video_duration(video_path)
    objects = aggregate_predictions(predictions)
    events = detect_events(predictions)
    
    analysis = {
        'duration': duration,
        'objects': objects,
        'key_events': events
    }
    
    # Create export
    export_dir = "exports"
    os.makedirs(export_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    generate_summary(analysis, comments, os.path.join(export_dir, base_name))