# Contributing to Sahayak

👋 Thanks for your interest in contributing to Sahayak — an AI-powered code review assistant!

## How to Contribute

We welcome contributions that improve Sahayak's code review capabilities, RAG system, or developer experience. Here's what we're looking for:

### 1. Bug Reports & Feature Requests
- Check existing [issues](https://github.com/AnantKumar17/sahayak/issues) first to avoid duplicates
- For bugs: include steps to reproduce, expected vs actual behavior, and environment details
- For features: explain the use case and why it would benefit code review workflows

### 2. Code Contributions

**We accept:**
- Small, focused patches that are easy to review manually
- Prompts you used to generate LLM-based changes (with evidence of manual testing)
- Documentation improvements and README updates
- New test cases (hand-written tests preferred)

**Please avoid:**
- Large, unreviewed LLM-generated patches
- Changes without testing evidence
- LLM-generated tests without manual verification

### 3. Testing Requirements

All contributions must include evidence of testing:
- For **VS Code extension**: test in VS Code development host, show screenshots/videos
- For **Backend API**: test API endpoints with sample code snippets, include request/response examples
- For **Frontend dashboard**: test UI flows, verify charts and visualizations render correctly
- For **RAG system**: verify FAISS retrieval quality, test with various code samples

## Development Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- VS Code (for extension development)
- Azure account (for GPT-4o access)
- GitHub Personal Access Token

### Installation

```bash
git clone https://github.com/AnantKumar17/sahayak.git
cd sahayak

# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp services/.env.example services/.env
# Edit services/.env with your GITHUB_TOKEN and GITHUB_REPO

# Frontend
cd ../frontend
npm install

# VS Code Extension
cd ../sahayak-vscode
npm install
# Press F5 in VS Code to launch development host
```

### Running Tests

```bash
# Backend tests
cd backend
pytest tests/ -v

# Frontend tests
cd frontend
npm test

# VS Code extension
cd sahayak-vscode
npm test
```

## Contribution Guidelines

### Code Style
- **Python**: Follow PEP 8, use type hints
- **TypeScript/JavaScript**: Use ESLint configuration in the repo
- **React**: Functional components with hooks
- Keep functions focused and well-named

### Commit Messages
- Use present tense ("Add feature" not "Added feature")
- Keep first line under 70 characters
- Reference issue numbers when applicable

### Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes with clear commits
4. Test thoroughly (see Testing Requirements above)
5. Update documentation if needed
6. Submit PR with:
   - Clear description of what changed and why
   - Evidence of testing (screenshots, logs, test output)
   - If LLM-generated: include the prompts used

### What to Include in Your PR

- **Description**: What problem does this solve? What's the approach?
- **Testing evidence**: Screenshots, terminal output, or video demos
- **Breaking changes**: Clearly mark if any APIs or interfaces changed
- **Documentation**: Update README.md if user-facing changes

## Areas We Need Help With

Check the [issues page](https://github.com/AnantKumar17/sahayak/issues) for backlog items. High-priority areas:

- Improving RAG retrieval quality (FAISS indexing, embedding strategies)
- Adding support for more programming languages
- Enhancing VS Code extension UX (inline decorations, hover tooltips)
- Optimizing GPT-4o prompts for better review quality
- Expanding test coverage (unit tests, integration tests)
- Performance improvements (API response time, FAISS search speed)

## Questions?

- Open an issue for discussion before starting major work
- For quick questions, comment on related issues
- Be respectful and constructive in all interactions

## License

By contributing, you agree that your contributions will be licensed under the same MIT License that covers this project.

---

**Note for AI-assisted development**: If you use LLM tools (GitHub Copilot, Claude, GPT-4) to generate code, please:
1. Review and understand all generated code before submitting
2. Test thoroughly — AI-generated code can have subtle bugs
3. Mention AI assistance in your PR description
4. Include the prompts you used for transparency
