from app.celery import celery_app
import os
import torch
from .models import JourneyModel, train_model, version_model

TRAINING_THRESHOLD = 10

@celery_app.task
def train_new_model():
    print("Starting model training...")
    model = JourneyModel()
    train_model(model)
    version_model(model)
    print("Model training completed and versioned.")
    
    # Clear training data
    training_data_dir = "data/training_data"
    for file in os.listdir(training_data_dir):
        os.remove(os.path.join(training_data_dir, file))

def add_to_training_queue(video_path, comments):
    training_data_dir = os.path.join("data", "training_data")
    os.makedirs(training_data_dir, exist_ok=True)
    
    # Save video path and comments
    with open(os.path.join(training_data_dir, f"{os.path.basename(video_path)}.txt"), 'w') as f:
        f.write(comments)
    
    # Check if ready to train
    count = len(os.listdir(training_data_dir))
    if count >= TRAINING_THRESHOLD:
        train_new_model.delay()