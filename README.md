

---

<p align="center">
  <a href="https://daffo-pilot.ashiksays.com/">
    <img src="https://i.imgur.com/k6Kx07p.png" alt="TotaPakhi Logo" width="150"/>
  </a>
</p>

<h1 align="center">TotaPakhi: Full-Stack Conversational AI Platform</h1>

<p align="center">
  This repository contains the complete source code for TotaPakhi, a full-stack AI chat application. It includes a modern, responsive frontend and a powerful, high-performance backend built on a hybrid RAG architecture.
</p>

<p align-center">
  <img src="https://img.shields.io/badge/Stack-Full_Stack-blueviolet" alt="Full Stack">
  <img src="https://img.shields.io/badge/Frontend-HTML_|_CSS_|_JS-orange" alt="Frontend Tech">
  <img src="https://img.shields.io/badge/Backend-Python_|_Flask-blue.svg" alt="Backend Tech">
  <img src="https://img.shields.io/badge/LLM-Llama_3.3_@_Groq-purple.svg" alt="LLM">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
</p>

This project is a demonstration of a complete, end-to-end AI system. The **frontend** is a visually appealing, feature-rich landing page built with HTML, CSS, and JavaScript. The **backend** is a sophisticated Python Flask API that serves as the "brain," using a Retrieval-Augmented Generation (RAG) model to answer questions from a private knowledge base and from live web searches.

---

## 🎨 Frontend: The User Experience

The frontend is a static, responsive website that serves as the user-facing interface for the TotaPakhi AI agent. It is designed with a modern "glassmorphism" aesthetic and is optimized for all screen sizes.

### 🚀 Live Demo

Experience the live frontend: **[https://totapakhi.ashiksays.com/](totapakhi.ashiksays.com/)**

### Frontend Interaction Flow

The frontend code is self-contained and interacts with the backend via API calls, ensuring a clean separation of concerns.

<p align="center">
  <img src="https://i.imgur.com/o1g9DqA.png" alt="Frontend Architecture" width="800"/>
</p>

### ✨ Frontend Features

- **📱 Modern & Responsive UI:** A beautiful design that works seamlessly on desktops, tablets, and mobile devices.
- **🤖 AI Chat Interface:** An "Ask Ai Agent" button that opens a full-screen chat popup, which communicates with the backend API.
- **🧠 Data Contribution Form:** A dedicated section allowing users to submit documents to train a personalized AI assistant.
- **🎮 Classic Pong Game:** An interactive Pong game built with HTML5 Canvas for user engagement.
- **📖 Integrated Blog & Project Showcase:** Sections for articles, other projects, and a user guide.
- **🚀 Zero Dependencies:** Built with pure HTML, CSS, and Vanilla JavaScript for maximum performance and portability.

### 💻 Frontend Technology Stack

- **Structure:** HTML5
- **Styling:** CSS3 (with extensive use of Flexbox, CSS Grid, and Media Queries)
- **Interactivity:** Vanilla JavaScript
- **Form Handling:** [Formspree](https://formspree.io/)

### ▶️ Running the Frontend

To run the frontend locally, no complex setup is required:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/hey-ashik/Totapakhii_ServerFiles.git
    cd your-repository-name
    ```
2.  **Open `index.html`:**
    Simply open the `index.html` file in your web browser. For a better development experience with live reloading, you can use a tool like the **Live Server** extension in VS Code.

---

## 🧠 Backend: The Intelligence Engine

The backend is a high-performance Python server that powers the conversational AI. It implements a Hybrid RAG architecture to provide accurate, context-aware answers from multiple information sources.

### Backend RAG & File Upload Architecture

The backend's core is its ability to ingest various file types into a knowledge base and use that information to answer questions. The file "upload" is the starting point of the ingestion pipeline.

<p align="center">
  <img src="https://i.imgur.com/h5TqQ5E.png" alt="Backend RAG Architecture" width="900"/>
</p>

### ✨ Backend Features

- **🧠 Multi-Source RAG:** Answers questions using information from both a private document knowledge base (**Pinecone**) and live web searches (**Tavily**).
- **📚 Broad Document Support:** An ingestion pipeline (`VectorEmbedding.py`) that processes `.pdf`, `.docx`, `.csv`, `.xlsx`, `.pptx`, and `.txt` files.
- **🚀 High-Speed Inference:** Uses the **Groq API** for ultra-low latency responses from the **Llama 3.3** model.
- **🗣️ Conversational Memory:** Maintains chat history to understand context across multiple interactions in a single session.
- **⚡ Scalable Vector Search:** Built on **Pinecone** for efficient, production-grade semantic search.
- **🌐 RESTful API:** A well-structured **Flask API** with endpoints for chat, session management, and health checks, ready for frontend integration.

### 🛠️ Backend Technology Stack

| Category              | Technology                                                                                                  |
| --------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Backend Framework** | ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)            |
| **LLM Inference**     | ![Groq](https://img.shields.io/badge/Groq-000000?style=for-the-badge&logo=groq&logoColor=white)                |
| **Vector Database**   | ![Pinecone](https://img.shields.io/badge/Pinecone-0C51C3?style=for-the-badge&logo=pinecone&logoColor=white)    |
| **AI Framework**      | `LangChain`                                                                                                 |
| **Web Search**        | `Tavily Search API`                                                                                         |
| **Document Parsing**  | `pypdf`, `pandas`, `openpyxl`, `python-docx`, `python-pptx`                                                   |

### ▶️ Running the Backend

#### 1. Setup

1.  **Navigate to the project directory** and set up a Python virtual environment.
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure Environment Variables:** Create a `.env` file in the project root and add your API keys:
    ```env
    # .env file
    GROQ_API_KEY="your_groq_api_key"
    PINECONE_API_KEY="your_pinecone_api_key"
    PINECONE_INDEX_NAME="pdfrag"
    TAVILY_API_KEY="your_tavily_api_key"
    ```

#### 2. Usage

1.  **Ingest Your Documents:**
    - Place your files (`.pdf`, `.docx`, etc.) inside the `documents/` folder.
    - Run the ingestion script to populate your Pinecone database. You only need to do this when your documents change.
    ```bash
    python VectorEmbedding.py
    ```

2.  **Start the API Server:**
    Once your data is ingested, start the Flask server.
    ```bash
    python ServerActive.py
    ```
    The API will be available at `http://127.0.0.1:7860`.

---

## 🔗 How It All Connects

The frontend and backend are designed to work together seamlessly:

1.  The user visits the frontend website (`index.html`).
2.  Clicking the **"Ask Ai Agent"** button opens a chat modal.
3.  When the user sends a message from this modal, the frontend's JavaScript makes a `POST` request to the backend's `/api/chat` endpoint.
4.  The backend processes the request, gets an answer from the AI, and returns it as a JSON response.
5.  The frontend JavaScript receives the response and displays the AI's answer in the chat window.

## 👨‍💻 Author

This project was designed and developed by **Ashikul Islam**.

- **Facebook:** [Ashikul Islam](https://www.facebook.com/share/1YQw2j7GBS/?mibextid=wwXIfr)
- **Email:** <a href="mailto:ashikulislam2070@gmail.com">ashikulislam2070@gmail.com</a>
- **WhatsApp:** [+8801792250709](https://wa.me/+8801792250709)

## 📄 License

This project is licensed under the MIT License.
