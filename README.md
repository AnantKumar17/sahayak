# Sahayak - A GenAI-Powered Context-Aware Code Reviewer

## Overview

Sahayak is an AI-powered code review assistant designed to enhance software quality by providing context-aware, actionable feedback. Leveraging a fine-tuned Large Language Model (GPT-4o), Retrieval-Augmented Generation (RAG), and FAISS for efficient similarity search, Sahayak integrates seamlessly into developer workflows via a VS Code extension and a web dashboard. It analyzes code for anti-patterns, security vulnerabilities, and inefficiencies, offering refactoring suggestions with interactive explanations. GitHub PR comment integration ensures alignment with project-specific guidelines, reducing manual review effort and standardizing code quality.

## Features

- **Automated Code Review**: Context-aware analysis using past commits, documentation, and best practices
- **Refactoring Suggestions**: Detects anti-patterns and proposes structured improvements
- **Interactive Explanations**: Justifications for suggestions with support for follow-up queries
- **Web Dashboard**: Tracks AI suggestions, trends, and recurring issues (Next.js + FastAPI)
- **VS Code Extension**: Real-time inline feedback within the IDE
- **GitHub Integration**: Fetches PR comments for enhanced context

## Installation and Setup

### Requirements

#### Hardware Requirements

- **Processor**: Intel Core i5 (9th Gen, 2.4 GHz, 4 cores) or equivalent
- **RAM**: 8 GB DDR4 (2666 MHz)
- **Storage**: 512 GB SSD

#### Software Requirements

- **Python**: 3.8 or higher
- **Node.js**: 16.x or higher
- **VS Code**: Latest version
- **Git**: For cloning repositories and GitHub integration

#### Dependencies

- **Python**: FastAPI, Uvicorn, SQLite, FAISS, BAAI-BGE3, OpenAI SDK
- **Node.js**: Next.js, React, TypeScript
- **Others**: Azure account for GPT-4o access, GitHub Personal Access Token (PAT) to fetch PR comments for enhanced context-aware reviews.

### Installation Steps

#### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/sahayak.git
cd sahayak
```

#### 2. Backend Setup (FastAPI)

Navigate to the backend directory:
```bash
cd backend
```

Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:
```bash
pip install fastapi uvicorn sqlite3 faiss-cpu sentence-transformers openai
```

Configure environment variables (e.g., Azure GPT-4o API key, GitHub PAT) in a `.env` file:
```env
AZURE_OPENAI_API_KEY=your_azure_key
GITHUB_PAT=your_github_token
```

#### 3. Frontend Setup (Next.js)

Navigate to the frontend directory:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
```

Ensure Node.js and npm are installed (`node -v`, `npm -v`).

#### 4. VS Code Extension Setup

Navigate to the extension directory:
```bash
cd vscode-extension
```

Install dependencies:
```bash
npm install
```

Install VS Code Extension Development tools:
```bash
npm install -g yo generator-code
```

#### 5. Database Setup

SQLite is used for storing reviews. Initialize the database:
```bash
python backend/init_db.py  # Create SQLite database if script provided
```

#### 6. FAISS and BAAI-BGE3 Setup

Ensure FAISS and BAAI-BGE3 are installed via backend dependencies. Preload embeddings for past reviews (if applicable, run provided script):
```bash
python backend/preload_embeddings.py
```

## Running the Application

### Backend (FastAPI)

Start the backend server:
```bash
cd backend
uvicorn main:app --reload
```

Access the API at `http://localhost:8000`.

### Frontend (Next.js)

Start the frontend development server:
```bash
cd frontend
npm start
```

Access the dashboard at `http://localhost:3000`.

### VS Code Extension

Compile the extension:
```bash
cd vscode-extension
npm run compile
```

Run the extension in VS Code:
1. Open VS Code
2. Press `Cmd+Shift+P` (or `Ctrl+Shift+P` on Windows/Linux)
3. Select **Run Extension** or **Launch Extension** to test in a development environment

To package for distribution:
```bash
npm run package
```

## Usage

- **VS Code Extension**: Open a code file, select a snippet, activate Sahayak via the extension, and optionally provide a GitHub PR number for context. Review AI suggestions inline and ask follow-up questions.
- **Web Dashboard**: Upload a code snippet, enter a PR number (if applicable), view AI-generated reviews, get refactored code, ask follow-up questions and analyse similarity graphs.

## Project Structure

```
sahayak/
├── backend/           # FastAPI backend (main.py, API logic)
├── frontend/          # Next.js frontend (dashboard)
├── vscode-extension/  # VS Code extension (TypeScript)
├── docs/              # Documentation
└── README.md
```

## Contributing

Contributions are welcome! Please submit issues or pull requests to the repository. Ensure code adheres to project-specific coding standards, as Sahayak itself can review contributions.

## Acknowledgments

- **Supervisor**: Mr. Arun Srinivasan, SAP Labs
- **Institution**: Birla Institute of Technology and Science, Pilani
- **Open-source communities**: FAISS, BAAI-BGE3, OpenAI, and more