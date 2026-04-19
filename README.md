# Sahayak — A GenAI-Powered Context-Aware Code Reviewer

> **M.Tech Dissertation Project** — BITS Pilani &nbsp;|&nbsp; SAP Labs, Bangalore  
> **Author:** Anant Kumar (2023SL93065) &nbsp;|&nbsp; **Supervisor:** Mr. Arun Srinivasan, Senior Developer, SAP

---

## Overview

Sahayak is an LLM-powered AI pair programmer that provides **context-aware code reviews and structured refactoring suggestions**. Unlike static analysis tools (SonarQube, ESLint) or completion-focused assistants (GitHub Copilot), Sahayak integrates **Retrieval-Augmented Generation (RAG)** to ground its feedback in your project's actual history — past code reviews, commit context, and GitHub PR comments.

The result: actionable, explainable feedback tailored to your codebase, delivered inside VS Code or a web dashboard — without disrupting your existing workflow.

---

## Key Features

| Feature | Description |
|---|---|
| **Context-Aware Code Review** | Analyses code against past reviews, architecture docs, and team conventions via RAG |
| **Refactoring Suggestions** | Detects anti-patterns, redundant code, and inefficiencies with structured improvements |
| **Interactive Explanations** | Every suggestion includes a justification; developers can ask follow-up questions |
| **Web Dashboard** | Track AI suggestions, monitor trends, and review accepted/rejected changes |
| **VS Code Extension** | Real-time inline reviews without leaving the IDE |
| **GitHub PR Integration** | Fetches historical PR comments to align suggestions with past team decisions |
| **FAISS Similarity Search** | Retrieves semantically similar past reviews for context-enriched feedback |

---

## How It Works

```
Developer submits code snippet (VS Code extension or web dashboard)
        ↓
Code is embedded → matched against past reviews using FAISS
        ↓
RAG system retrieves relevant past reviews + GitHub PR comments
        ↓
GPT-4o processes enriched prompt → generates structured review
        ↓
Output: readability / security / performance / bugs / refactored code
        ↓
Developer interacts: asks follow-up questions → AI responds contextually
        ↓
Review stored in SQLite → visible on web dashboard for trend analysis
```

---

## Comparison with Existing Tools

| Feature | SonarQube | ESLint | GitHub Copilot | **Sahayak** |
|---|---|---|---|---|
| Primary function | Static analysis | JS/TS linting | Code completion | AI-powered context-aware review |
| Context awareness | No | No | Limited | Yes (RAG-based) |
| AI-powered suggestions | No | No | Yes (completion) | Yes (review + refactoring) |
| Explanation of suggestions | No | No | No | Yes — interactive |
| Learns from past reviews | No | No | No | Yes — via FAISS + GitHub |
| Refactoring recommendations | No | No | No | Yes — structured |
| IDE integration | Limited | Yes | Yes | Yes (VS Code) |

---

## Architecture

### Core Components

- **VS Code Extension** — triggers reviews inline; supports follow-up questions
- **FastAPI Backend** — handles requests, orchestrates AI inference and RAG pipeline
- **GPT-4o (hosted on Azure)** — generates review comments and refactored code
- **RAG System** — retrieves relevant documentation and past reviews for context
- **FAISS Vector Store** — semantically indexes past code reviews using BAAI/BGE-3 embeddings
- **React Frontend (web dashboard)** — visualises reviews, trends, and adoption metrics
- **SQLite** — stores AI-generated reviews and interaction history
- **GitHub API Integration** — fetches PR comments for a given PR number on demand

### Data Flow

1. User submits a code snippet (optionally with a GitHub PR number)
2. Snippet is embedded via BAAI/BGE-3 and matched with past reviews using FAISS
3. RAG retrieves relevant reviews and GitHub PR comments
4. GPT-4o generates a structured JSON review covering readability, security, performance, bugs, and a refactored version
5. Response is returned to the IDE / dashboard and stored in SQLite

---

## Tech Stack

| Layer | Technology |
|---|---|
| AI Model | GPT-4o (Azure-hosted) |
| Embeddings | BAAI/BGE-3 |
| Vector Store | FAISS |
| Backend | Python, FastAPI |
| Frontend | React (TypeScript) |
| VS Code Extension | TypeScript |
| Database | SQLite |
| AI Inference | Azure AI ChatCompletionsClient |

---

## Installation and Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- VS Code (latest)
- Git
- Azure account (for GPT-4o access)
- GitHub Personal Access Token (PAT) — to fetch PR comments

### 1. Clone the Repository

```bash
git clone https://github.com/AnantKumar17/sahayak.git
cd sahayak
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Copy the environment template and fill in your values:

```bash
cp services/.env.example services/.env
```

```env
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_REPO=AnantKumar17/sahayak
```

Start the backend:

```bash
uvicorn main:app --reload
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm start
```

### 4. VS Code Extension

```bash
cd sahayak-vscode
npm install
```

Press **F5** in VS Code to launch the extension in a development host window.

---

## Project Structure

```
sahayak/
├── backend/
│   ├── main.py                      # FastAPI entry point
│   ├── requirements.txt
│   └── services/
│       ├── gpt_api.py               # GPT-4o inference + prompt engineering
│       ├── rag_storage.py           # FAISS indexing + RAG retrieval
│       ├── github_reviews.py        # GitHub PR comment fetcher
│       └── .env.example             # Environment variable template
├── frontend/                        # React dashboard (TypeScript)
├── sahayak-vscode/                  # VS Code extension (TypeScript)
│   └── src/extension.ts
├── test-files/                      # Sample code snippets for testing
└── .gitignore
```

---

## Review Output Format

Sahayak returns a structured JSON response for each review:

```json
{
  "readability": "...",
  "security": "...",
  "performance": "...",
  "best practices": "...",
  "bugs": "...",
  "overall analysis": "...",
  "suggested refactored code": "..."
}
```

---

## Research Context (Dissertation)

This project was developed at **SAP Labs, Bangalore** as part of the M.Tech Software Engineering dissertation at BITS Pilani (2024–25).

**Key research contributions:**
- Demonstrates that RAG-enhanced LLM feedback reduces hallucinations by grounding responses in project-specific historical data
- Shows measurable improvement in review cycle time vs. manual-only reviews
- Validates GPT-4o as viable for structured, explainable code quality analysis
- Explores FAISS + BAAI/BGE-3 for efficient semantic retrieval of past code reviews

**Keywords:** AI-powered code review, LLM, Retrieval-Augmented Generation (RAG), Context-Aware Refactoring, Software Quality, Developer Productivity, GenAI, IDE Integration, Full-Stack Development
