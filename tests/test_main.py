"""Tests for main application module."""

import os
import tempfile
import unittest
from unittest.mock import patch

from research_integrator.config import Config
from research_integrator.main import ResearchIntegrator


class TestResearchIntegrator(unittest.TestCase):
    """Test cases for ResearchIntegrator class."""

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

        # Set required environment variables for testing
        os.environ["PUBMED_API_KEY"] = "test_pubmed_key"
        os.environ["LLM_API_KEY"] = "test_llm_key"
        os.environ["LLM_ENDPOINT"] = "https://api.test.com"

        self.temp_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.temp_dir, "test.log")
        os.environ["LOG_FILE"] = self.log_file

    def tearDown(self):
        """Clean up test environment."""
        # Restore original environment variables
        for var, value in self.original_env.items():
            if value is not None:
                os.environ[var] = value
            elif var in os.environ:
                del os.environ[var]

    def test_initialization_success(self):
        """Test successful initialization with valid configuration."""
        integrator = ResearchIntegrator()

        self.assertIsNotNone(integrator.config)
        self.assertIsNotNone(integrator.logger)
        self.assertEqual(integrator.config.pubmed_api_key, "test_pubmed_key")
        self.assertEqual(integrator.config.llm_api_key, "test_llm_key")
        self.assertEqual(integrator.config.llm_endpoint, "https://api.test.com")

    def test_initialization_with_custom_config(self):
        """Test initialization with custom configuration."""
        config = Config()
        integrator = ResearchIntegrator(config=config)

        self.assertEqual(integrator.config, config)

    def test_initialization_missing_required_vars(self):
        """Test initialization failure with missing required variables."""
        # Remove required environment variable
        del os.environ["PUBMED_API_KEY"]

        with self.assertRaises(ValueError) as context:
            ResearchIntegrator()

        self.assertIn("Missing required environment variables", str(context.exception))
        self.assertIn("PUBMED_API_KEY", str(context.exception))

    def test_configuration_test(self):
        """Test configuration testing functionality."""
        integrator = ResearchIntegrator()
        status = integrator.test_configuration()

        self.assertIsInstance(status, dict)
        self.assertIn("pubmed_api_key", status)
        self.assertIn("llm_api_key", status)
        self.assertIn("llm_endpoint", status)
        self.assertIn("log_level", status)

        # Check that boolean values are correct
        self.assertTrue(status["pubmed_api_key"])
        self.assertTrue(status["llm_api_key"])
        self.assertTrue(status["llm_endpoint"])

    def test_configuration_test_with_optional_vars(self):
        """Test configuration testing with optional variables set."""
        os.environ["REDIS_URL"] = "redis://localhost:6379"
        os.environ["ARXIV_USER_AGENT"] = "custom-agent/1.0"

        integrator = ResearchIntegrator()
        status = integrator.test_configuration()

        self.assertTrue(status["redis_url"])
        self.assertEqual(status["arxiv_user_agent"], "custom-agent/1.0")


class TestMainFunction(unittest.TestCase):
    """Test cases for main function."""

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

    @patch('builtins.print')
    def test_main_with_missing_config(self, mock_print):
        """Test main function with missing configuration."""
        from research_integrator.main import main

        main()

        # Check that error message was printed
        mock_print.assert_called()
        printed_args = [call[0][0] for call in mock_print.call_args_list]
        error_messages = [msg for msg in printed_args if "Configuration error" in msg]
        self.assertTrue(len(error_messages) > 0)

    @patch('builtins.print')
    def test_main_with_valid_config(self, mock_print):
        """Test main function with valid configuration."""
        from research_integrator.main import main

        # Set required environment variables
        os.environ["PUBMED_API_KEY"] = "test_key"
        os.environ["LLM_API_KEY"] = "test_llm_key"
        os.environ["LLM_ENDPOINT"] = "https://api.test.com"

        main()

        # Check that configuration status was printed
        mock_print.assert_called()
        printed_args = [call[0][0] for call in mock_print.call_args_list]
        status_messages = [msg for msg in printed_args if "Configuration Status" in msg]
        self.assertTrue(len(status_messages) > 0)


if __name__ == "__main__":
    unittest.main()
