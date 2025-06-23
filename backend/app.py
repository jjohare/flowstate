#!/usr/bin/env python3
"""Flask API server for Tai Chi video processing and analysis."""

import os
import sys
import json
import logging
import tempfile
import time
import atexit
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import cv2
import numpy as np

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from video_processor import VideoProcessor
from model_manager import ModelManager
from pose_analyzer import PoseAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://localhost:3001"])

# Configuration
UPLOAD_FOLDER = tempfile.mkdtemp(prefix='taichi_')
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'webm', 'mkv'}
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Initialize components
model_manager = ModelManager()
video_processor = VideoProcessor(model_manager)
pose_analyzer = PoseAnalyzer()

# Global state for processing
processing_status = {}


def allowed_file(filename):
    """Check if file has allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'models_loaded': model_manager.models_loaded(),
        'upload_folder': str(Path(UPLOAD_FOLDER).exists())
    })


@app.route('/models/status', methods=['GET'])
def model_status():
    """Get status of AI models."""
    return jsonify({
        'pose_detection': model_manager.is_model_loaded('pose'),
        'motion_analysis': model_manager.is_model_loaded('motion'),
        'models': model_manager.get_model_info()
    })


@app.route('/models/load', methods=['POST'])
def load_models():
    """Load or download required AI models."""
    try:
        model_manager.load_all_models()
        return jsonify({
            'status': 'success',
            'message': 'Models loaded successfully'
        })
    except Exception as e:
        logger.error(f"Failed to load models: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/video/upload', methods=['POST'])
def upload_video():
    """Upload video for processing."""
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Initialize processing status
        video_id = os.path.splitext(filename)[0]
        processing_status[video_id] = {
            'status': 'uploaded',
            'filepath': filepath,
            'progress': 0,
            'results': None
        }

        return jsonify({
            'status': 'success',
            'video_id': video_id,
            'filename': filename
        })

    return jsonify({'error': 'Invalid file type'}), 400


@app.route('/video/process/<video_id>', methods=['POST'])
def process_video(video_id):
    """Process uploaded video for pose detection and analysis."""
    if video_id not in processing_status:
        return jsonify({'error': 'Video not found'}), 404

    try:
        filepath = processing_status[video_id]['filepath']
        processing_status[video_id]['status'] = 'processing'

        # Process video with pose detection
        results = video_processor.process_video(
            filepath,
            progress_callback=lambda p: update_progress(video_id, p)
        )

        # Analyze poses for Tai Chi form quality
        analysis = pose_analyzer.analyze_sequence(results['poses'])

        processing_status[video_id]['status'] = 'completed'
        processing_status[video_id]['results'] = {
            'poses': results['poses'],
            'analysis': analysis,
            'metrics': results['metrics']
        }

        return jsonify({
            'status': 'success',
            'video_id': video_id,
            'summary': {
                'frames_processed': results['frames_processed'],
                'poses_detected': len(results['poses']),
                'average_confidence': results['metrics']['average_confidence']
            }
        })

    except Exception as e:
        logger.error(f"Error processing video {video_id}: {e}")
        processing_status[video_id]['status'] = 'error'
        processing_status[video_id]['error'] = str(e)
        return jsonify({'error': str(e)}), 500


@app.route('/video/status/<video_id>', methods=['GET'])
def get_video_status(video_id):
    """Get processing status for a video."""
    if video_id not in processing_status:
        return jsonify({'error': 'Video not found'}), 404

    status = processing_status[video_id]
    return jsonify({
        'video_id': video_id,
        'status': status['status'],
        'progress': status.get('progress', 0),
        'error': status.get('error')
    })


@app.route('/video/results/<video_id>', methods=['GET'])
def get_video_results(video_id):
    """Get analysis results for processed video."""
    if video_id not in processing_status:
        return jsonify({'error': 'Video not found'}), 404

    status = processing_status[video_id]
    if status['status'] != 'completed':
        return jsonify({'error': 'Video processing not completed'}), 400

    return jsonify({
        'video_id': video_id,
        'results': status['results']
    })


@app.route('/video/stream', methods=['POST'])
def process_stream():
    """Process video stream frames in real-time."""
    try:
        data = request.json
        frame_data = data.get('frame')

        if not frame_data:
            return jsonify({'error': 'No frame data provided'}), 400

        # Decode base64 frame
        import base64
        frame_bytes = base64.b64decode(frame_data.split(',')[1])
        nparr = np.frombuffer(frame_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Process single frame
        pose_result = video_processor.process_frame(frame)

        # Quick analysis for real-time feedback
        if pose_result['landmarks']:
            feedback = pose_analyzer.get_realtime_feedback(pose_result['landmarks'])
        else:
            feedback = None

        return jsonify({
            'status': 'success',
            'pose': pose_result,
            'feedback': feedback
        })

    except Exception as e:
        logger.error(f"Error processing stream frame: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/training/forms', methods=['GET'])
def get_training_forms():
    """Get available Tai Chi forms for training."""
    forms = [
        {
            'id': 'yang_24',
            'name': 'Yang Style 24 Forms',
            'difficulty': 'beginner',
            'duration': '5-7 minutes',
            'movements': 24
        },
        {
            'id': 'yang_40',
            'name': 'Yang Style 40 Forms',
            'difficulty': 'intermediate',
            'duration': '10-12 minutes',
            'movements': 40
        },
        {
            'id': 'chen_18',
            'name': 'Chen Style 18 Forms',
            'difficulty': 'intermediate',
            'duration': '6-8 minutes',
            'movements': 18
        }
    ]
    return jsonify({'forms': forms})


@app.route('/analysis/compare', methods=['POST'])
def compare_movements():
    """Compare user movement with reference form."""
    try:
        data = request.json
        user_poses = data.get('user_poses')
        reference_form = data.get('reference_form')

        if not user_poses or not reference_form:
            return jsonify({'error': 'Missing required data'}), 400

        comparison = pose_analyzer.compare_with_reference(
            user_poses,
            reference_form
        )

        return jsonify({
            'status': 'success',
            'comparison': comparison
        })

    except Exception as e:
        logger.error(f"Error comparing movements: {e}")
        return jsonify({'error': str(e)}), 500


def update_progress(video_id, progress):
    """Update processing progress for a video."""
    if video_id in processing_status:
        processing_status[video_id]['progress'] = progress


def cleanup_old_files():
    """Clean up old temporary files."""
    try:
        temp_dir = Path(app.config['UPLOAD_FOLDER'])
        logger.info(f"Cleaning up temporary files in {temp_dir}")
        for file_path in temp_dir.glob('*'):
            if file_path.is_file() and file_path.stat().st_mtime < time.time() - 3600:
                logger.info(f"Removing old file: {file_path}")
                file_path.unlink()
    except Exception as e:
        logger.error(f"Error cleaning up files: {e}")


if __name__ == '__main__':
    # Register cleanup functions
    atexit.register(cleanup_old_files)
    atexit.register(lambda: video_processor.cleanup())

    # Initialize models on startup
    logger.info("Starting Tai Chi backend server...")

    try:
        model_manager.load_all_models()
        logger.info("Models loaded successfully")
    except Exception as e:
        logger.warning(f"Failed to load models on startup: {e}")

    # Run Flask app
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=os.environ.get('FLASK_ENV') == 'development'
    )