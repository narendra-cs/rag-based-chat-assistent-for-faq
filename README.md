# RAG-based Chat Assistant for FAQ

A specialized Retrieval-Augmented Generation (RAG) system that enhances product support by providing accurate, context-aware responses to customer inquiries. This solution combines the power of large language models with targeted knowledge retrieval from product documentation.

## 🎯 Project Objective

This project implements a RAG-based chat assistant that helps users find accurate product information by:
- Processing and indexing FAQ documents using advanced embedding models
- Enabling natural language queries about product features and support
- Retrieving relevant context before generating responses
- Providing a user-friendly interface for seamless interaction

## 🚀 Features

### Core Capabilities
- **PDF Processing**: Extracts and structures FAQ content from product documentation
- **Smart Chunking**: Breaks down documents into meaningful segments for precise retrieval
- **Vector Embeddings**: Converts text into high-dimensional vectors for semantic search

### Intelligent Retrieval
- **Contextual Search**: Finds the most relevant FAQ sections for each query
- **Semantic Understanding**: Matches user questions with document content beyond simple keyword matching
- **Efficient Storage**: Uses ChromaDB for fast and scalable vector similarity search

### Advanced RAG Workflow
- **Context-Enriched Generation**: Enhances LLM responses with retrieved document excerpts
- **Confidence Scoring**: Indicates response reliability based on source material relevance
- **Source Attribution**: Provides references to the original document sections

### User Experience
- **Natural Interaction**: Understands and responds to free-form product questions
- **Conversation Flow**: Maintains context for follow-up questions
- **Clear Feedback**: Handles unknown queries gracefully with helpful guidance

### Observability & Monitoring
- **Observability**: Integrated with LangSmith for tracing and debugging
- **Modular Design**: Easy to extend with additional data sources or LLM providers
- **Performance Metrics**: Tracks response quality and system performance

### Extensibility
- **Modular Architecture**: Easy integration of additional document sources

## 🛠️ Tech Stack

- **Backend**: FastAPI, Uvicorn
- **Vector Database**: ChromaDB
- **LLM Integration**: OpenAI
- **NLP**: LangChain
- **Frontend**: React
- **Environment**: Python 3.8+

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/narendra-cs/rag-based-chat-assistent-for-faq.git
   cd rag-based-chat-assistent-for-faq
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Copy `.env.example` to `.env` and update the values:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file with your configuration (API keys, model names, etc.)

## 🚀 Quick Start

1. **Start the backend server**
   ```bash
   python -m src.main
   ```

2. **Access the web interface**
   Open your browser and navigate to `http://localhost:8000`

3. **Upload documents** : (To be implemented)
   - Use the web interface to upload PDFs or other supported documents
   - The system will automatically process and index the content

4. **Start chatting**
   - Type your questions in the chat interface
   - The assistant will provide answers based on the uploaded documents

## 🔧 Configuration

Edit the `.env` file to customize the application:

```env
# LLM Configuration
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key

# LangChain API Key
LANGCHAIN_API_KEY=your_langchain_api_key
LANGCHAIN_PROJECT="your_langchain_project"
LANGCHAIN_TRACING_V2=true

# Application Settings
LOG_LEVEL=info
ENVIRONMENT=development
```

## 📚 Documentation

For detailed documentation, please refer to the [docs](docs/) directory.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with ❤️ using FastAPI and LangChain
- Thanks to all contributors who have helped improve this project

## 📞 Contact

For any questions or feedback, please open an issue on GitHub.
