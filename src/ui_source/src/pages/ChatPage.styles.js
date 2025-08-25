export const chatContainer = {
  height: 'calc(100vh - 200px)',
  py: 2,
};

export const chatPaper = {
  display: 'flex',
  flexDirection: 'column',
  height: '100%',
  borderRadius: 2,
  overflow: 'hidden',
};

export const chatHeader = {
  display: 'flex',
  alignItems: 'center',
  padding: '12px 16px',
  borderBottom: '1px solid rgba(0, 0, 0, 0.12)',
  backgroundColor: 'primary.main',
  color: 'white',
  borderRadius: '4px 4px 0 0',
};

export const messagesContainer = {
  flex: 1,
  p: 2,
  overflowY: 'auto',
  bgcolor: 'background.default',
};

export const messageItem = (isUser) => ({
  display: 'flex',
  flexDirection: isUser ? 'row-reverse' : 'row',
  alignItems: 'flex-start',
  mb: 1,
});

export const messageAvatar = (isUser) => ({
  bgcolor: isUser ? 'primary.main' : 'grey.500',
});

export const messageBubble = (isUser) => ({
  maxWidth: '70%',
  bgcolor: isUser ? 'primary.light' : 'grey.200',
  color: isUser ? 'white' : 'text.primary',
  p: 1.5,
  borderRadius: 2,
  position: 'relative',
  '&:after': {
    content: '""',
    position: 'absolute',
    width: 0,
    height: 0,
    borderStyle: 'solid',
    borderWidth: '10px 10px 0 0',
    borderColor: `${isUser ? '#008080' : '#e0e0e0'} transparent transparent transparent`,
    [isUser ? 'right' : 'left']: -10,
    top: 0,
    transform: isUser ? 'rotate(90deg)' : 'rotate(-90deg)',
  },
});

export const messageTime = (isUser) => ({
  display: 'block',
  textAlign: 'right',
  color: isUser ? 'rgba(255,255,255,0.7)' : 'text.secondary',
  mt: 0.5,
});

export const inputContainer = {
  p: 2,
  borderTop: '1px solid',
  borderColor: 'divider',
  display: 'flex',
  alignItems: 'center',
  gap: 1,
};

export const textField = {
  '& .MuiOutlinedInput-root': {
    borderRadius: 4,
    bgcolor: 'background.paper',
  },
};

export const sendButton = () => ({
  bgcolor: 'primary.main',
  color: 'white',
  '&:hover': {
    bgcolor: 'primary.dark',
  },
  '&.Mui-disabled': {
    bgcolor: 'action.disabledBackground',
    color: 'action.disabled',
  },
});
