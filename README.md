# Research Integrator

A Python application that connects to academic databases (e.g., PubMed, arXiv) to retrieve and summarize research papers using AI/LLM integration.

## Project Goals

- **Academic Database Integration**: Connect to PubMed and arXiv APIs to search and retrieve research papers
- **AI-Powered Summarization**: Use Large Language Models to generate concise summaries of research papers
- **Configurable Environment**: Support multiple API keys and endpoints through environment variables
- **Structured Logging**: Comprehensive logging system for monitoring and debugging
- **Caching Support**: Redis integration for efficient data caching and retrieval

## Features

- Search and retrieve papers from PubMed and arXiv
- Generate AI-powered summaries of research papers
- Configurable logging with multiple output formats
- Environment-based configuration management
- Redis caching for improved performance

## Requirements

- Python 3.10+
- Redis (optional, for caching)
- API keys for external services (PubMed, LLM providers)

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env` and configure the following environment variables:

- `PUBMED_API_KEY`: API key for PubMed access
- `ARXIV_USER_AGENT`: User agent string for arXiv requests
- `LLM_API_KEY`: API key for LLM service
- `LLM_ENDPOINT`: Endpoint URL for LLM service
- `REDIS_URL`: Redis connection URL (optional)

## Usage

```python
from research_integrator import ResearchIntegrator

integrator = ResearchIntegrator()
# Use the integrator to search and summarize papers
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
