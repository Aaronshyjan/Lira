# LIRA - LOG INTELLIGENCE & RESPONSE AGENT
**An AI-powered agent for automated incident diagnosis, classification, and resolution.**

LIRA is a state-of-the-art incident response agent designed to transform chaotic log streams into actionable intelligence. Featuring a high-performance **FastAPI** backend, a **Bento-style** real-time dashboard, and a sophisticated **n8n** workflow, LIRA provides sub-second diagnostics for enterprise infrastructure.

## 🏗️ Enterprise Tech Stack

LIRA is powered by a world-class infrastructure designed for speed and precision:
- **Core Engine**: FastAPI (Python) for asynchronous WebSocket handling.
- **AI Reasoning**: **Groq (Llama-3 70B)** for lightning-fast neural reasoning.
- **Workflow Orchestration**: **n8n v2.13+** for advanced RAG (Retrieval Augmented Generation) logic.
- **Vector Intelligence**: **Pinecone** for long-term incident memory and semantic search.
- **Local Embedding**: **Ollama (BGE-M3)** for 1024-d high-fidelity semantic vectors.
- **Status Ledger**: **Supabase** for persistent incident logging and historical recall.
- **Visual Interface**: **Vanilla JS & Tailwind CSS** for a premium, interactive "Nothing-style" dashboard.

## 🌟 Key Features

### 1. **Neural Analysis Pipeline**
Watch the machine think. LIRA visualizes every step of its process in a linear pipeline:
- **CLEAN**: Sanitization and normalization of raw log data.
- **VECTOR**: Semantic embedding and searching against Pinecone knowledge.
- **REASON**: High-speed reasoning via Groq LLM to identify root causes.

### 2. **Interactive 3D Dashboard**
A high-res, Bento-style interface featuring:
- **Neural Web Background**: An interactive Three.js particle network that reacts to your cursor.
- **System Impact Profile**: Real-time drifts in latency, error rates, and traffic patterns.
- **Anomaly Vector Map**: Visual representation of incident severity distribution.
- **Instant Ingestion**: Drop any `.txt` log file to trigger an automated diagnosis instantly.

## 🛠️ Installation & Setup

### 1. Clone & Install
```powershell
pip install -r requirements.txt
```

### 2. Configure Environment

1. Copy the template environment file:
   ```powershell
   cp .env.example .env
   ```
2. Open `.env` and fill in your API credentials:
   - **Supabase**: URL and Anon Key for persistent logging.
   - **Pinecone**: API Key for vector storage.
   - **Groq**: API Key for the Llama-3 reasoning engine.
   - **Ollama**: (Optional) For local embeddings if not using Pinecone's managed ones.

### 3. Git Setup (For Contribution/Pushing)

To prepare the repository for GitHub:
```powershell
git init
git add .
git commit -m "Initial commit: LIRA Incident Intelligence & Response Agent"
git branch -M main
# git remote add origin <your-github-repo-url>
# git push -u origin main
```
Note: Sensitive files like `.env` and large datasets (`*.csv`) are automatically ignored via `.gitignore`.

### 4. Launch LIRA
Start the FastAPI server:
```powershell
python main.py
```
Open the terminal at: **http://localhost:8000/dashboard**

👉 **[FINAL TECHNICAL REPORT](file:///c:/Users/aaron/Downloads/projects/heh/LIRA_FINAL_REPORT.md)**  
👉 **[PRESENTATION SLIDE CONTENT](file:///c:/Users/aaron/Downloads/projects/heh/LIRA_PPT_CONTENT.md)**

---
*Built for the LIRA Incident Intelligence & Response Project.*
