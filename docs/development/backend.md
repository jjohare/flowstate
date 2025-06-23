# Backend Development Guide

## Overview

The Tai Chi Flow backend is a Python-based service that handles video processing, pose detection, and motion analysis.

## Architecture

### Core Components

1. **app.py** - Flask application server
   - RESTful API endpoints
   - WebSocket support for real-time data
   - CORS configuration for Electron frontend

2. **video_processor.py** - Video processing pipeline
   - Frame extraction
   - Pose detection using MediaPipe
   - Motion data extraction

3. **pose_analyzer.py** - Pose analysis engine
   - Landmark detection
   - Skeletal tracking
   - Movement pattern analysis

4. **model_manager.py** - ML model management
   - Model loading and caching
   - Inference optimization
   - Model versioning

## Setup

### Requirements

```bash
python >= 3.8
pip install -r backend/requirements.txt
```

### Environment Variables

```bash
FLASK_ENV=development
FLASK_PORT=5000
MODEL_PATH=./models
```

## API Endpoints

### POST /api/process-video
Process uploaded video for pose detection

**Request:**
```json
{
  "video": "<base64_encoded_video>",
  "options": {
    "fps": 30,
    "quality": "high"
  }
}
```

**Response:**
```json
{
  "frames": [
    {
      "timestamp": 0.033,
      "landmarks": [...],
      "confidence": 0.95
    }
  ]
}
```

### GET /api/health
Health check endpoint

### WebSocket /ws/stream
Real-time pose data streaming

## Development

### Running Tests

```bash
cd backend
python test_backend.py
```

### Debugging

Enable debug mode:
```python
app.run(debug=True)
```

## Performance Optimization

1. **Batch Processing** - Process multiple frames simultaneously
2. **Model Caching** - Keep models in memory
3. **GPU Acceleration** - Use CUDA when available
4. **Frame Skipping** - Configurable frame rate reduction

## Error Handling

- Graceful video format handling
- Pose detection confidence thresholds
- Memory management for large videos
- Proper error responses with status codes