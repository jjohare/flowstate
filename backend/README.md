# Tai Chi Flow Backend

Python backend for the Tai Chi motion capture and training application.

## Features

- Real-time pose detection using MediaPipe
- Video processing and analysis
- Motion quality assessment
- Tai Chi form comparison
- RESTful API for Electron frontend

## Architecture

- **app.py** - Flask API server
- **video_processor.py** - Video and frame processing with MediaPipe
- **pose_analyzer.py** - Tai Chi movement analysis and scoring
- **model_manager.py** - AI model management and initialization
- **utils.py** - Utility functions

## Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Installation

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Run the setup script:
   ```bash
   python setup.py
   ```

   This will:
   - Create a virtual environment
   - Install all dependencies
   - Set up required directories
   - Test the installation

### Manual Installation

If you prefer manual setup:

1. Create virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Backend

### Development Mode

```bash
# Activate virtual environment first
python app.py
```

The server will start on `http://127.0.0.1:5000`

### Testing

Run the test script to verify functionality:

```bash
python test_backend.py
```

## API Endpoints

### Health & Status

- `GET /health` - Health check
- `GET /models/status` - Get AI model status
- `POST /models/load` - Load/download AI models

### Video Processing

- `POST /video/upload` - Upload video file
- `POST /video/process/<video_id>` - Process uploaded video
- `GET /video/status/<video_id>` - Get processing status
- `GET /video/results/<video_id>` - Get analysis results
- `POST /video/stream` - Process real-time frame

### Training & Analysis

- `GET /training/forms` - Get available Tai Chi forms
- `POST /analysis/compare` - Compare movements with reference

## Configuration

Environment variables:
- `FLASK_ENV` - Set to 'development' for debug mode
- `CUDA_VISIBLE_DEVICES` - GPU selection for TensorFlow
- `TF_CPP_MIN_LOG_LEVEL` - TensorFlow logging level

## Models

The backend uses:
- **MediaPipe Pose** - Automatic download on first use
- **Custom models** - Place in `models/` directory

## Development

### Adding New Endpoints

1. Add route handler in `app.py`
2. Implement processing logic in appropriate module
3. Update IPC handlers in Electron
4. Add to API documentation

### Debugging

Enable debug mode:
```bash
export FLASK_ENV=development  # macOS/Linux
set FLASK_ENV=development     # Windows
python app.py
```

View logs in `logs/` directory.

## Performance Optimization

- Use GPU acceleration when available
- Batch process frames for efficiency
- Cache model predictions
- Implement frame skipping for real-time processing

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Activate virtual environment
2. **Port already in use**: Change port in app.py or kill existing process
3. **Model download fails**: Check internet connection
4. **Low FPS**: Reduce model complexity or enable GPU

### Logs

Check `logs/` directory for detailed error messages.

## License

Part of the Tai Chi Flow application.