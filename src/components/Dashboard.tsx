import React from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
  LinearProgress,
  Chip,
} from '@mui/material';
import {
  PlayArrow as PlayIcon,
  Assessment as AssessmentIcon,
  TrendingUp as TrendingUpIcon,
  Schedule as ScheduleIcon,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useAppStore } from '../store/appStore';

const stats = [
  {
    title: 'Total Sessions',
    value: '24',
    change: '+12%',
    icon: <PlayIcon />,
    color: 'primary',
  },
  {
    title: 'Flow Score',
    value: '87%',
    change: '+5%',
    icon: <TrendingUpIcon />,
    color: 'success',
  },
  {
    title: 'Practice Time',
    value: '12.5h',
    change: '+2.3h',
    icon: <ScheduleIcon />,
    color: 'info',
  },
  {
    title: 'Accuracy',
    value: '92%',
    change: '+3%',
    icon: <AssessmentIcon />,
    color: 'warning',
  },
];

const recentSessions = [
  {
    id: '1',
    name: 'Morning Practice',
    date: '2024-01-15',
    duration: '45 min',
    flowScore: 85,
  },
  {
    id: '2',
    name: 'Evening Flow',
    date: '2024-01-14',
    duration: '30 min',
    flowScore: 92,
  },
  {
    id: '3',
    name: 'Form Training',
    date: '2024-01-13',
    duration: '60 min',
    flowScore: 78,
  },
];

export default function Dashboard() {
  const navigate = useNavigate();
  const { currentSession, flowMetrics } = useAppStore();

  const cardVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: (i: number) => ({
      opacity: 1,
      y: 0,
      transition: {
        delay: i * 0.1,
        duration: 0.3,
      },
    }),
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ mb: 4, fontWeight: 600 }}>
        Welcome Back
      </Typography>

      {/* Stats Grid */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {stats.map((stat, index) => (
          <Grid item xs={12} sm={6} md={3} key={stat.title}>
            <motion.div
              custom={index}
              initial="hidden"
              animate="visible"
              variants={cardVariants}
            >
              <Paper
                sx={{
                  p: 3,
                  display: 'flex',
                  flexDirection: 'column',
                  height: 140,
                  position: 'relative',
                  overflow: 'hidden',
                  '&::before': {
                    content: '""',
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    right: 0,
                    height: 4,
                    bgcolor: `${stat.color}.main`,
                  },
                }}
              >
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Box
                    sx={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      width: 48,
                      height: 48,
                      borderRadius: 2,
                      bgcolor: `${stat.color}.main`,
                      color: 'white',
                      mr: 2,
                    }}
                  >
                    {stat.icon}
                  </Box>
                  <Typography color="text.secondary" variant="body2">
                    {stat.title}
                  </Typography>
                </Box>
                <Typography variant="h4" component="div" sx={{ fontWeight: 700 }}>
                  {stat.value}
                </Typography>
                <Typography
                  variant="body2"
                  sx={{
                    color: stat.change.startsWith('+') ? 'success.main' : 'error.main',
                    mt: 'auto',
                  }}
                >
                  {stat.change} from last week
                </Typography>
              </Paper>
            </motion.div>
          </Grid>
        ))}
      </Grid>

      {/* Main Actions */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Quick Actions
              </Typography>
              <Grid container spacing={2} sx={{ mt: 1 }}>
                <Grid item xs={12} sm={6}>
                  <Button
                    variant="contained"
                    size="large"
                    fullWidth
                    startIcon={<PlayIcon />}
                    onClick={() => navigate('/capture')}
                    sx={{ py: 2 }}
                  >
                    Start New Session
                  </Button>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Button
                    variant="outlined"
                    size="large"
                    fullWidth
                    startIcon={<AssessmentIcon />}
                    onClick={() => navigate('/flow')}
                    sx={{ py: 2 }}
                  >
                    View Analysis
                  </Button>
                </Grid>
              </Grid>
            </CardContent>
          </Card>

          {/* Recent Sessions */}
          <Card sx={{ mt: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Sessions
              </Typography>
              <Box sx={{ mt: 2 }}>
                {recentSessions.map((session) => (
                  <Box
                    key={session.id}
                    sx={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      p: 2,
                      borderRadius: 2,
                      mb: 1,
                      bgcolor: 'background.default',
                      '&:hover': {
                        bgcolor: 'action.hover',
                      },
                    }}
                  >
                    <Box>
                      <Typography variant="subtitle1">{session.name}</Typography>
                      <Typography variant="body2" color="text.secondary">
                        {session.date} • {session.duration}
                      </Typography>
                    </Box>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                      <Chip
                        label={`Flow: ${session.flowScore}%`}
                        color={session.flowScore > 80 ? 'success' : 'default'}
                        size="small"
                      />
                      <Button size="small">View</Button>
                    </Box>
                  </Box>
                ))}
              </Box>
            </CardContent>
            <CardActions>
              <Button size="small" fullWidth>
                View All Sessions
              </Button>
            </CardActions>
          </Card>
        </Grid>

        {/* Current Flow State */}
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Current Flow State
              </Typography>
              <Box sx={{ mt: 3 }}>
                {Object.entries(flowMetrics).map(([key, value]) => (
                  <Box key={key} sx={{ mb: 3 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="body2" sx={{ textTransform: 'capitalize' }}>
                        {key}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {Math.round(value * 100)}%
                      </Typography>
                    </Box>
                    <LinearProgress
                      variant="determinate"
                      value={value * 100}
                      sx={{
                        height: 8,
                        borderRadius: 4,
                        bgcolor: 'background.default',
                        '& .MuiLinearProgress-bar': {
                          borderRadius: 4,
                          bgcolor: value > 0.7 ? 'success.main' : value > 0.4 ? 'warning.main' : 'error.main',
                        },
                      }}
                    />
                  </Box>
                ))}
              </Box>
              <Button
                variant="contained"
                fullWidth
                sx={{ mt: 3 }}
                onClick={() => navigate('/training')}
              >
                Start Training
              </Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}