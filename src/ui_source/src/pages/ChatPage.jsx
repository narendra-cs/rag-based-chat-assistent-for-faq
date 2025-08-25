/**
 * @typedef {'user' | 'bot'} MessageSender
 * @typedef {Object} Message
 * @property {string|number} id - Unique identifier for the message
 * @property {string} text - The message content
 * @property {MessageSender} sender - The sender of the message ('user' or 'bot')
 * @property {Date} timestamp - When the message was sent
 * @property {boolean} [isError] - Optional flag indicating if this is an error message
 */

import { useState, useRef, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import {
  Box,
  Container,
  TextField,
  IconButton,
  Paper,
  Typography,
  Avatar,
  List,
  ListItem,
  ListItemAvatar,
  Divider,
  Button,
  Snackbar,
  Alert,
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import DeleteIcon from '@mui/icons-material/Delete';
import RefreshIcon from '@mui/icons-material/Refresh';
import PersonIcon from '@mui/icons-material/Person';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import {
  chatContainer,
  chatPaper,
  chatHeader,
  messagesContainer,
  messageItem,
  messageAvatar,
  messageBubble,
  messageTime,
  inputContainer,
  textField,
  sendButton,
} from './ChatPage.styles';

// Helper function to get or create session ID
const getOrCreateSessionId = () => {
  const storedSessionId = sessionStorage.getItem('chatSessionId');
  if (storedSessionId) {
    return storedSessionId;
  }
  const newSessionId = uuidv4();
  sessionStorage.setItem('chatSessionId', newSessionId);
  return newSessionId;
};

const ChatPage = () => {
  /** @type {Message} */
  const greetingMessage = {
    id: Date.now(),
    text: 'Hello! How can I assist you today?',
    sender: 'bot',
    timestamp: new Date(),
  };

  const [input, setInput] = useState('');
  const [sessionId, setSessionId] = useState(getOrCreateSessionId);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success',
  });
  /** @type {[Message[], import('react').Dispatch<import('react').SetStateAction<Message[]>>]} */
  const [messages, setMessages] = useState([greetingMessage]);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  /**
   * Handles sending a message
   * @param {React.FormEvent} e - The form submission event
   * @returns {Promise<void>}
   */
  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    /** @type {Message} */
    const userMessage = {
      id: Date.now(),
      text: input.trim(),
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');

    try {
      const response = await fetch('/api/v1/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: input.trim(),
          session_id: sessionId,
        }),
      });

      if (!response.ok) throw new Error('Failed to get response');

      const data = await response.json();

      /** @type {Message} */
      const botMessage = {
        id: Date.now() + 1,
        text: data.answer.trim(),
        sender: 'bot',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      /** @type {Message} */
      const errorMessage = {
        id: Date.now() + 2,
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'bot',
        timestamp: new Date(),
        isError: true,
      };
      setMessages((prev) => [...prev, errorMessage]);
    }
  };

  /**
   * Clears the current chat session
   * @returns {Promise<void>}
   */
  const clearChat = async () => {
    try {
      const response = await fetch(`/api/v1/chat/${sessionId}`, {
        method: 'DELETE',
      });

      if (!response.ok) throw new Error('Failed to clear chat');

      // Reset to just the greeting message with the new session
      setMessages([
        {
          id: Date.now(),
          text: 'Chat has been cleared. How can I assist you now?',
          sender: 'bot',
          timestamp: new Date(),
        },
      ]);

      // Clear the current session ID from storage and generate a new one
      sessionStorage.removeItem('chatSessionId');
      const newSessionId = getOrCreateSessionId();
      setSessionId(newSessionId);
    } catch (error) {
      // Add error message to chat
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          text: 'Failed to clear chat. Please try again.',
          sender: 'bot',
          timestamp: new Date(),
          isError: true,
        },
      ]);
    }
  };

  /**
   * Reloads the context data
   * @returns {Promise<void>}
   */
  const reloadContext = async () => {
    try {
      const response = await fetch('/api/v1/documents/load?reload=true&product=EduTrack');

      if (!response.ok) throw new Error('Failed to reload context');

      setSnackbar({
        open: true,
        message: 'Documents reloaded successfully',
        severity: 'success',
      });
    } catch (error) {
      setSnackbar({
        open: true,
        message: 'Failed to reload documents',
        severity: 'error',
      });
    }
  };

  const handleCloseSnackbar = () => {
    setSnackbar((prev) => ({ ...prev, open: false }));
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <Container maxWidth="md" sx={chatContainer}>
      <Paper elevation={3} sx={chatPaper}>
        <Box sx={chatHeader}>
          <SmartToyIcon sx={{ mr: 1 }} />
          <Typography sx={{ flexGrow: 1 }} variant="h6">
            AI Assistant
          </Typography>

          <Button
            size="small"
            startIcon={<RefreshIcon />}
            sx={{
              textTransform: 'none',
              color: 'white',
              borderColor: 'rgba(255, 255, 255, 0.5)',
              mr: 1,
              '&:hover': {
                borderColor: 'white',
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
              },
            }}
            variant="outlined"
            onClick={reloadContext}
          >
            Reload Context
          </Button>

          <Button
            size="small"
            startIcon={<DeleteIcon />}
            sx={{
              textTransform: 'none',
              color: 'white',
              borderColor: 'rgba(255, 255, 255, 0.5)',
              '&:hover': {
                borderColor: 'white',
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
              },
            }}
            variant="outlined"
            onClick={clearChat}
          >
            Clear Chat
          </Button>
        </Box>

        <Box sx={messagesContainer}>
          <List>
            {messages.map((message) => {
              const isUser = message.sender === 'user';
              return (
                <Box key={message.id}>
                  <ListItem sx={messageItem(isUser)}>
                    <ListItemAvatar>
                      <Avatar sx={messageAvatar(isUser)}>
                        {isUser ? <PersonIcon /> : <SmartToyIcon />}
                      </Avatar>
                    </ListItemAvatar>
                    <Box sx={messageBubble(isUser, message.isError)}>
                      <Typography variant="body1">{message.text}</Typography>
                      <Typography sx={messageTime(isUser)} variant="caption">
                        {formatTime(message.timestamp)}
                      </Typography>
                    </Box>
                  </ListItem>
                  <Divider component="li" />
                </Box>
              );
            })}
            <div ref={messagesEndRef} />
          </List>
        </Box>

        <Box component="form" sx={inputContainer} onSubmit={handleSend}>
          <TextField
            fullWidth
            multiline
            maxRows={4}
            placeholder="Type your message..."
            size="small"
            sx={{
              ...textField,
              '& .MuiInputBase-root': {
                alignItems: 'flex-start',
              },
              '& textarea': {
                maxHeight: '120px',
                overflowY: 'auto !important',
              },
            }}
            value={input}
            variant="outlined"
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend(e);
              }
            }}
          />
          <IconButton
            color="primary"
            disabled={!input.trim()}
            sx={sendButton(!input.trim())}
            type="submit"
          >
            <SendIcon />
          </IconButton>
        </Box>
      </Paper>
      <Snackbar
        anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
        autoHideDuration={6000}
        open={snackbar.open}
        onClose={handleCloseSnackbar}
      >
        <Alert
          severity={snackbar.severity}
          sx={{ width: '100%' }}
          variant="filled"
          onClose={handleCloseSnackbar}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default ChatPage;
