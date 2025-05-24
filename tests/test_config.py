"""Tests for configuration management."""

import os
import tempfile
import unittest
from pathlib import Path

from research_integrator.config import Config


class TestConfig(unittest.TestCase):
    """Test cases for Config class."""

    def setUp(self):
        """Set up test environment."""
        # Store original environment variables
        self.original_env = {}
        env_vars = [
            "PUBMED_API_KEY", "ARXIV_USER_AGENT", "LLM_API_KEY",
            "LLM_ENDPOINT", "REDIS_URL", "LOG_LEVEL", "LOG_FILE"
        ]
        for var in env_vars:
            self.original_env[var] = os.environ.get(var)
            if var in os.environ:
                del os.environ[var]

    def tearDown(self):
        """Clean up test environment."""
        # Restore original environment variables
        for var, value in self.original_env.items():
            if value is not None:
                os.environ[var] = value
            elif var in os.environ:
                del os.environ[var]

    def test_config_defaults(self):
        """Test configuration with default values."""
        config = Config()

        self.assertIsNone(config.pubmed_api_key)
        self.assertEqual(config.arxiv_user_agent, "research-integrator/1.0")
        self.assertIsNone(config.llm_api_key)
        self.assertIsNone(config.llm_endpoint)
        self.assertIsNone(config.redis_url)
        self.assertEqual(config.log_level, "INFO")
        self.assertEqual(config.log_file, "logs/research_integrator.log")

    def test_config_from_environment(self):
        """Test configuration loading from environment variables."""
        os.environ["PUBMED_API_KEY"] = "test_pubmed_key"
        os.environ["ARXIV_USER_AGENT"] = "test-agent/1.0"
        os.environ["LLM_API_KEY"] = "test_llm_key"
        os.environ["LLM_ENDPOINT"] = "https://api.test.com"
        os.environ["REDIS_URL"] = "redis://localhost:6379"
        os.environ["LOG_LEVEL"] = "DEBUG"
        os.environ["LOG_FILE"] = "test.log"

        config = Config()

        self.assertEqual(config.pubmed_api_key, "test_pubmed_key")
        self.assertEqual(config.arxiv_user_agent, "test-agent/1.0")
        self.assertEqual(config.llm_api_key, "test_llm_key")
        self.assertEqual(config.llm_endpoint, "https://api.test.com")
        self.assertEqual(config.redis_url, "redis://localhost:6379")
        self.assertEqual(config.log_level, "DEBUG")
        self.assertEqual(config.log_file, "test.log")

    def test_config_from_file(self):
        """Test configuration loading from .env file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
            f.write("PUBMED_API_KEY=file_pubmed_key\n")
            f.write("LLM_API_KEY=file_llm_key\n")
            f.write("LLM_ENDPOINT=https://api.file.com\n")
            env_file = f.name

        try:
            config = Config(env_file=env_file)

            self.assertEqual(config.pubmed_api_key, "file_pubmed_key")
            self.assertEqual(config.llm_api_key, "file_llm_key")
            self.assertEqual(config.llm_endpoint, "https://api.file.com")
        finally:
            os.unlink(env_file)

    def test_config_validation(self):
        """Test configuration validation."""
        config = Config()
        missing = config.validate()

        expected_missing = ["PUBMED_API_KEY", "LLM_API_KEY", "LLM_ENDPOINT"]
        self.assertEqual(sorted(missing), sorted(expected_missing))

        # Set required variables
        os.environ["PUBMED_API_KEY"] = "test_key"
        os.environ["LLM_API_KEY"] = "test_llm_key"
        os.environ["LLM_ENDPOINT"] = "https://api.test.com"

        config = Config()
        missing = config.validate()
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
