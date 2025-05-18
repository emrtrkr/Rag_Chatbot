# RAG Chatbot

A Streamlit-based Retrieval-Augmented Generation (RAG) chatbot that answers user questions **only** from the content of uploaded PDF or Word documents. Perfect for sharing knowledge bases, company manuals, or any text collection without exposing external web data.

---

## 🚀 Features

- **Document Upload**  
  Upload one or more PDF/DOCX files; the app automatically extracts, chunks, and indexes their text.

- **Custom Prompting**  
  Edit the system prompt on-the-fly to guide the assistant’s tone, style, and response format.

- **Interactive Chat UI**  
  Ask questions and get answers in a clean chat interface powered by Streamlit’s built-in components.

- **Vector Store**  
  Uses a local Chroma (or FAISS) vector database to store embeddings for fast, context-aware retrieval.

- **OpenAI Integration**  
  Plug in any OpenAI model (e.g. GPT-4) via your own API key. No hard-coded secrets.

---

## 📦 Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/<your-username>/rag_chatbot.git
   cd rag_chatbot
