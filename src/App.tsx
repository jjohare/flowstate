import React, { useEffect } from 'react';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import Layout from './components/Layout';
import Dashboard from './components/Dashboard';
import VideoCapture from './components/VideoCapture';
import Training from './components/Training';
import FlowAnalysis from './components/FlowAnalysis';
import Settings from './components/Settings';
import { useAppStore } from './store/appStore';
import './App.css';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#00bcd4',
    },
    secondary: {
      main: '#ff4081',
    },
    background: {
      default: '#0a0a0a',
      paper: '#1a1a1a',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '3rem',
      fontWeight: 700,
    },
    h2: {
      fontSize: '2.5rem',
      fontWeight: 600,
    },
  },
  shape: {
    borderRadius: 12,
  },
});

function App() {
  const { initializeApp, setBackendStatus } = useAppStore();

  useEffect(() => {
    initializeApp();

    // Listen for backend status updates
    if (window.electronAPI) {
      window.electronAPI.onBackendStatus((status: any) => {
        setBackendStatus(status);
      });

      // Menu action handlers
      window.electronAPI.onMenuAction('open-video', () => {
        // Handle open video from menu
        console.log('Open video from menu');
      });

      window.electronAPI.onMenuAction('save-session', () => {
        // Handle save session from menu
        console.log('Save session from menu');
      });

      window.electronAPI.onMenuAction('load-session', () => {
        // Handle load session from menu
        console.log('Load session from menu');
      });
    }
  }, [initializeApp, setBackendStatus]);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <AnimatePresence mode="wait">
          <Layout>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/capture" element={<VideoCapture />} />
              <Route path="/training" element={<Training />} />
              <Route path="/flow" element={<FlowAnalysis />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </Layout>
        </AnimatePresence>
      </Router>
    </ThemeProvider>
  );
}

export default App;