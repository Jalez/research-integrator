"""Main application module demonstrating configuration and logging setup."""

from .config import Config
from .logger import setup_logger, get_logger


class ResearchIntegrator:
    """Main application class for research integration."""

    def __init__(self, config: Config = None):
        """Initialize the research integrator.

        Args:
            config: Configuration instance. If None, creates a new one.
        """
        self.config = config or Config()

        # Validate configuration
        missing_vars = self.config.validate()
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

        # Set up logging
        self.logger = setup_logger(
            level=self.config.log_level,
            log_file=self.config.log_file
        )

        self.logger.info("Research Integrator initialized successfully")
        self.logger.debug(f"Configuration loaded with log level: {self.config.log_level}")

    def test_configuration(self) -> dict:
        """Test configuration by checking all loaded values.

        Returns:
            Dictionary with configuration status.
        """
        self.logger.info("Testing configuration...")

        config_status = {
            "pubmed_api_key": bool(self.config.pubmed_api_key),
            "arxiv_user_agent": self.config.arxiv_user_agent,
            "llm_api_key": bool(self.config.llm_api_key),
            "llm_endpoint": bool(self.config.llm_endpoint),
            "redis_url": bool(self.config.redis_url),
            "log_level": self.config.log_level,
            "log_file": self.config.log_file,
        }

        self.logger.info("Configuration test completed", extra={"extra_fields": config_status})
        return config_status


def main():
    """Main entry point for the application."""
    try:
        integrator = ResearchIntegrator()
        status = integrator.test_configuration()
        print("Configuration Status:")
        for key, value in status.items():
            print(f"  {key}: {value}")
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please check your .env file and ensure all required variables are set.")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
