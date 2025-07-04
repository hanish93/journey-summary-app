import os
import uuid
from flask import Blueprint, jsonify, request, send_file
from .video_processor import process_video
from .utils import generate_summary
from .training import add_to_training_queue

bp = Blueprint('routes', __name__)

@bp.route('/upload', methods=['POST'])
def upload_video():
    file = request.files['video']
    comments = request.form.get('comments', '')
    
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400
    
    video_id = str(uuid.uuid4())
    video_ext = os.path.splitext(file.filename)[1]
    video_filename = f"{video_id}{video_ext}"
    video_path = os.path.join("uploads", video_filename)
    os.makedirs(os.path.dirname(video_path), exist_ok=True)
    file.save(video_path)
    
    # Start processing
    process_video.delay(video_path, comments)
    
    # Add to training dataset
    add_to_training_queue(video_path, comments)
    
    return jsonify({
        'id': video_id,
        'status': 'processing_started'
    }), 202

@bp.route('/status/<video_id>')
def processing_status(video_id):
    # Implement status checking logic
    txt_path = os.path.join("exports", f"{video_id}.txt")
    pdf_path = os.path.join("exports", f"{video_id}.pdf")
    if os.path.exists(txt_path) or os.path.exists(pdf_path):
        return jsonify({'status': 'completed'})
    return jsonify({'status': 'processing'})

@bp.route('/export/<video_id>.<format>')
def export_summary(video_id, format):
    if format not in ['txt', 'pdf']:
        return jsonify({'error': 'Invalid format'}), 400
    export_path = os.path.join("exports", f"{video_id}.{format}")
    return send_file(export_path, as_attachment=True)