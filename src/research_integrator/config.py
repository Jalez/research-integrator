"""Configuration management using python-dotenv."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


class Config:
    """Configuration class that loads environment variables using python-dotenv."""

    def __init__(self, env_file: Optional[str] = None):
        """Initialize configuration by loading environment variables.

        Args:
            env_file: Path to .env file. If None, searches for .env in current and parent directories.
        """
        if env_file:
            load_dotenv(env_file)
        else:
            # Search for .env file in current directory and parent directories
            current_dir = Path.cwd()
            for path in [current_dir] + list(current_dir.parents):
                env_path = path / ".env"
                if env_path.exists():
                    load_dotenv(env_path)
                    break
            else:
                # If no .env file found, still load from environment
                load_dotenv()

    @property
    def pubmed_api_key(self) -> Optional[str]:
        """Get PubMed API key from environment."""
        return os.getenv("PUBMED_API_KEY")

    @property
    def arxiv_user_agent(self) -> str:
        """Get arXiv user agent from environment."""
        return os.getenv("ARXIV_USER_AGENT", "research-integrator/1.0")

    @property
    def llm_api_key(self) -> Optional[str]:
        """Get LLM API key from environment."""
        return os.getenv("LLM_API_KEY")

    @property
    def llm_endpoint(self) -> Optional[str]:
        """Get LLM endpoint URL from environment."""
        return os.getenv("LLM_ENDPOINT")

    @property
    def redis_url(self) -> Optional[str]:
        """Get Redis URL from environment."""
        return os.getenv("REDIS_URL")

    @property
    def log_level(self) -> str:
        """Get logging level from environment."""
        return os.getenv("LOG_LEVEL", "INFO").upper()

    @property
    def log_file(self) -> str:
        """Get log file path from environment."""
        return os.getenv("LOG_FILE", "logs/research_integrator.log")

    def validate(self) -> list[str]:
        """Validate configuration and return list of missing required variables.

        Returns:
            List of missing required environment variable names.
        """
        missing = []

        if not self.pubmed_api_key:
            missing.append("PUBMED_API_KEY")

        if not self.llm_api_key:
            missing.append("LLM_API_KEY")

        if not self.llm_endpoint:
            missing.append("LLM_ENDPOINT")

        return missing
