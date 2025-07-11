const { app, BrowserWindow, ipcMain, dialog, Menu } = require('electron');
const path = require('path');
const isDev = require('electron-is-dev');
const fs = require('fs');

let mainWindow;

// Configure menu
const isMac = process.platform === 'darwin';
const template = [
  ...(isMac ? [{
    label: app.getName(),
    submenu: [
      { role: 'about' },
      { type: 'separator' },
      { role: 'services', submenu: [] },
      { type: 'separator' },
      { role: 'hide' },
      { role: 'hideOthers' },
      { role: 'unhide' },
      { type: 'separator' },
      { role: 'quit' }
    ]
  }] : []),
  {
    label: 'File',
    submenu: [
      {
        label: 'Open Video',
        accelerator: 'CmdOrCtrl+O',
        click: () => mainWindow.webContents.send('menu-open-video')
      },
      {
        label: 'Save Session',
        accelerator: 'CmdOrCtrl+S',
        click: () => mainWindow.webContents.send('menu-save-session')
      },
      {
        label: 'Load Session',
        accelerator: 'CmdOrCtrl+L',
        click: () => mainWindow.webContents.send('menu-load-session')
      },
      { type: 'separator' },
      isMac ? { role: 'close' } : { role: 'quit' }
    ]
  },
  {
    label: 'Edit',
    submenu: [
      { role: 'undo' },
      { role: 'redo' },
      { type: 'separator' },
      { role: 'cut' },
      { role: 'copy' },
      { role: 'paste' }
    ]
  },
  {
    label: 'View',
    submenu: [
      { role: 'reload' },
      { role: 'forceReload' },
      { role: 'toggleDevTools' },
      { type: 'separator' },
      { role: 'resetZoom' },
      { role: 'zoomIn' },
      { role: 'zoomOut' },
      { type: 'separator' },
      { role: 'togglefullscreen' }
    ]
  },
  {
    label: 'Window',
    submenu: [
      { role: 'minimize' },
      { role: 'close' },
      ...(isMac ? [
        { type: 'separator' },
        { role: 'front' }
      ] : [])
    ]
  }
];

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1600,
    height: 1000,
    minWidth: 1200,
    minHeight: 800,
    webPreferences: {
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
      webSecurity: !isDev
    },
    icon: path.join(__dirname, '..', 'public', 'icon.png'),
    titleBarStyle: 'hiddenInset',
    show: false
  });

  // Set up menu
  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);

  mainWindow.loadURL(
    isDev
      ? 'http://localhost:3000'
      : `file://${path.join(__dirname, '../build/index.html')}`
  );

  // Show window when ready
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
    if (isDev) {
      mainWindow.webContents.openDevTools();
    }
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// IPC handlers
ipcMain.handle('select-video', async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    properties: ['openFile'],
    filters: [
      { name: 'Videos', extensions: ['mp4', 'avi', 'mov', 'mkv', 'webm'] }
    ]
  });

  if (!result.canceled) {
    return result.filePaths[0];
  }
  return null;
});

ipcMain.handle('save-session', async (event, data) => {
  const result = await dialog.showSaveDialog(mainWindow, {
    defaultPath: `tai-chi-session-${new Date().toISOString().slice(0, 10)}.json`,
    filters: [
      { name: 'JSON', extensions: ['json'] }
    ]
  });

  if (!result.canceled) {
    fs.writeFileSync(result.filePath, JSON.stringify(data, null, 2));
    return result.filePath;
  }
  return null;
});

ipcMain.handle('load-session', async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    properties: ['openFile'],
    filters: [
      { name: 'JSON', extensions: ['json'] }
    ]
  });

  if (!result.canceled) {
    const data = fs.readFileSync(result.filePaths[0], 'utf8');
    return JSON.parse(data);
  }
  return null;
});

ipcMain.handle('export-video', async (event, options) => {
  const result = await dialog.showSaveDialog(mainWindow, {
    defaultPath: `tai-chi-export-${new Date().toISOString().slice(0, 10)}.mp4`,
    filters: [
      { name: 'MP4 Video', extensions: ['mp4'] }
    ]
  });

  if (!result.canceled) {
    return result.filePath;
  }
  return null;
});

const BACKEND_URL = 'http://127.0.0.1:5000';

ipcMain.handle('backend-request', async (event, endpoint, method = 'GET', data = null) => {
  try {
    const config = {
      method,
      url: `${BACKEND_URL}${endpoint}`,
      headers: {
        'Content-Type': 'application/json'
      }
    };

    if (data) {
      config.data = data;
    }

    const response = await axios(config);
    return { success: true, data: response.data };
  } catch (error) {
    console.error('Backend request error:', error);
    return {
      success: false,
      error: error.response?.data?.error || error.message
    };
  }
});

// Specific backend handlers
ipcMain.handle('backend-health', async () => {
  try {
    const response = await axios.get(`${BACKEND_URL}/health`);
    return response.data;
  } catch (error) {
    return { status: 'error', message: error.message };
  }
});

ipcMain.handle('upload-video', async (event, videoPath) => {
  try {
    const FormData = require('form-data');
    const form = new FormData();
    form.append('video', fs.createReadStream(videoPath));

    const response = await axios.post(`${BACKEND_URL}/video/upload`, form, {
      headers: form.getHeaders(),
      maxContentLength: Infinity,
      maxBodyLength: Infinity
    });

    return { success: true, data: response.data };
  } catch (error) {
    console.error('Video upload error:', error);
    return {
      success: false,
      error: error.response?.data?.error || error.message
    };
  }
});

ipcMain.handle('process-video', async (event, videoId) => {
  try {
    const response = await axios.post(`${BACKEND_URL}/video/process/${videoId}`);
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.error || error.message
    };
  }
});

ipcMain.handle('get-video-status', async (event, videoId) => {
  try {
    const response = await axios.get(`${BACKEND_URL}/video/status/${videoId}`);
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.error || error.message
    };
  }
});

ipcMain.handle('get-video-results', async (event, videoId) => {
  try {
    const response = await axios.get(`${BACKEND_URL}/video/results/${videoId}`);
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.error || error.message
    };
  }
});

ipcMain.handle('process-stream-frame', async (event, frameData) => {
  try {
    const response = await axios.post(`${BACKEND_URL}/video/stream`, {
      frame: frameData
    });
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.error || error.message
    };
  }
});

ipcMain.handle('get-training-forms', async () => {
  try {
    const response = await axios.get(`${BACKEND_URL}/training/forms`);
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.error || error.message
    };
  }
});

ipcMain.handle('compare-movements', async (event, userPoses, referenceForm) => {
  try {
    const response = await axios.post(`${BACKEND_URL}/analysis/compare`, {
      user_poses: userPoses,
      reference_form: referenceForm
    });
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.error || error.message
    };
  }
});

// App event handlers
app.whenReady().then(async () => {
  createWindow();
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});
