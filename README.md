# DocuMind AI - Multi-Agent Document Intelligence System

A production-grade GenAI system that ingests documents, creates embeddings, performs intelligent retrieval, and uses multiple specialized AI agents to answer complex questions with citations and fact-checking.

## 🎯 Project Status

**Current Stage:** Week 1 - Foundation Setup  
**Last Updated:** Day 1

## 📁 Project Structure

```
documind-ai/
├── app/                    # Main application code
│   ├── api/               # API routes and schemas
│   ├── core/              # Core functionality (RAG, agents, LLM)
│   ├── services/          # Business logic services
│   └── models/            # Database models
├── ingestion/             # Document processing pipeline
├── tests/                 # Test files
├── scripts/               # Utility scripts
├── docker/                # Docker configuration
└── docs/                  # Documentation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Virtual environment (venv)
- Google Gemini API key

### Setup

1. **Activate virtual environment:**
   ```bash
   D:\AI_Agent_DocuMind\venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   (We'll create this in Day 2)

3. **Create `.env` file:**
   ```bash
   cp .env.example .env
   ```
   Then add your actual API keys.

## 📚 Learning Resources

- **Git Workflow:** See `docs/git-workflow.md`
- **ChatGPT Learning Prompt:** See `docs/chatgpt-learning-prompt.md`
- **Project Plan:** See `multi-agent-document-intelligence-system.plan.md`

## 🗓️ Daily Progress

- **Day 1:** Project structure setup, config.py, Gemini client wrapper

## 🎓 Learning Goals

This project is designed for learning by building. Each day focuses on:
- Understanding concepts deeply
- Building production-quality code
- Preparing for technical interviews

## 📝 Notes

- This is a learning project - code may be incomplete as we build
- Daily commits to GitHub to track progress
- Focus on understanding, not just completion

---

**Built with:** Python, FastAPI, Google Gemini API, ChromaDB, CrewAI

