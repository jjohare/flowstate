import React from 'react';
import { Box, Typography } from '@mui/material';

export default function Settings() {
  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ mb: 4, fontWeight: 600 }}>
        Settings
      </Typography>
      <Typography variant="body1" color="text.secondary">
        Settings module coming soon...
      </Typography>
    </Box>
  );
}