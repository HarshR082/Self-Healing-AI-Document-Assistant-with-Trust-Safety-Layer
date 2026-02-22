# 🚀 Self-Healing RAG Document Intelligence System

Welcome to the **Self-Healing RAG Document Intelligence System** — an enterprise-grade AI assistant that transforms documents into **reliable, explainable insights**.

This platform combines **Retrieval-Augmented Generation (RAG)**, trust-aware AI safeguards, and adaptive intelligence to deliver accurate, safe, and context-aware responses from uploaded documents.

---

## 🧠 Why This Project?

Traditional AI assistants may hallucinate or provide unreliable answers.

This system introduces:

✅ Grounded document intelligence  
✅ Trust & safety enforcement  
✅ Self-healing AI responses  
✅ Adaptive learning & optimization  
✅ Enterprise-ready reliability  

---

## ✨ Core Features

### 📄 Document Intelligence
- Upload PDF/TXT documents  
- Automatic document understanding & summarization  
- Multi-document memory & contextual retrieval  

### 💬 Context-Aware Q&A
- Retrieval-Augmented Generation (RAG)  
- Context grounding with document excerpts  
- Follow-up question support with memory  

### 🛡 Trust & Safety Layer
- Hallucinaton detection  
- Risk classification & confidence scoring  
- Unsupported sentence highlighting  
- Self-healing response correction  

### ⚡ Adaptive Intelligence
- Semantic caching for instant repeat responses  
- Prompt optimization for improved accuracy  
- Feedback-driven learning loop  
- Knowledge gap detection  

### 🔍 Explainability & Transparency
- Source-grounded responses  
- Trust & quality indicators  
- Snippet-level justification  

### ☁️ Cloud Deployment
- Hosted on AWS EC2  
- Real-time AI inference  
- Accessible via web interface  

---

## 🏗 Architecture Overview

User Query
↓
Semantic Cache ⚡
↓
Intent Detection
↓
Vector Retrieval (ChromaDB)
↓
LLM Generation (Groq LLaMA 3)
↓
Trust & Safety Layer
↓
Self-Healing Logic
↓
Adaptive Learning Loop
↓
Response

## 🛠 Technology Stack

| Technology | Purpose |
|------------|---------|
| **FastAPI** | Backend & AI pipeline orchestration |
| **LangChain** | RAG workflow & LLM integration |
| **ChromaDB** | Vector storage & semantic retrieval |
| **HuggingFace Embeddings** | Document vectorization |
| **Groq LLaMA 3** | Ultra-fast LLM inference |
| **Streamlit** | Interactive user interface |
| **AWS EC2** | Cloud deployment |
| **Python** | Core development |

---

## ⚙️ Local Setup

### 1️⃣ Clone Repository
```bash
git clone https://github.com/yourusername/project-name.git
cd project-name

###2️⃣ Create Virtual Environment
```bash
python -m venv venv

Activate:

Windows
```bash
venv\Scripts\activate
```bash
Mac/Linux

source venv/bin/activate
###3️⃣ Install Dependencies
```bahs
pip install -r requirements.txt
###4️⃣ Configure API Key
```bash
Create a .env file:

GROQ_API_KEY=your_api_key_here
###5️⃣ Run Backend
```bash
uvicorn api:app --reload
###6️⃣ Launch Interface
``` bash
streamlit run app.py
```
