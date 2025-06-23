# Frontend Development Guide

## Overview

The Tai Chi Flow frontend is built with React, TypeScript, and Three.js for 3D visualization.

## Architecture

### Component Structure

```
src/
├── App.tsx                 # Main application component
├── components/
│   ├── Dashboard.tsx       # Main dashboard view
│   ├── VideoCapture.tsx    # Video recording interface
│   ├── FlowAnalysis.tsx    # Flow state analysis
│   ├── Training.tsx        # Training mode interface
│   ├── Settings.tsx        # Application settings
│   └── Layout.tsx          # Layout wrapper
├── hooks/                  # Custom React hooks
├── store/                  # State management
│   └── appStore.ts        # Zustand store
├── types/                  # TypeScript definitions
└── utils/                  # Utility functions
```

## Key Technologies

### React 19.1.0
- Function components with hooks
- Concurrent features
- Automatic batching

### TypeScript
- Strict type checking
- Interface definitions for all data models
- Type-safe props and state

### Three.js Integration
- @react-three/fiber for React integration
- @react-three/drei for helpers
- Custom shaders for effects

## 3D Visualization

### Stick Figure Rendering

```typescript
interface PoseLandmark {
  x: number;
  y: number;
  z: number;
  visibility: number;
}

interface SkeletonConnection {
  start: number;
  end: number;
  color?: string;
}
```

### Camera Controls
- OrbitControls for navigation
- Preset viewing angles
- Smooth transitions

### Animation System
- Frame interpolation
- Variable playback speed
- Timeline scrubbing

## State Management

### Zustand Store

```typescript
interface AppState {
  // Video state
  currentVideo: VideoData | null;
  isProcessing: boolean;
  
  // Playback state
  isPlaying: boolean;
  currentFrame: number;
  playbackSpeed: number;
  
  // UI state
  showGrid: boolean;
  mirrorMode: boolean;
  
  // Actions
  setVideo: (video: VideoData) => void;
  play: () => void;
  pause: () => void;
  setFrame: (frame: number) => void;
}
```

## Development

### Running Development Server

```bash
npm run dev:react
```

### Building for Production

```bash
npm run build:react
```

### Code Style

- ESLint configuration
- Prettier formatting
- TypeScript strict mode

## Performance Optimization

### React Optimization
- Memoization with useMemo/useCallback
- Virtual list for large datasets
- Code splitting with lazy loading

### Three.js Optimization
- Instanced rendering for multiple figures
- LOD (Level of Detail) system
- Efficient geometry reuse
- Texture atlasing

## Testing

### Unit Tests
```bash
npm test
```

### Integration Tests
- Component testing with React Testing Library
- Three.js scene testing
- Store action testing

## Debugging

### React DevTools
- Component inspection
- Performance profiling
- State debugging

### Three.js Inspector
- Scene graph visualization
- Performance metrics
- Draw call analysis