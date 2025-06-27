# 🛠 TotaPakhii - Agentic RAG Chat Application

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Gradio](https://img.shields.io/badge/Interface-Gradio-orange.svg)](https://gradio.app/)

**TotaPakhii** is an advanced AI-powered chat application that leverages Large Language Models (LLM) and Retrieval-Augmented Generation (RAG) methodology to provide intelligent document-based question answering. Built with modern technologies, it offers conversational memory, context awareness, and semantic document search capabilities.

## ✨ Features

- 🧠 **Intelligent RAG System**: Advanced retrieval-augmented generation for accurate document-based responses
- 💬 **Conversational Memory**: Maintains context across conversations for natural dialogue flow
- 📚 **Multi-PDF Support**: Process and query multiple PDF documents simultaneously
- 🔍 **Semantic Search**: Vector-based similarity search using state-of-the-art embeddings
- 🎨 **Modern UI**: Claude AI-inspired interface with dark theme and responsive design
- 📱 **Mobile Responsive**: Optimized for both desktop and mobile devices
- 💾 **Chat History**: Persistent conversation storage with session management
- 🚀 **Real-time Processing**: Fast document retrieval and response generation

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   PDF Documents │───▶│  Vector Embedding │───▶│   Pinecone DB   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Gradio UI     │◄───│   Chat Server    │◄───│  LangChain RAG  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Groq LLM      │
                       │  (Llama 3.3)    │
                       └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Pinecone API account
- Groq API account

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/totapakhii.git
   cd totapakhii
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   PINECONE_API_KEY=your_pinecone_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   ```

### Document Preparation

1. **Add your PDF documents**
   ```bash
   mkdir documents
   # Place your PDF files in the documents/ folder
   ```

2. **Create vector embeddings**
   ```bash
   python VectorEmbedding.py
   ```
   This will:
   - Process all PDFs in the `documents/` folder
   - Create vector embeddings using HuggingFace sentence transformers
   - Store embeddings in Pinecone vector database

### Launch the Application

```bash
python NewActiveServer.py
```

The application will be available at: `http://127.0.0.1:7860`

## 💡 Usage

1. **Start a New Chat**: Click the "+ New Chat" button to begin a conversation
2. **Ask Questions**: Type your questions about the uploaded documents
3. **View Sources**: Expand the "Source Documents" section to see relevant document excerpts
4. **Browse History**: Use the sidebar to navigate between previous conversations
5. **Clear History**: Use "Clear All History" to reset all conversations

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | Gradio | Interactive web interface |
| **Backend** | Python, FastAPI | Application server |
| **LLM** | Groq (Llama 3.3-70B) | Language model for responses |
| **Embeddings** | HuggingFace Transformers | Document vectorization |
| **Vector DB** | Pinecone | Semantic search and retrieval |
| **RAG Framework** | LangChain | Document processing pipeline |
| **PDF Processing** | PyPDF | Document text extraction |

## 📁 Project Structure

```
totapakhii/
├── NewActiveServer.py          # Main chat server application
├── VectorEmbedding.py         # Document processing and embedding
├── requirements.txt           # Python dependencies
├── README.md                 # Project documentation
├── .env                      # Environment variables (create this)
├── documents/                # PDF documents folder (create this)
│   ├── document1.pdf
│   ├── document2.pdf
│   └── ...
└── venv/                     # Virtual environment (auto-generated)
```

## ⚙️ Configuration

### Model Settings

You can customize the LLM behavior in `NewActiveServer.py`:

```python
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile",
    temperature=0.5,        # Adjust creativity (0.0-1.0)
    max_tokens=500         # Response length limit
)
```

### Document Processing

Modify chunk settings in `VectorEmbedding.py`:

```python
def split_documents(documents, chunk_size=500, chunk_overlap=100):
    # Adjust chunk_size and chunk_overlap for optimal performance
```

## 🔧 API Keys Setup

### Pinecone Setup
1. Sign up at [Pinecone](https://www.pinecone.io/)
2. Create a new project
3. Get your API key from the dashboard
4. Note your environment and index settings

### Groq Setup
1. Visit [Groq Console](https://console.groq.com/)
2. Create an account and generate an API key
3. Choose your preferred model (Llama 3.3-70B recommended)

## 🚨 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError` when running the application
```bash
# Solution: Ensure virtual environment is activated and dependencies are installed
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**Issue**: Pinecone connection errors
```bash
# Solution: Verify your API key and index configuration
# Check if the index exists in your Pinecone dashboard
```

**Issue**: No documents found
```bash
# Solution: Ensure PDFs are in the documents/ folder
mkdir documents
# Add your PDF files to this folder
python VectorEmbedding.py
```

## 📊 Performance Optimization

- **Chunk Size**: Smaller chunks (300-500 tokens) work better for specific queries
- **Retrieval Count**: Adjust `k` parameter in retriever for more/fewer source documents
- **Model Selection**: Use `llama-3.1-8b-instant` for faster responses, `llama-3.3-70b-versatile` for better quality

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) for the RAG framework
- [Groq](https://groq.com/) for fast LLM inference
- [Pinecone](https://www.pinecone.io/) for vector database
- [Gradio](https://gradio.app/) for the web interface
- [HuggingFace](https://huggingface.co/) for embedding models

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/totapakhii/issues) page
2. Create a new issue with detailed description
3. Join our community discussions

---

**Made with ❤️ by [Ashikul Islam]**

*Transform your documents into an intelligent conversational experience with TotaPakhii!*