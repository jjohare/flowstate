# Tai Chi Motion Capture Application

An Electron-based 3D visualization application for rendering Tai Chi forms derived from video analysis. This application transforms motion capture data into interactive 3D stick figure animations.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Technology Stack](#technology-stack)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

The Tai Chi Motion Capture Application is a desktop application built with Electron that visualizes human pose data extracted from video recordings. It renders 3D stick figures representing Tai Chi practitioners' movements, allowing for detailed analysis and study of form and technique.

### Key Components

- **Electron Desktop App**: Cross-platform desktop application
- **React Frontend**: Modern UI with responsive controls
- **Three.js 3D Rendering**: Real-time 3D visualization
- **Motion Data Processing**: Interprets pose landmarks from video analysis

## ✨ Features

### 3D Visualization
- Real-time 3D stick figure rendering
- Smooth animation playback with variable speed control
- Interactive camera controls (pan, zoom, rotate)
- Mirror mode for practice and instruction

### Playback Controls
- Play/pause functionality
- Frame-by-frame navigation
- Adjustable playback speed (0.1x to 2.0x)
- Timeline scrubbing
- Reset to beginning

### Data Support
- JSON-based animation data format
- Support for 33 pose landmarks
- Hand tracking with 21 landmarks per hand
- Skeletal connection mapping
- Frame interpolation for smooth playback

### User Interface
- Dark theme optimized for focus
- Responsive control panel
- Real-time frame and timing information
- Grid reference for spatial awareness

## 🏗️ Architecture

The application follows a modular architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│                    Electron Main Process                 │
│  - Window Management                                     │
│  - File System Access                                    │
│  - IPC Communication                                     │
└────────────────────────┬────────────────────────────────┘
                         │
                         │ IPC
                         │
┌────────────────────────┴────────────────────────────────┐
│                   Renderer Process                       │
│  ┌─────────────────────────────────────────────────┐   │
│  │                  React Application                │   │
│  │  ┌───────────┐  ┌─────────────┐  ┌───────────┐ │   │
│  │  │   App.tsx │  │ Components  │  │   Utils   │ │   │
│  │  └─────┬─────┘  └──────┬──────┘  └─────┬─────┘ │   │
│  │        │                │                │       │   │
│  │  ┌─────┴────────────────┴────────────────┴────┐ │   │
│  │  │          AnimationViewer Component         │ │   │
│  │  │  ┌─────────┐ ┌──────────┐ ┌─────────────┐│ │   │
│  │  │  │Three.js │ │ Controls │ │ StickFigure ││ │   │
│  │  │  │ Canvas  │ │  Panel   │ │  Renderer   ││ │   │
│  │  │  └─────────┘ └──────────┘ └─────────────┘│ │   │
│  │  └────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

For detailed architecture documentation, see [Architecture Guide](./architecture/README.md).

## 🚀 Quick Start

### Prerequisites

- Node.js 16.x or higher
- npm or yarn package manager
- Git

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd taichi-electron-app
```

2. Install dependencies:
```bash
npm install
```

3. Start development mode:
```bash
npm run dev
```

4. Build for production:
```bash
npm run build
npm run dist
```

For detailed setup instructions, see [Setup Guide](./guides/setup.md).

## 📚 Documentation

### Core Documentation

- [Architecture Overview](./architecture/README.md) - System design and components
- [API Reference](./api/README.md) - Detailed API documentation
- [Component Guide](./components/README.md) - UI component documentation
- [Data Format](./api/data-models.md) - Animation data structure

### Guides

- [Setup Guide](./guides/setup.md) - Development environment setup
- [Building Guide](./guides/building.md) - Build and packaging instructions
- [Deployment Guide](./guides/deployment.md) - Platform-specific deployment
- [Usage Guide](./guides/usage.md) - User manual
- [Troubleshooting](./guides/troubleshooting.md) - Common issues and solutions

### Diagrams

- [System Architecture](./diagrams/system-architecture.md) - High-level system design
- [Data Flow](./diagrams/data-flow.md) - Data processing pipeline
- [Component Hierarchy](./diagrams/component-hierarchy.md) - React component structure

## 🛠️ Technology Stack

### Frontend
- **React 19.1.0** - UI framework
- **TypeScript** - Type-safe development
- **Three.js 0.177.0** - 3D graphics library
- **@react-three/fiber** - React renderer for Three.js
- **@react-three/drei** - Three.js helpers and abstractions

### Desktop
- **Electron 36.5.0** - Desktop application framework
- **Node.js** - JavaScript runtime

### Build Tools
- **React Scripts** - Build configuration
- **TypeScript Compiler** - TypeScript compilation
- **Electron Builder** - Application packaging

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](./CONTRIBUTING.md) for details on:

- Code style guidelines
- Development workflow
- Testing requirements
- Pull request process

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

For more information, visit our [documentation portal](./README.md) or check out the [guides](./guides/README.md).