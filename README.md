# 🤖 RAG-Chatbot

**RAG-Chatbot** is an intelligent, LLM-powered chatbot with integrated **Retrieval-Augmented Generation (RAG)** functionality. It enables contextual, knowledge-grounded conversations powered by **FastAPI**, **Hugging Face Transformers**, **Mistral-7B**, and **ChromaDB**.

---

## 🚀 Features

- ✅ **RAG Integration:** Combines document retrieval via ChromaDB with language generation from Mistral-7B.
- 💬 **Chat API:** Interact with the bot via a simple RESTful API.
- ⚡ **Mistral-7B:** Generates coherent, high-quality language responses.
- 🔧 **FastAPI Backend:** High-performance API server for LLM inference.
- 🧠 **Transformers:** Uses Hugging Face Transformers for model management.
- 📚 **ChromaDB:** Embedded vector store for fast and efficient retrieval.

---

## 🛠️ Tech Stack

| Tech         | Role                                             |
|--------------|--------------------------------------------------|
| FastAPI      | Backend API server                              |
| Hugging Face | Transformer models                              |
| Mistral-7B   | Language generation                             |
| ChromaDB     | Vector database for document retrieval          |
| Docker       | Containerization for consistent deployment      |

---

## 🧪 Getting Started

### Prerequisites

- Python 3.8+
- Docker & Docker Compose (for containerized deployment)
- GPU (recommended) or CPU with sufficient memory
- Ollama (recommended for faster responses)

### Run Directly

```bash
git clone https://github.com/your-username/RAG-Chatbot.git
cd RAG-Chatbot
pip install -r requirements.txt
uvicorn app:app --reload
```
### Run using Docker
```bash
git clone https://github.com/your-username/RAG-Chatbot.git
cd RAG-Chatbot
docker build -t rag_chatbot .
docker run -p 7860:7860 rag_chatbot
```


### Note
The deployed version of this app does not use ollama and Mistral-7B instead microsoft phi-2 model is used via llama-cpp-python library due to platform constraints. \
The deployed code is given with file name `run_model_hf.py`.
**Migration to Microsoft Azure for better performance and less constraints is underway.**

