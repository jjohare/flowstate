# Tai Chi Flow - Project Overview

## 🎯 Project Vision

Tai Chi Flow is an innovative desktop application that transforms traditional Tai Chi practice through modern technology. By combining video analysis, 3D visualization, and flow state detection, it provides practitioners with unprecedented insights into their form and movement quality.

## 🔑 Key Features

### 1. Video-to-3D Conversion
- Upload or record Tai Chi practice videos
- Automatic pose detection using advanced ML models
- Real-time conversion to 3D stick figure animations
- Frame-by-frame movement analysis

### 2. Interactive 3D Visualization
- 360° rotatable view of movements
- Synchronized playback with original video
- Multiple viewing angles and perspectives
- Mirror mode for self-correction

### 3. Flow State Analysis
- Movement smoothness metrics
- Rhythm and timing analysis
- Balance and stability indicators
- Progress tracking over time

### 4. Training Tools
- Side-by-side comparison with masters
- Slow-motion playback
- Key frame highlighting
- Practice session recording

## 🏗️ Technical Architecture

### Three-Layer Architecture

```
┌─────────────────────────────────────────────┐
│          Desktop Application              │
│              (Electron)                   │
├─────────────────────────────────────────────┤
│         Frontend Interface                │
│     (React + TypeScript + Three.js)       │
├─────────────────────────────────────────────┤
│         Backend Processing                │
│      (Python + Flask + MediaPipe)         │
└─────────────────────────────────────────────┘
```

### Technology Stack

#### Frontend
- **React 19.1.0** - Modern UI framework
- **TypeScript** - Type-safe development
- **Three.js** - 3D graphics rendering
- **@react-three/fiber** - React Three.js integration
- **Zustand** - State management

#### Backend
- **Python 3.8+** - Core processing language
- **Flask** - RESTful API server
- **MediaPipe** - Pose detection ML models
- **OpenCV** - Video processing
- **NumPy** - Numerical computations

#### Desktop
- **Electron 36.5.0** - Cross-platform desktop framework
- **Node.js** - JavaScript runtime
- **electron-builder** - Application packaging

## 📊 Data Flow

```
Video Input → Frame Extraction → Pose Detection → 
3D Coordinates → Animation Data → 3D Visualization
```

### Pose Data Structure

```typescript
interface AnimationFrame {
  timestamp: number;
  landmarks: PoseLandmark[];
  leftHandLandmarks?: HandLandmark[];
  rightHandLandmarks?: HandLandmark[];
}

interface PoseLandmark {
  x: number;  // Normalized 0-1
  y: number;  // Normalized 0-1
  z: number;  // Relative depth
  visibility: number;  // Confidence 0-1
}
```

## 🚀 Getting Started

### Prerequisites
- Node.js 16+
- Python 3.8+
- Git

### Quick Setup

```bash
# Clone repository
git clone <repository-url>
cd flowstate

# Install dependencies
npm install
cd backend && pip install -r requirements.txt
cd ..

# Run development mode
npm run dev
```

## 📁 Project Structure

```
flowstate/
├── src/                    # React frontend source
├── electron/               # Electron main process
├── backend/                # Python backend
├── docs/                   # Documentation
├── models/                 # ML models
├── public/                 # Static assets
└── build/                  # Build output
```

## 🎓 Use Cases

1. **Personal Practice**
   - Self-assessment and improvement
   - Progress tracking
   - Form correction

2. **Teaching**
   - Student movement analysis
   - Visual feedback for corrections
   - Demonstration recording

3. **Research**
   - Movement pattern analysis
   - Biomechanics study
   - Style comparison

## 🔮 Future Enhancements

- Real-time pose detection from webcam
- Multi-person tracking
- AI-powered form suggestions
- Cloud synchronization
- Mobile companion app
- VR/AR integration

## 📚 Documentation

For detailed documentation, see:
- [Architecture Guide](./architecture/README.md)
- [Development Guides](./development/)
- [API Reference](./api/README.md)
- [User Manual](./guides/usage.md)