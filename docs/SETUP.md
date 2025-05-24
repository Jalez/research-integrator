# Research Integrator Setup Guide

## Overview

This document describes the setup and configuration of the Research Integrator project, which provides academic database integration with AI summarization capabilities.

## Project Structure

```
research-integrator/
├── src/
│   └── research_integrator/
│       ├── __init__.py          # Package initialization
│       ├── config.py            # Configuration management
│       ├── logger.py            # Structured logging
│       └── main.py              # Main application
├── tests/
│   ├── __init__.py
│   ├── test_config.py           # Configuration tests
│   ├── test_logger.py           # Logging tests
│   └── test_main.py             # Main application tests
├── docs/
│   └── SETUP.md                 # This file
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── workflows/               # GitHub Actions workflows
├── logs/                        # Log files directory
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── LICENSE                      # MIT License
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
├── setup.py                     # Package setup
└── pytest.ini                  # Test configuration
```

## Features Implemented

### ✅ Repository Structure
- Created proper Python package structure with `src/`, `tests/`, `docs/`, and `.github/ISSUE_TEMPLATE/` directories
- Added comprehensive `.gitignore` with Python and OS-specific ignores
- Included MIT License
- Updated README.md with clear project goals and usage instructions

### ✅ Configuration Management
- **python-dotenv integration**: Loads environment variables from `.env` files
- **Environment variable support**:
  - `PUBMED_API_KEY`: API key for PubMed access
  - `ARXIV_USER_AGENT`: User agent string for arXiv requests
  - `LLM_API_KEY`: API key for LLM service
  - `LLM_ENDPOINT`: Endpoint URL for LLM service
  - `REDIS_URL`: Redis connection URL (optional)
  - `LOG_LEVEL`: Logging level configuration
  - `LOG_FILE`: Log file path configuration
- **Configuration validation**: Checks for required environment variables
- **Flexible loading**: Supports loading from specific files or auto-discovery

### ✅ Structured JSON Logging
- **JSON formatter**: Custom formatter that outputs structured JSON logs
- **Multiple handlers**: Console and rotating file handlers
- **Configurable levels**: DEBUG, INFO, WARNING, ERROR support
- **Rotating files**: Automatic log rotation with configurable size and backup count
- **Extra fields**: Support for additional context in log messages
- **Timestamp formatting**: ISO format timestamps for better parsing

### ✅ Testing Infrastructure
- **Comprehensive test suite**: 18 tests covering all major functionality
- **93% code coverage**: High test coverage ensuring reliability
- **pytest configuration**: Proper test discovery and execution
- **Mocking**: Proper isolation of tests using unittest.mock
- **Environment isolation**: Tests don't interfere with each other

### ✅ Package Management
- **setup.py**: Proper package configuration for installation
- **Console script**: `research-integrator` command-line entry point
- **Requirements management**: Clear dependency specification
- **Editable installation**: Development-friendly installation

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd research-integrator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install the package in development mode**:
   ```bash
   pip install -e .
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your actual API keys and configuration
   ```

## Configuration

### Required Environment Variables

- `PUBMED_API_KEY`: Your PubMed API key
- `LLM_API_KEY`: Your LLM service API key
- `LLM_ENDPOINT`: Your LLM service endpoint URL

### Optional Environment Variables

- `ARXIV_USER_AGENT`: Custom user agent for arXiv (default: "research-integrator/1.0")
- `REDIS_URL`: Redis connection URL for caching
- `LOG_LEVEL`: Logging level (default: "INFO")
- `LOG_FILE`: Log file path (default: "logs/research_integrator.log")

## API Keys Setup

### PubMed API Key
To use the PubMed integration, you'll need an API key from NCBI:

1. Create an NCBI account:
   - Visit https://www.ncbi.nlm.nih.gov/
   - Click "Log in" in the top right
   - If you don't have an account, you'll see an option to create one on the login page

2. Once logged in:
   - Navigate to https://www.ncbi.nlm.nih.gov/account/settings/
   - Find "API Key Management" in your account settings
   - Generate a new API key if you don't have one

3. Add the API key to your .env file:
   ```
   PUBMED_API_KEY=your_api_key_here
   ```

## Usage

### Command Line
```bash
# Using the console script
research-integrator

# Using Python module
python -m research_integrator.main
```

### Python API
```python
from research_integrator import Config
from research_integrator.main import ResearchIntegrator

# Initialize with default configuration
integrator = ResearchIntegrator()

# Initialize with custom configuration
config = Config(env_file="custom.env")
integrator = ResearchIntegrator(config=config)

# Test configuration
status = integrator.test_configuration()
print(status)
```

## Testing

### Run all tests
```bash
pytest tests/ -v
```

### Run tests with coverage
```bash
pytest tests/ -v --cov=src/research_integrator --cov-report=term-missing
```

### Run specific test files
```bash
pytest tests/test_config.py -v
pytest tests/test_logger.py -v
pytest tests/test_main.py -v
```

## Logging

The application uses structured JSON logging with the following features:

- **Console output**: Real-time log viewing during development
- **File output**: Persistent logs with automatic rotation
- **JSON format**: Machine-readable structured logs
- **Configurable levels**: DEBUG, INFO, WARNING, ERROR
- **Context preservation**: Module, function, and line number tracking

### Example log output:
```json
{
  "timestamp": "2025-05-24 17:58:47",
  "level": "INFO",
  "logger": "research_integrator",
  "message": "Research Integrator initialized successfully",
  "module": "main",
  "function": "__init__",
  "line": 29
}
```

## Development

### Adding new features
1. Create feature branch
2. Implement functionality in `src/research_integrator/`
3. Add comprehensive tests in `tests/`
4. Update documentation as needed
5. Ensure all tests pass and coverage remains high

### Code quality
- Follow PEP 8 style guidelines
- Add type hints where appropriate
- Write comprehensive docstrings
- Maintain test coverage above 90%

## Troubleshooting

### Common Issues

1. **Missing environment variables**:
   - Error: "Missing required environment variables: ..."
   - Solution: Check your `.env` file and ensure all required variables are set

2. **Import errors**:
   - Error: "ModuleNotFoundError: No module named 'research_integrator'"
   - Solution: Install the package with `pip install -e .`

3. **Permission errors with log files**:
   - Error: "PermissionError: [Errno 13] Permission denied: 'logs/...'"
   - Solution: Ensure the logs directory is writable or change LOG_FILE path

### Getting Help

- Check the [README.md](../README.md) for basic usage
- Review test files for usage examples
- Create an issue using the GitHub issue templates
- Check logs for detailed error information

## Next Steps

This setup provides a solid foundation for the Research Integrator project. Future development can focus on:

1. **API Integration**: Implement actual PubMed and arXiv API clients
2. **LLM Integration**: Add AI summarization capabilities
3. **Caching**: Implement Redis-based caching for API responses
4. **Web Interface**: Add a web-based user interface
5. **Database**: Add persistent storage for research papers and summaries
6. **Authentication**: Implement user authentication and authorization
