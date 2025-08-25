# RAG-based Chat Assistant for FAQ - Frontend

This is the frontend for the RAG-based Chat Assistant for FAQ, built with React, Material-UI, and Vite.

## Prerequisites

- Node.js (v16 or later)
- npm (v7 or later) or yarn
- Python 3.8+ (for backend)

## Getting Started

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <repository-url>
   cd rag-based-chat-assistent-for-faq
   ```

2. **Install frontend dependencies**:
   ```bash
   cd src/ui_source
   npm install
   # or
   yarn
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. **Access the application**:
   Open your browser and navigate to `http://localhost:8080`

## Development

### Available Scripts

- `npm run dev` - Start the development server
- `npm run build` - Build for production
- `npm run lint` - Run ESLint
- `npm run format` - Format code using Prettier

### Environment Variables

The following environment variables can be configured:

- `VITE_API_BASE_URL` - Base URL for API requests (default: `/api/v1`)

## Project Structure

- `src/` - Source code
  - `components/` - Reusable UI components
  - `pages/` - Page components
  - `App.jsx` - Main application component
  - `main.jsx` - Application entry point

## Backend Integration

The frontend communicates with the FastAPI backend through the following API endpoints:

- `POST /api/v1/chat` - Send a chat message
- `DELETE /api/v1/chat/{session_id}` - Clear chat session
- `GET /api/v1/health` - Health check
- `GET /api/v1/documents/load` - Reload context

## License

This project is licensed under the MIT License.
