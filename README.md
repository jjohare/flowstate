# Tai Chi Flow - Motion Capture & Training Application

An advanced Electron-based desktop application for Tai Chi motion capture, analysis, and flow state training using computer vision and machine learning. The application provides real-time pose detection, movement analysis, and personalized feedback to help practitioners improve their Tai Chi form and achieve deeper flow states.

## Features

- **Real-time Motion Capture**: Advanced pose detection from video files or live camera feed
- **Flow State Analysis**: Sophisticated metrics for movement quality, balance, and flow state detection
- **Training Programs**: Multiple Tai Chi forms (Yang 24, Yang 40, Chen 18) with guided practice
- **3D Visualization**: Interactive 3D skeleton rendering with movement trajectories
- **Performance Analytics**: Detailed movement analysis with form accuracy scoring
- **Progress Tracking**: Historical data visualization and improvement metrics
- **Video Export**: Save analyzed videos with pose overlays and feedback

## Tech Stack

### Frontend
- **Framework**: React 18 with TypeScript
- **UI Library**: Material-UI v5 with custom theming
- **3D Graphics**: Three.js with React Three Fiber
- **State Management**: Zustand for global state
- **Animation**: Framer Motion for smooth transitions
- **Charts**: Chart.js with React-Chart.js-2

### Desktop
- **Platform**: Electron 27 with IPC communication
- **Build Tool**: Electron Builder for cross-platform packaging
- **Auto-Update**: Built-in update mechanism

### Backend
- **API Server**: Python Flask with CORS support
- **ML Framework**: TensorFlow/MediaPipe for pose detection
- **Video Processing**: OpenCV for frame manipulation
- **Async Processing**: Threading for non-blocking video analysis

### Machine Learning
- **Pose Detection**: MediaPipe Holistic model
- **Motion Analysis**: Custom algorithms for Tai Chi form evaluation
- **Flow State Detection**: Pattern recognition for movement quality

## System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.15+, Ubuntu 20.04+
- **Processor**: Intel i5 or AMD Ryzen 5
- **Memory**: 8GB RAM
- **Storage**: 2GB available space
- **Graphics**: OpenGL 3.3 support

### Recommended Requirements
- **Processor**: Intel i7 or AMD Ryzen 7
- **Memory**: 16GB RAM
- **Graphics**: NVIDIA GPU with CUDA support for faster processing
- **Camera**: 1080p webcam for live capture

## Installation & Setup

### Quick Start (Using Scripts)

#### Windows
```batch
# Run the start script
start.bat
```

#### macOS/Linux
```bash
# Make script executable (first time only)
chmod +x start.sh

# Run the start script
./start.sh
```

### Manual Setup

1. **Clone the repository**:
```bash
git clone <repository-url>
cd flowstate
```

2. **Install Node.js dependencies**:
```bash
npm install
```

3. **Set up Python backend**:
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
cd ..
```

4. **Create required directories**:
```bash
mkdir -p models
```

## Running the Application

### Development Mode

#### Option 1: All-in-One Command
```bash
npm run dev
```
This starts both the backend server and the Electron app with hot-reload enabled.

#### Option 2: Individual Components
```bash
# Terminal 1: Start backend
cd backend
python app.py

# Terminal 2: Start frontend
npm run dev:react

# Terminal 3: Start Electron (after frontend is running)
npm run dev:electron
```

### Production Mode
```bash
# Build the application
npm run build

# Create distribution package
npm run dist

# Platform-specific builds
npm run dist:win    # Windows
npm run dist:mac    # macOS
npm run dist:linux  # Linux
```

## Project Structure

```
flowstate/
├── backend/              # Python Flask API server
│   ├── app.py           # Main API endpoints
│   ├── video_processor.py # Video analysis logic
│   ├── pose_analyzer.py  # Tai Chi form analysis
│   ├── model_manager.py  # ML model management
│   └── requirements.txt  # Python dependencies
├── electron/            # Electron main process
│   ├── main.js         # Main process entry
│   └── preload.js      # Preload script for IPC
├── src/                # React application
│   ├── components/     # UI components
│   │   ├── Dashboard.tsx
│   │   ├── VideoCapture.tsx
│   │   ├── FlowAnalysis.tsx
│   │   ├── Training.tsx
│   │   └── Settings.tsx
│   ├── store/          # Zustand state management
│   ├── types/          # TypeScript definitions
│   └── utils/          # Utility functions
├── models/             # ML models (auto-downloaded)
├── public/             # Static assets
├── electron-builder.yml # Build configuration
├── package.json        # Node.js dependencies
├── start.sh           # Unix startup script
└── start.bat          # Windows startup script
```

## API Endpoints

The backend server provides the following endpoints:

- `GET /health` - Health check
- `GET /models/status` - Check ML model status
- `POST /models/load` - Load ML models
- `POST /video/upload` - Upload video for processing
- `POST /video/process/:id` - Start video processing
- `GET /video/status/:id` - Check processing status
- `GET /video/results/:id` - Get analysis results
- `POST /video/stream` - Process live video frames
- `GET /training/forms` - Get available Tai Chi forms
- `POST /analysis/compare` - Compare movements with reference

## Configuration

### Environment Variables
Create a `.env` file in the root directory:
```env
REACT_APP_API_URL=http://localhost:5000
ELECTRON_IS_DEV=1
```

### Backend Configuration
Edit `backend/config.py` for advanced settings:
```python
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'webm', 'mkv'}
MODEL_CONFIDENCE_THRESHOLD = 0.5
```

## Troubleshooting

### Common Issues

1. **Backend not starting**
   - Ensure Python 3.8+ is installed
   - Check if port 5000 is available
   - Verify all Python dependencies are installed

2. **Video processing fails**
   - Check video format is supported
   - Ensure sufficient disk space
   - Verify ML models are downloaded

3. **Electron app won't start**
   - Run `npm run clean:install` to reset dependencies
   - Check Node.js version (18+ required)
   - Ensure backend is running first

### Debug Mode
Enable debug logging:
```bash
# Windows
set DEBUG=electron:*
npm run dev

# macOS/Linux
DEBUG=electron:* npm run dev
```

## Building for Distribution

### Code Signing (macOS)
```bash
# Set your Apple Developer ID
export CSC_NAME="Developer ID Application: Your Name"
npm run dist:mac
```

### Windows Installer
The NSIS installer includes:
- Start menu shortcuts
- Desktop shortcut (optional)
- Uninstaller
- Auto-update support

### Linux Packages
Builds available formats:
- AppImage (universal)
- .deb (Debian/Ubuntu)
- .rpm (Fedora/RHEL)

## Contributing

We welcome contributions! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow TypeScript best practices
- Maintain test coverage above 80%
- Use ESLint and Prettier for code formatting
- Document new features in the README

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- MediaPipe team for the pose detection models
- Electron community for the excellent framework
- Material-UI team for the beautiful components
- All contributors and testers

## Support

For issues and feature requests, please use the GitHub issues page.

For general questions, join our Discord community: [Discord Link]

---

Built with ❤️ by the Flow State team

## Project Structure

```
flowstate/
├── electron/          # Electron main process
├── src/              # React application source
│   ├── components/   # React components
│   ├── store/        # Zustand state management
│   ├── types/        # TypeScript type definitions
│   └── utils/        # Utility functions
├── backend/          # Python ML backend (optional)
├── public/           # Static assets
└── package.json      # Project configuration
```

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

## License

This project is licensed under the MIT License.