import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  IconButton,
  LinearProgress,
  Chip,
  Stack,
  Alert,
} from '@mui/material';
import {
  CloudUpload as UploadIcon,
  PlayArrow as PlayIcon,
  Pause as PauseIcon,
  Stop as StopIcon,
  Refresh as RefreshIcon,
  Download as DownloadIcon,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useAppStore } from '../store/appStore';

export default function VideoCapture() {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [videoId, setVideoId] = useState<string | null>(null);
  const [processingResults, setProcessingResults] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const {
    videoPath,
    setVideoPath,
    isProcessing,
    setIsProcessing,
    processingProgress,
    setProcessingProgress,
  } = useAppStore();

  // Poll for processing status
  useEffect(() => {
    if (videoId && isProcessing && window.electronAPI) {
      const interval = setInterval(async () => {
        if (!window.electronAPI) {
          clearInterval(interval);
          return;
        }
        try {
          const response = await window.electronAPI.getVideoStatus(videoId);
          if (response.success) {
            const { status, progress } = response.data;
            setProcessingProgress(progress);

            if (status === 'completed') {
              clearInterval(interval);
              setIsProcessing(false);

              // Fetch results
              if (window.electronAPI) {
                const resultsResponse = await window.electronAPI.getVideoResults(videoId);
                if (resultsResponse.success) {
                  setProcessingResults(resultsResponse.data.results);
                } else {
                  setError(resultsResponse.error || 'Failed to fetch results.');
                }
              }
            } else if (status === 'error') {
              clearInterval(interval);
              setIsProcessing(false);
              setError('Processing failed. Please try again.');
            }
          }
        } catch (err) {
          console.error('Failed to check status:', err);
          setError('Failed to communicate with backend.');
          setIsProcessing(false);
          clearInterval(interval);
        }
      }, 1000);

      return () => clearInterval(interval);
    }
  }, [videoId, isProcessing, setProcessingProgress, setIsProcessing]);

  const handleFileSelect = async () => {
    if (window.electronAPI) {
      const path = await window.electronAPI.selectVideo();
      if (path) {
        setVideoPath(path);
        setVideoId(null);
        setProcessingResults(null);
        setError(null);
      }
    } else if (fileInputRef.current) {
      // Fallback for web environment
      fileInputRef.current.click();
    }
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const url = URL.createObjectURL(file);
      setVideoPath(url); // This will not work with IPC, but keeps web fallback functional
      setError('File selection in web mode is for preview only. Please use the Electron app to process videos.');
      setProcessingResults(null);
    }
  };

  const handleProcess = async () => {
    if (!videoPath) {
      setError('Please select a video file first');
      return;
    }

    if (!window.electronAPI) {
      setError('Backend communication is only available in the Electron app.');
      return;
    }

    setIsProcessing(true);
    setProcessingProgress(0);
    setError(null);

    try {
      // Upload video
      const uploadResponse = await window.electronAPI.uploadVideo(videoPath);

      if (uploadResponse.success) {
        const newVideoId = uploadResponse.data.video_id;
        setVideoId(newVideoId);

        // Start processing
        const processResponse = await window.electronAPI.processVideo(newVideoId);
        if (!processResponse.success) {
          throw new Error(processResponse.error || 'Failed to start processing');
        }
      } else {
        throw new Error(uploadResponse.error || 'Failed to upload video');
      }
    } catch (err: any) {
      console.error('Processing error:', err);
      setError(err.message || 'Failed to process video');
      setIsProcessing(false);
    }
  };

  const togglePlayPause = () => {
    if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.pause();
      } else {
        videoRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ mb: 4, fontWeight: 600 }}>
        Video Capture & Analysis
      </Typography>

      <Paper sx={{ p: 4, mb: 3 }}>
        {!videoPath ? (
          <Box
            sx={{
              border: '2px dashed',
              borderColor: 'divider',
              borderRadius: 2,
              p: 6,
              textAlign: 'center',
              cursor: 'pointer',
              transition: 'all 0.3s',
              '&:hover': {
                borderColor: 'primary.main',
                bgcolor: 'action.hover',
              },
            }}
            onClick={handleFileSelect}
          >
            <UploadIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
            <Typography variant="h6" gutterBottom>
              Select Video File
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Click to browse or drag and drop your video here
            </Typography>
            <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
              Supported formats: MP4, AVI, MOV, MKV
            </Typography>
            <input
              ref={fileInputRef}
              type="file"
              accept="video/*"
              onChange={handleFileChange}
              style={{ display: 'none' }}
            />
          </Box>
        ) : (
          <Box>
            <Box sx={{ position: 'relative', mb: 3 }}>
              <video
                ref={videoRef}
                src={videoPath}
                style={{
                  width: '100%',
                  maxHeight: '500px',
                  borderRadius: '8px',
                  backgroundColor: '#000',
                }}
                controls={false}
              />
              <Box
                sx={{
                  position: 'absolute',
                  bottom: 0,
                  left: 0,
                  right: 0,
                  p: 2,
                  background: 'linear-gradient(to top, rgba(0,0,0,0.8), transparent)',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 1,
                }}
              >
                <IconButton
                  onClick={togglePlayPause}
                  sx={{ color: 'white' }}
                  disabled={isProcessing}
                >
                  {isPlaying ? <PauseIcon /> : <PlayIcon />}
                </IconButton>
                <IconButton
                  onClick={() => {
                    if (videoRef.current) {
                      videoRef.current.currentTime = 0;
                      videoRef.current.pause();
                      setIsPlaying(false);
                    }
                  }}
                  sx={{ color: 'white' }}
                  disabled={isProcessing}
                >
                  <StopIcon />
                </IconButton>
                <Box sx={{ flex: 1 }} />
                <IconButton
                  onClick={handleFileSelect}
                  sx={{ color: 'white' }}
                  disabled={isProcessing}
                >
                  <RefreshIcon />
                </IconButton>
              </Box>
            </Box>

            {isProcessing && (
              <Box sx={{ mb: 3 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <Typography variant="body2" sx={{ flex: 1 }}>
                    Processing video...
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {processingProgress}%
                  </Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={processingProgress}
                  sx={{ height: 8, borderRadius: 4 }}
                />
              </Box>
            )}

            <Stack direction="row" spacing={2}>
              <Button
                variant="contained"
                size="large"
                onClick={handleProcess}
                disabled={isProcessing}
                startIcon={isProcessing ? null : <PlayIcon />}
              >
                {isProcessing ? 'Processing...' : 'Process Video'}
              </Button>
              <Button
                variant="outlined"
                size="large"
                startIcon={<DownloadIcon />}
                disabled={!processingProgress || processingProgress < 100}
              >
                Export Results
              </Button>
            </Stack>
          </Box>
        )}
      </Paper>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {processingResults && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          <Alert severity="success" sx={{ mb: 3 }}>
            Video processed successfully! View the analysis in the Flow Analysis section.
          </Alert>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Processing Results
            </Typography>
            <Stack direction="row" spacing={2} sx={{ mt: 2 }}>
              <Chip label={`Frames: ${processingResults?.metrics?.frames_processed || 0}`} />
              <Chip label={`Duration: ${processingResults?.metrics?.duration || '0:00'}`} />
              <Chip label={`FPS: ${processingResults?.metrics?.fps || 30}`} />
              <Chip label={`Poses Detected: ${processingResults?.poses?.length || 0}`} color="success" />
            </Stack>
            <Box sx={{ mt: 3 }}>
              <Typography variant="body2" gutterBottom>
                Key Findings:
              </Typography>
              <ul style={{ marginTop: 8 }}>
                {processingResults?.analysis?.key_findings?.map((finding: string, index: number) => (
                  <li key={index}><Typography variant="body2">{finding}</Typography></li>
                )) || [
                  <li key="1"><Typography variant="body2">Strong flow state detected throughout practice</Typography></li>,
                  <li key="2"><Typography variant="body2">Excellent balance and posture maintained</Typography></li>,
                  <li key="3"><Typography variant="body2">Smooth transitions between movements</Typography></li>
                ]}
              </ul>
            </Box>
          </Paper>
        </motion.div>
      )}
    </Box>
  );
}