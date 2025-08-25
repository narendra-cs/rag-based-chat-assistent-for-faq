export type MessageSender = 'user' | 'bot';

export interface Message {
  id: string | number;
  text: string;
  sender: MessageSender;
  timestamp: Date;
  isError?: boolean;  // Optional flag for error messages
}

// Example usage:
// const message: Message = {
//   id: 1,
//   text: 'Hello!',
//   sender: 'user',
//   timestamp: new Date(),
//   isError: false
// };
