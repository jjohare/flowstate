# Electron Development Guide

## Overview

The Electron layer provides desktop application functionality, bridging the React frontend with the Python backend.

## Architecture

### Main Process (main.js)

```javascript
// Window management
// IPC communication
// Native API access
// Backend process management
```

### Preload Script (preload.js)

```javascript
// Secure context bridge
// API exposure to renderer
// Security isolation
```

## Key Features

### Window Management

- Main application window
- Video capture overlay
- Settings window
- About dialog

### IPC Communication

#### Main → Renderer
```javascript
win.webContents.send('video-processed', data);
```

#### Renderer → Main
```javascript
window.electronAPI.processVideo(videoData);
```

### Backend Integration

1. **Process Management**
   - Spawn Python backend on startup
   - Monitor backend health
   - Graceful shutdown

2. **Communication**
   - HTTP requests to Flask API
   - WebSocket for real-time data
   - File system access

## Security

### Context Isolation
```javascript
contextIsolation: true,
nodeIntegration: false,
webSecurity: true
```

### Preload API
```javascript
contextBridge.exposeInMainWorld('electronAPI', {
  processVideo: (data) => ipcRenderer.invoke('process-video', data),
  onProgress: (callback) => ipcRenderer.on('progress', callback)
});
```

## Development

### Running in Development

```bash
npm run dev:electron
```

### Debugging

1. **Main Process**
   ```bash
   electron --inspect=5858 .
   ```

2. **Renderer Process**
   - Chrome DevTools (Ctrl+Shift+I)
   - React DevTools extension

## Building & Distribution

### Configuration (electron-builder.yml)

```yaml
appId: com.flowstate.taichi
productName: Tai Chi Flow

mac:
  category: public.app-category.healthcare-fitness
  icon: assets/icon.icns
  
win:
  icon: assets/icon.ico
  target:
    - nsis
    - portable
    
linux:
  icon: assets/icon.png
  category: Education
  target:
    - AppImage
    - deb
```

### Building

```bash
# All platforms
npm run dist:all

# Platform specific
npm run dist:mac
npm run dist:win
npm run dist:linux
```

## Platform-Specific Features

### macOS
- Touch Bar support
- Native notifications
- Dock integration

### Windows
- Jump list tasks
- Thumbnail toolbar
- System tray

### Linux
- Desktop integration
- AppIndicator support

## Performance

### Memory Management
- Proper cleanup of video data
- Renderer process limits
- Background process optimization

### Startup Optimization
- Lazy loading of heavy modules
- Preload optimization
- Splash screen

## Updates

### Auto-Update Implementation

```javascript
const { autoUpdater } = require('electron-updater');

autoUpdater.checkForUpdatesAndNotify();
```

### Update Server Configuration
- GitHub Releases
- Custom update server
- Delta updates