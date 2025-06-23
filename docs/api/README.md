# API Reference

This document provides comprehensive API documentation for the Tai Chi Motion Capture Application, including data structures, interfaces, and communication protocols.

## Table of Contents

- [Data Models](#data-models)
- [Component APIs](#component-apis)
- [Utility Functions](#utility-functions)
- [IPC Channels](#ipc-channels)
- [Animation Loader API](#animation-loader-api)
- [Animation Processor API](#animation-processor-api)

## Data Models

### AnimationData

The core data structure representing a complete animation sequence.

```typescript
interface AnimationData {
  metadata: {
    fps: number;              // Frames per second (e.g., 30)
    total_frames: number;     // Total number of frames
    processed_size: number;   // Size of processed video (e.g., 1920)
    original_bbox: number[];  // Original bounding box [x, y, width, height]
  };
  skeleton: {
    pose_connections: number[][];     // Pairs of landmark indices for bones
    hand_connections: number[][];     // Pairs of landmark indices for hand bones
    landmark_names: {
      pose: string[];                 // Names of pose landmarks (33 total)
      hand: string[];                 // Names of hand landmarks (21 total)
    };
  };
  frames: AnimationFrame[];           // Array of animation frames
}
```

### AnimationFrame

Represents a single frame of animation data.

```typescript
interface AnimationFrame {
  frame: number;                      // Frame number (0-indexed)
  time: number;                       // Time in seconds
  landmarks: {
    pose: number[][] | null;          // 33 pose landmarks [x, y, z]
    world_pose: number[][] | null;    // World coordinates with visibility
    left_hand: HandData | null;       // Left hand tracking data
    right_hand: HandData | null;      // Right hand tracking data
  };
}
```

### HandData

Hand tracking data structure.

```typescript
interface HandData {
  landmarks: number[][];              // 21 hand landmarks [x, y, z]
  handedness: string;                 // "left" or "right"
}
```

### PlaybackState

Current playback state of the animation.

```typescript
interface PlaybackState {
  playing: boolean;                   // Is animation playing
  currentFrame: number;               // Current frame index
  playbackSpeed: number;              // Playback speed multiplier
  mirrored: boolean;                  // Is view mirrored
}
```

## Component APIs

### AnimationViewer

Main component for displaying and controlling animations.

```typescript
interface AnimationViewerProps {
  animationData: AnimationData;       // Animation data to display
}

// Component usage
<AnimationViewer animationData={data} />
```

**State Management:**
- `playing`: Controls playback state
- `currentFrame`: Current frame being displayed
- `playbackSpeed`: Speed multiplier (0.1 to 2.0)
- `mirrored`: Mirror mode toggle

**Methods:**
- `togglePlayPause()`: Toggle between play and pause
- `resetAnimation()`: Reset to frame 0
- `handleFrameChange(frame: number)`: Jump to specific frame
- `handleSpeedChange(speed: number)`: Adjust playback speed

### StickFigure

3D stick figure renderer component.

```typescript
interface StickFigureProps {
  animationData: AnimationData;       // Animation data
  currentFrame: number;               // Frame to render
  mirrored: boolean;                  // Mirror X-axis
  showJoints?: boolean;               // Show joint spheres (default: true)
  showBones?: boolean;                // Show bone connections (default: true)
  jointSize?: number;                 // Size of joint spheres (default: 0.03)
  boneWidth?: number;                 // Width of bone lines (default: 3)
}

// Component usage
<StickFigure 
  animationData={data}
  currentFrame={frame}
  mirrored={false}
  showJoints={true}
  showBones={true}
  jointSize={0.03}
  boneWidth={3}
/>
```

### PlaybackControls

Animation playback control interface.

```typescript
interface PlaybackControlsProps {
  playing: boolean;
  onPlayPause: () => void;
  onReset: () => void;
  currentFrame: number;
  totalFrames: number;
  onFrameChange: (frame: number) => void;
  playbackSpeed: number;
  onSpeedChange: (speed: number) => void;
}
```

### Timeline

Frame timeline component.

```typescript
interface TimelineProps {
  currentFrame: number;
  totalFrames: number;
  onChange: (frame: number) => void;
  markers?: number[];                 // Optional frame markers
}
```

### CameraControls

3D camera control configuration.

```typescript
interface CameraControlsProps {
  enablePan?: boolean;                // Enable panning (default: true)
  enableZoom?: boolean;               // Enable zooming (default: true)
  enableRotate?: boolean;             // Enable rotation (default: true)
  zoomSpeed?: number;                 // Zoom speed (default: 0.6)
  panSpeed?: number;                  // Pan speed (default: 0.5)
  rotateSpeed?: number;               // Rotation speed (default: 0.5)
}
```

## Utility Functions

### Pose Connections

```typescript
// Get color for joint based on body part
function getJointColor(jointIndex: number): number

// Get color for bone connection
function getConnectionColor(startJoint: number, endJoint: number): number

// Check if landmark is visible (confidence > threshold)
function isLandmarkVisible(landmark: number[]): boolean

// Default pose connections (MediaPipe format)
const DEFAULT_POSE_CONNECTIONS: number[][]

// Default hand connections
const DEFAULT_HAND_CONNECTIONS: number[][]
```

## IPC Channels

Inter-process communication channels for Electron.

### load-animation

Load animation data from file.

```typescript
// Main process handler
ipcMain.handle('load-animation', async (event, filePath?: string) => {
  // If no filePath, show file dialog
  // Load and validate JSON data
  // Return AnimationData or error
});

// Renderer process usage
const data = await window.electron.loadAnimationData(filePath);
```

### save-animation

Save animation data to file.

```typescript
// Main process handler
ipcMain.handle('save-animation', async (event, data: AnimationData, filePath?: string) => {
  // If no filePath, show save dialog
  // Write JSON data to file
  // Return success or error
});

// Renderer process usage
await window.electron.saveAnimationData(data, filePath);
```

### file-dialog

Show file selection dialog.

```typescript
// Main process handler
ipcMain.handle('file-dialog', async (event, options: OpenDialogOptions) => {
  // Show file dialog with options
  // Return selected file paths
});

// Renderer process usage
const files = await window.electron.showFileDialog({
  filters: [{ name: 'Animation Files', extensions: ['json'] }]
});
```

## Animation Loader API

### AnimationLoader.loadFromFile

Load animation data from a file.

```typescript
static async loadFromFile(file: File): Promise<AnimationData>
```

**Parameters:**
- `file`: File object to load

**Returns:**
- Promise resolving to AnimationData

**Throws:**
- Error if file reading fails
- Error if JSON parsing fails
- Error if data validation fails

### AnimationLoader.loadFromURL

Load animation data from a URL.

```typescript
static async loadFromURL(url: string): Promise<AnimationData>
```

**Parameters:**
- `url`: URL to fetch animation data from

**Returns:**
- Promise resolving to AnimationData

**Throws:**
- Error if network request fails
- Error if JSON parsing fails
- Error if data validation fails

### AnimationLoader.validateAnimationData

Validate animation data structure.

```typescript
static validateAnimationData(data: any): data is AnimationData
```

**Parameters:**
- `data`: Data to validate

**Returns:**
- Boolean indicating if data is valid AnimationData

### AnimationLoader.exportToFile

Export animation data to a file.

```typescript
static exportToFile(data: AnimationData, filename?: string): void
```

**Parameters:**
- `data`: AnimationData to export
- `filename`: Optional filename (default: 'animation.json')

## Animation Processor API

### AnimationProcessor.optimizeAnimationData

Optimize animation data by reducing precision.

```typescript
static optimizeAnimationData(data: AnimationData): AnimationData
```

**Parameters:**
- `data`: Original animation data

**Returns:**
- Optimized animation data with reduced precision

### AnimationProcessor.interpolateFrames

Interpolate frames to change frame rate.

```typescript
static interpolateFrames(data: AnimationData, targetFps: number): AnimationData
```

**Parameters:**
- `data`: Original animation data
- `targetFps`: Target frames per second

**Returns:**
- Animation data with interpolated frames

## Three.js Integration

### Scene Setup

```typescript
// Canvas configuration
<Canvas shadows>
  <PerspectiveCamera makeDefault position={[0, 0, 5]} fov={50} />
  <ambientLight intensity={0.6} />
  <directionalLight position={[10, 10, 10]} intensity={0.8} castShadow />
  <pointLight position={[-10, -10, -10]} intensity={0.4} />
  <StickFigure {...props} />
  <Grid args={[10, 10]} cellSize={0.5} />
  <OrbitControls />
</Canvas>
```

### Material Configuration

```typescript
// Joint material
const jointMaterial = new THREE.MeshPhongMaterial({
  color: 0x0000ff,
  emissive: 0x000066,
  shininess: 100,
  specular: 0x222222
});

// Bone material
const boneMaterial = new THREE.LineBasicMaterial({
  color: 0x00ff00,
  linewidth: 3,
  opacity: 0.9,
  transparent: true
});
```

---

For implementation examples, see:
- [Component Guide](../components/README.md)
- [Usage Guide](../guides/usage.md)
- [Data Models](./data-models.md)