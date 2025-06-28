import cv2
import os
from fpdf import FPDF

def extract_key_frames(video_path, interval_sec=5):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval_sec)
    frames = []
    count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count % frame_interval == 0:
            frames.append(frame)
        count += 1
    
    cap.release()
    return frames

def get_video_duration(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return frame_count / fps

def aggregate_predictions(predictions):
    object_counts = {}
    for pred in predictions:
        for obj in pred.get('objects', []):
            obj_class = obj['class']
            object_counts[obj_class] = object_counts.get(obj_class, 0) + 1
    return object_counts

def detect_events(predictions):
    events = []
    prev_objects = set()
    
    for i, pred in enumerate(predictions):
        current_objects = set([obj['class'] for obj in pred.get('objects', [])])
        new_objects = current_objects - prev_objects
        if new_objects:
            events.append({
                'frame': i,
                'event': f"New objects: {', '.join(new_objects)}"
            })
        prev_objects = current_objects
    
    return events

def generate_summary(analysis, comments, base_path):
    # TXT Export
    txt_path = f"{base_path}.txt"
    with open(txt_path, 'w') as f:
        f.write(f"Journey Summary\n")
        f.write(f"Duration: {analysis['duration']:.2f} seconds\n")
        f.write("Objects Detected:\n")
        for obj, count in analysis['objects'].items():
            f.write(f"- {obj}: {count}\n")
        f.write("Key Events:\n")
        for event in analysis['key_events']:
            f.write(f"Frame {event['frame']}: {event['event']}\n")
        f.write(f"\nUser Comments:\n{comments}")
    
    # PDF Export
    pdf_path = f"{base_path}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Journey Summary", ln=True)
    pdf.cell(200, 10, txt=f"Duration: {analysis['duration']:.2f} seconds", ln=True)
    pdf.cell(200, 10, txt="Objects Detected:", ln=True)
    for obj, count in analysis['objects'].items():
        pdf.cell(200, 10, txt=f"- {obj}: {count}", ln=True)
    pdf.cell(200, 10, txt="Key Events:", ln=True)
    for event in analysis['key_events']:
        pdf.cell(200, 10, txt=f"Frame {event['frame']}: {event['event']}", ln=True)
    pdf.multi_cell(0, 10, txt=f"User Comments:\n{comments}")
    pdf.output(pdf_path)