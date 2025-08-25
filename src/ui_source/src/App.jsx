import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { Box, Container, CssBaseline, Toolbar, AppBar, Typography } from '@mui/material';

import HomePage from './pages/HomePage';
import ChatPage from './pages/ChatPage';

const theme = createTheme({
  palette: {
    primary: {
      main: '#008080', // Teal
      light: '#4fb3bf',
      dark: '#005b4f',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#ff6b6b', // Soft red for accents
      light: '#ff9e7d',
      dark: '#c73e1d',
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
  },
  components: {
    MuiAppBar: {
      styleOverrides: {
        root: {
          background: 'linear-gradient(45deg, #008080 30%, #4fb3bf 90%)',
        },
      },
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
          <AppBar position="static">
            <Toolbar>
              <Typography component="div" sx={{ flexGrow: 1 }} variant="h6">
                <Link style={{ textDecoration: 'none', color: 'inherit' }} to="/">
                  Q & A Chatbot
                </Link>
              </Typography>
            </Toolbar>
          </AppBar>

          <Container component="main" sx={{ mt: 4, mb: 4, flex: 1 }}>
            <Routes>
              <Route element={<HomePage />} path="/" />
              <Route element={<ChatPage />} path="/chat" />
            </Routes>
          </Container>

          <Box
            component="footer"
            sx={{ py: 3, px: 2, mt: 'auto', backgroundColor: (theme) => theme.palette.grey[200] }}
          >
            <Container maxWidth="sm">
              <Typography align="center" color="text.secondary" variant="body2">
                {new Date().getFullYear()} Q & A Chatbot
              </Typography>
            </Container>
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;
