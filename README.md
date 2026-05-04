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
