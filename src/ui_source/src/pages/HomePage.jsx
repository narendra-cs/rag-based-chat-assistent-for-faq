import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Button, Container, Typography, CircularProgress, Alert } from '@mui/material';

const HomePage = () => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(true);
  const [isBackendHealthy, setIsBackendHealthy] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const checkBackendHealth = async () => {
      try {
        const response = await fetch('/api/v1/health');
        if (response.ok) {
          setIsBackendHealthy(true);
        } else {
          throw new Error('Backend is not healthy');
        }
      } catch (err) {
        setError('Backend is having some issues. Please check the backend service.');
      } finally {
        setIsLoading(false);
      }
    };

    checkBackendHealth();
  }, []);

  const handleStartChat = () => {
    navigate('/chat');
  };

  if (isLoading) {
    return (
      <Box alignItems="center" display="flex" height="100vh" justifyContent="center">
        <CircularProgress />
      </Box>
    );
  }

  if (!isBackendHealthy) {
    return (
      <Container maxWidth="md" sx={{ mt: 8, textAlign: 'center' }}>
        <Alert severity="error" sx={{ mb: 3 }}>
          {error || 'Backend is having some issues. Please check the backend service.'}
        </Alert>
        <Button color="primary" variant="contained" onClick={() => window.location.reload()}>
          Retry
        </Button>
      </Container>
    );
  }

  return (
    <Container maxWidth="md" sx={{ mt: 8, textAlign: 'center' }}>
      <Typography gutterBottom component="h1" variant="h3">
        Welcome to the RAG-based Chat Assistant
      </Typography>
      <Typography paragraph color="text.secondary" variant="h5">
        Get started by clicking the button below to begin chatting with our AI assistant.
      </Typography>
      <Button
        color="primary"
        size="large"
        sx={{ mt: 4 }}
        variant="contained"
        onClick={handleStartChat}
      >
        Start Chatting
      </Button>
    </Container>
  );
};

export default HomePage;
