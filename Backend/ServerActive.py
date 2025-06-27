# --- START OF FILE hello19.py ---

import os
from pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_pinecone import PineconeVectorStore
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.schema import HumanMessage, AIMessage
from langchain.prompts import PromptTemplate
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import uuid
from datetime import datetime
import requests
import json
import re # <-- Added this import at the top

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Flask app initialization
app = Flask(__name__)
application = app

# --- CHANGE 1: More flexible CORS configuration ---
# Allows requests from your public domain and localhost for testing.
CORS(app, origins=["https://chat.ashikai.xyz", "http://127.0.0.1:7860", "http://localhost:7860"])

# API Keys Configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "pdfrag")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Initialize Pinecone only if key is provided
pc = None
if PINECONE_API_KEY:
    try:
        pc = Pinecone(api_key=PINECONE_API_KEY)
        print("✅ Pinecone initialized successfully")
    except Exception as e:
        print(f"❌ Pinecone initialization failed: {e}")

# Define the embedding model for similarity search
embedding_model = 'sentence-transformers/all-MiniLM-L6-v2'

# Initialize HuggingFace Embeddings model
embeddings = HuggingFaceEmbeddings(model_name=embedding_model)

# Initialize Groq LLM
llm = None
if GROQ_API_KEY:
    try:
        llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name="llama-3.3-70b-versatile",
            temperature=0.5,
            max_tokens=500
        )
        print("✅ Groq LLM initialized successfully")
    except Exception as e:
        print(f"❌ Groq LLM initialization failed: {e}")

# Global chat history storage
chat_sessions = {}

def load_vector_store():
    """Load the Pinecone vector store."""
    if not PINECONE_API_KEY:
        print("❌ Pinecone API key not configured")
        return None
        
    if not pc:
        print("❌ Pinecone client not initialized")
        return None
        
    print(f"Looking for Pinecone index '{PINECONE_INDEX_NAME}'")
    
    try:
        # Get the Pinecone index
        index = pc.Index(PINECONE_INDEX_NAME)
        
        # Create LangChain vector store from Pinecone index
        vector_store = PineconeVectorStore(
            index=index,
            embedding=embeddings
        )
        
        print(f"✅ Vector store '{PINECONE_INDEX_NAME}' loaded successfully.")
        return vector_store
    except Exception as e:
        print(f"❌ Error loading Pinecone index: {e}")
        return None

def create_conversational_qa_chain(vector_store):
    """Create a conversational question-answering chain with memory."""
    if not llm:
        print("❌ LLM not available for conversational chain")
        return None
        
    try:
        # Create retriever from vector store
        retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        )
        
        # Create Conversational Retrieval Chain
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            return_source_documents=True,
            verbose=False,
            max_tokens_limit=4000
        )
        
        return qa_chain
    except Exception as e:
        print(f"❌ Error creating Conversational QA chain: {e}")
        return create_qa_chain(vector_store)

def create_qa_chain(vector_store):
    """Create a question-answering chain (fallback)."""
    if not llm:
        print("❌ LLM not available for QA chain")
        return None
        
    try:
        # Create retriever from vector store
        retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        )
        
        # Create QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )
        
        return qa_chain
    except Exception as e:
        print(f"❌ Error creating QA chain: {e}")
        return None

def tavily_web_search(query, max_results=3):
    """Perform web search using Tavily API."""
    if not TAVILY_API_KEY:
        return None, "Tavily API key not configured"
    
    try:
        url = "https://api.tavily.com/search"
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "advanced",
            "include_answer": True,
            "include_raw_content": False,
            "max_results": max_results,
            "include_domains": [],
            "exclude_domains": []
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            return data, None
        else:
            return None, f"Tavily API error: {response.status_code} - {response.text}"
            
    except requests.exceptions.Timeout:
        return None, "Web search timeout"
    except Exception as e:
        return None, f"Web search error: {str(e)}"

def format_web_search_response(search_data, original_query):
    """Format web search results into a coherent response."""
    if not search_data:
        return "No web search results found.", []
    
    # Get the answer from Tavily if available
    answer = search_data.get('answer', '')
    results = search_data.get('results', [])
    
    # If no direct answer, create one from results
    if not answer and results and llm:
        # Use LLM to synthesize an answer from search results
        context = "\n\n".join([f"Source: {r.get('title', 'Unknown')}\nContent: {r.get('content', '')[:300]}..." 
                              for r in results[:3]])
        
        prompt = f"""Based on the following web search results, provide a comprehensive answer to the question: "{original_query}"

Search Results:
{context}

Please provide a clear, informative answer based on these sources. If the information is insufficient, mention that."""

        try:
            llm_response = llm.invoke(prompt)
            answer = llm_response.content if hasattr(llm_response, 'content') else str(llm_response)
        except Exception as e:
            print(f"❌ Error generating LLM response from web results: {e}")
            answer = "Found relevant web results, but couldn't generate a comprehensive answer."
    
    # Format sources for display
    sources = []
    for i, result in enumerate(results[:3]):
        title = result.get('title', 'Unknown Source')
        url = result.get('url', '')
        content = result.get('content', '')[:200]
        if len(result.get('content', '')) > 200:
            content += "..."
        
        source_info = f"**{title}**\n{content}\n🔗 {url}"
        sources.append([f"Web Source {i+1}", source_info])
    
    return answer, sources

def query_pdfs_with_context(query, session_id=None):
    """Query the Pinecone vector database with conversation context."""
    if not query.strip():
        return "Please enter a question.", [], "pdf"
    
    # Check if services are available
    if not llm:
        return ("Service Unavailable: Groq API key not configured. Please set your GROQ_API_KEY environment variable.", 
                [], "pdf")
    
    # Try PDF search
    vector_store = load_vector_store()
    
    if vector_store is None:
        return ("Knowledge Base Unavailable: I couldn't access the knowledge base at the moment. Please try using web search.", 
                [], "pdf")
    
    # Create Conversational QA chain
    qa_chain = create_conversational_qa_chain(vector_store)
    
    if qa_chain is None:
        return ("Knowledge Base Unavailable: I couldn't create the QA chain for the knowledge base. Please try using web search.", 
                [], "pdf")
    
    try:
        # Prepare chat history for context
        chat_history = []
        if session_id and session_id in chat_sessions:
            session_data = chat_sessions[session_id]
            if session_data.get('messages'):
                for human_msg, ai_msg in session_data['messages']:
                    chat_history.extend([
                        HumanMessage(content=human_msg),
                        AIMessage(content=ai_msg)
                    ])
        
        # Perform the query with context
        response = qa_chain.invoke({"question": query, "chat_history": chat_history})
        
        # Get the answer from response
        answer = response.get('answer', response.get('result', ''))
        source_docs = response.get('source_documents', [])
        
        # Check if the answer is meaningful
        is_meaningful = (
            answer and len(answer.strip()) > 10 and 
            not any(phrase in answer.lower() for phrase in [
                "i don't know", "i cannot", "no information", "not found", 
                "unable to answer", "cannot find", "no relevant information"
            ])
        )
        
        if is_meaningful and source_docs:
            sources = []
            if source_docs:
                top_sources = source_docs[:2]
                for i, doc in enumerate(top_sources):
                    page_number = None
                    if hasattr(doc, 'metadata') and doc.metadata:
                        page_number = (doc.metadata.get('page') or 
                                     doc.metadata.get('page_number') or 
                                     doc.metadata.get('source_page') or 
                                     doc.metadata.get('page_label'))
                    
                    if not page_number and hasattr(doc, 'metadata') and doc.metadata.get('source'):
                        source_info = doc.metadata.get('source', '')
                        page_match = re.search(r'page[_\s]*(\d+)', source_info.lower())
                        if page_match:
                            page_number = page_match.group(1)
                    
                    if not page_number:
                        page_number = f"PDF Source {i + 1}"
                    else:
                        page_number = f"Page {page_number}"
                    
                    snippet = doc.page_content[:200].strip() + "..."
                    sources.append([str(page_number), snippet])
            
            # --- MODIFIED PART ---
            # Return the raw answer, not the formatted string
            return answer, sources, "pdf"
        
        else:
            # --- MODIFIED PART ---
            return ("I couldn't find relevant information in the knowledge base for your question. Try using the web search.", 
                    [], "pdf")
        
    except Exception as e:
        print(f"❌ Error during PDF query: {e}")
        # --- MODIFIED PART ---
        return ("Knowledge Base Error: There was an error accessing the knowledge base. Please try using web search.", 
                [], "pdf")

def query_web_search(query):
    """Query web search only."""
    if not query.strip():
        return "Please enter a question.", [], "web"
    
    print("🌐 Performing web search...")
    search_data, error = tavily_web_search(query)
    
    if error:
        # --- MODIFIED PART ---
        return f"Web Search Failed: {error}", [], "web"
    
    answer, sources = format_web_search_response(search_data, query)
    # --- MODIFIED PART ---
    # Return the raw answer from the web search
    return answer, sources, "web"

def get_demo_response(query):
    """Provide demo responses when APIs are not configured."""
    demo_responses = {
        "hello": "Hello! This is a demo response. To get full functionality, please configure your API keys.",
        "how are you": "I'm doing well! This chatbot can answer questions from PDFs and web search when properly configured.",
        "what can you do": "I can help you with:\n• Answering questions from PDF documents\n• Web searches for current information\n• Maintaining conversation context\n\nPlease configure your API keys for full functionality."
    }
    
    query_lower = query.lower()
    for key, response in demo_responses.items():
        if key in query_lower:
            return response, [], "demo"
    
    # --- MODIFIED PART ---
    return ("Demo Mode: This is a demo response. To enable full functionality, set your GROQ, Pinecone, and Tavily API keys.", 
            [], "demo")

# Flask Routes
@app.route('/')
def index():
    """Serve the main interface."""
    try:
        # Make sure you have a 'templates' folder with 'index.html' inside.
        return render_template('index.html')
    except Exception as e:
        print(f"Error rendering template: {e}")
        return "<h1>Error</h1><p>Could not find the index.html template. Make sure it's in a 'templates' folder.</p>", 500

@app.route('/api/chat', methods=['POST'])
def chat_api():
    """Handle chat messages from the frontend."""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        search_type = data.get('type', 'pdf')
        session_id = data.get('session_id')
        
        if not message:
            return jsonify({'success': False, 'error': 'Empty message'}), 400
        
        if not session_id or session_id not in chat_sessions:
            session_id = str(uuid.uuid4())[:8]
            chat_sessions[session_id] = {
                'title': 'New Chat',
                'messages': [],
                'created_at': datetime.now().strftime("%H:%M"),
                'context_memory': []
            }
        
        # --- ENTIRE LOGIC BLOCK MODIFIED ---

        # 1. Get raw content, sources, and type from the appropriate function
        if search_type == 'web':
            if TAVILY_API_KEY:
                raw_content, sources, result_type = query_web_search(message)
            else:
                raw_content, sources, result_type = get_demo_response(message)
        else:
            if GROQ_API_KEY and PINECONE_API_KEY:
                raw_content, sources, result_type = query_pdfs_with_context(message, session_id)
            else:
                raw_content, sources, result_type = get_demo_response(message)
        
        # 2. Determine the prefix based on the result type
        prefix = ""
        if result_type == "pdf":
            # Check if it's a success or an error/fallback message
            if sources:
                 prefix = "📄 From Knowledge Base:"
            else:
                 prefix = "📄 Knowledge Base:" # A simpler prefix for notifications
        elif result_type == "web":
            prefix = "🌐 Web Search Results:"
        elif result_type == "demo":
            prefix = "🤖 Demo Mode:"

        # 3. Combine prefix and content, then clean the Markdown
        # This is the key fix: .replace('**', '') removes the bolding characters.
        full_response_markdown = f"{prefix}\n\n{raw_content}"
        final_answer = full_response_markdown.replace('**', '')

        # 4. Update session with the cleaned, final answer
        session = chat_sessions[session_id]
        session['messages'].append([message, final_answer])
        
        if len(session['messages']) == 1:
            session['title'] = message[:30] + ("..." if len(message) > 30 else "")
        
        if 'context_memory' not in session:
            session['context_memory'] = []
        
        session['context_memory'].append({
            'question': message,
            'answer': final_answer,
            'search_type': result_type,
            'timestamp': datetime.now().isoformat()
        })
        
        # 5. Return the cleaned answer in the JSON response
        return jsonify({
            'success': True,
            'answer': final_answer, # Sending the cleaned answer
            'sources': sources,
            'session_id': session_id,
            'search_type': result_type
        })
        
    except Exception as e:
        print(f"❌ Error in chat API: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ... (rest of your Flask routes are fine) ...
@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    """Get all chat sessions."""
    try:
        sessions_list = []
        for session_id, session_data in reversed(list(chat_sessions.items())):
            sessions_list.append({
                'id': session_id,
                'title': session_data['title'],
                'created_at': session_data['created_at'],
                'message_count': len(session_data['messages'])
            })
        
        return jsonify({
            'success': True,
            'sessions': sessions_list
        })
        
    except Exception as e:
        print(f"❌ Error getting sessions: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/sessions/<session_id>', methods=['GET'])
def get_session(session_id):
    """Get a specific chat session."""
    try:
        if session_id not in chat_sessions:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        session = chat_sessions[session_id]
        return jsonify({
            'success': True,
            'session': {
                'id': session_id,
                'title': session['title'],
                'messages': session['messages'],
                'created_at': session['created_at']
            }
        })
        
    except Exception as e:
        print(f"❌ Error getting session: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/sessions', methods=['DELETE'])
def clear_sessions():
    """Clear all chat sessions."""
    try:
        global chat_sessions
        chat_sessions = {}
        
        return jsonify({
            'success': True,
            'message': 'All sessions cleared'
        })
        
    except Exception as e:
        print(f"❌ Error clearing sessions: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/sessions/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    """Delete a specific chat session."""
    try:
        if session_id in chat_sessions:
            del chat_sessions[session_id]
        
        return jsonify({
            'success': True,
            'message': 'Session deleted'
        })
        
    except Exception as e:
        print(f"❌ Error deleting session: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Health check endpoint
@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'groq': bool(GROQ_API_KEY),
            'pinecone': bool(PINECONE_API_KEY),
            'tavily': bool(TAVILY_API_KEY)
        },
        'features': {
            'pdf_search': bool(GROQ_API_KEY and PINECONE_API_KEY),
            'web_search': bool(TAVILY_API_KEY),
            'chat_sessions': True,
            'conversation_memory': True
        }
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == "__main__":
    print("🚀 Starting AI ChatBot Flask Server...")
    print("=" * 50)
    
    # Check API key configuration
    print("📋 Configuration Status:")
    print(f"   • Groq API: {'✅ Configured' if GROQ_API_KEY else '❌ Not Configured'}")
    print(f"   • Pinecone API: {'✅ Configured' if PINECONE_API_KEY else '❌ Not Configured'}")
    print(f"   • Tavily API: {'✅ Configured' if TAVILY_API_KEY else '❌ Not Configured'}")
    
    print("\n🔧 Available Features:")
    print(f"   • PDF Search: {'✅ Enabled' if (GROQ_API_KEY and PINECONE_API_KEY) else '❌ Disabled'}")
    print(f"   • Web Search: {'✅ Enabled' if TAVILY_API_KEY else '❌ Disabled'}")
    print(f"   • Chat Sessions: ✅ Enabled")
    print(f"   • Conversation Memory: ✅ Enabled")
    
    if not any([GROQ_API_KEY, PINECONE_API_KEY, TAVILY_API_KEY]):
        print("\n⚠️  Demo Mode: No API keys configured")
        print("   The chatbot will run in demo mode with limited functionality.")
    
    print("\n🌐 Server Information:")
    print(f"   • URL: http://127.0.0.1:7860")
    print(f"   • Health Check: http://127.0.0.1:7860/health")
    print(f"   • LLM Model: llama-3.3-70b-versatile")
    print(f"   • Embedding Model: sentence-transformers/all-MiniLM-L6-v2")
    
    print("\n" + "=" * 50)
    print("Press CTRL+C to quit")
    
    # --- CHANGE 2: Run the server on 0.0.0.0 for better accessibility ---
    app.run(debug=False, host='0.0.0.0', port=7860)