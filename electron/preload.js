const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  // File operations
  selectVideo: () => ipcRenderer.invoke('select-video'),
  saveSession: (data) => ipcRenderer.invoke('save-session', data),
  loadSession: () => ipcRenderer.invoke('load-session'),
  exportVideo: (options) => ipcRenderer.invoke('export-video', options),
  
  // Backend communication
  backendRequest: (endpoint, method, data) => ipcRenderer.invoke('backend-request', endpoint, method, data),
  backendHealth: () => ipcRenderer.invoke('backend-health'),
  uploadVideo: (videoPath) => ipcRenderer.invoke('upload-video', videoPath),
  processVideo: (videoId) => ipcRenderer.invoke('process-video', videoId),
  getVideoStatus: (videoId) => ipcRenderer.invoke('get-video-status', videoId),
  getVideoResults: (videoId) => ipcRenderer.invoke('get-video-results', videoId),
  processStreamFrame: (frameData) => ipcRenderer.invoke('process-stream-frame', frameData),
  getTrainingForms: () => ipcRenderer.invoke('get-training-forms'),
  compareMovements: (userPoses, referenceForm) => ipcRenderer.invoke('compare-movements', userPoses, referenceForm),
  
  // Event listeners
  onBackendStatus: (callback) => {
    ipcRenderer.on('backend-status', (event, status) => callback(status));
  },
  
  onMenuAction: (action, callback) => {
    ipcRenderer.on(`menu-${action}`, () => callback());
  },
  
  onBackendReady: (callback) => {
    ipcRenderer.on('backend-ready', () => callback());
  },
  
  // System info
  platform: process.platform,
  versions: {
    node: process.versions.node,
    chrome: process.versions.chrome,
    electron: process.versions.electron
  }
});