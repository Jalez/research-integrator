"""Tests for logging functionality."""

import json
import logging
import tempfile
import unittest
from pathlib import Path

from research_integrator.logger import JSONFormatter, setup_logger, get_logger


class TestJSONFormatter(unittest.TestCase):
    """Test cases for JSONFormatter class."""

    def setUp(self):
        """Set up test environment."""
        self.formatter = JSONFormatter()

    def test_json_format(self):
        """Test JSON formatting of log records."""
        record = logging.LogRecord(
            name="test_logger",
            level=logging.INFO,
            pathname="/test/path.py",
            lineno=42,
            msg="Test message",
            args=(),
            exc_info=None,
            func="test_function"
        )

        formatted = self.formatter.format(record)
        log_data = json.loads(formatted)

        self.assertEqual(log_data["level"], "INFO")
        self.assertEqual(log_data["logger"], "test_logger")
        self.assertEqual(log_data["message"], "Test message")
        self.assertEqual(log_data["module"], "path")
        self.assertEqual(log_data["function"], "test_function")
        self.assertEqual(log_data["line"], 42)
        self.assertIn("timestamp", log_data)

    def test_json_format_with_extra_fields(self):
        """Test JSON formatting with extra fields."""
        record = logging.LogRecord(
            name="test_logger",
            level=logging.INFO,
            pathname="/test/path.py",
            lineno=42,
            msg="Test message",
            args=(),
            exc_info=None,
            func="test_function"
        )
        record.extra_fields = {"user_id": 123, "action": "test"}

        formatted = self.formatter.format(record)
        log_data = json.loads(formatted)

        self.assertEqual(log_data["user_id"], 123)
        self.assertEqual(log_data["action"], "test")


class TestLogger(unittest.TestCase):
    """Test cases for logger setup and functionality."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.log_file = str(Path(self.temp_dir) / "test.log")

    def tearDown(self):
        """Clean up test environment."""
        # Clear all handlers from loggers
        for logger_name in logging.Logger.manager.loggerDict:
            logger = logging.getLogger(logger_name)
            logger.handlers.clear()

    def test_setup_logger_basic(self):
        """Test basic logger setup."""
        logger = setup_logger(
            name="test_logger",
            level="INFO",
            log_file=self.log_file,
            console_output=False
        )

        self.assertEqual(logger.name, "test_logger")
        self.assertEqual(logger.level, logging.INFO)
        self.assertEqual(len(logger.handlers), 1)  # Only file handler
        self.assertIsInstance(logger.handlers[0], logging.handlers.RotatingFileHandler)

    def test_setup_logger_with_console(self):
        """Test logger setup with console output."""
        logger = setup_logger(
            name="test_logger_console",
            level="DEBUG",
            log_file=self.log_file,
            console_output=True
        )

        self.assertEqual(logger.level, logging.DEBUG)
        self.assertEqual(len(logger.handlers), 2)  # Console and file handlers

        handler_types = [type(h).__name__ for h in logger.handlers]
        self.assertIn("StreamHandler", handler_types)
        self.assertIn("RotatingFileHandler", handler_types)

    def test_logger_file_creation(self):
        """Test that log file is created."""
        logger = setup_logger(
            name="test_file_creation",
            log_file=self.log_file,
            console_output=False
        )

        logger.info("Test message")

        self.assertTrue(Path(self.log_file).exists())

        with open(self.log_file, 'r') as f:
            content = f.read()
            self.assertIn("Test message", content)

    def test_json_logging(self):
        """Test JSON formatted logging."""
        logger = setup_logger(
            name="test_json",
            log_file=self.log_file,
            console_output=False,
            json_format=True
        )

        logger.info("Test JSON message")

        with open(self.log_file, 'r') as f:
            line = f.readline().strip()
            log_data = json.loads(line)

            self.assertEqual(log_data["level"], "INFO")
            self.assertEqual(log_data["message"], "Test JSON message")
            self.assertIn("timestamp", log_data)

    def test_get_logger(self):
        """Test get_logger function."""
        # First setup a logger
        setup_logger(name="test_get", log_file=self.log_file)

        # Then get it
        logger = get_logger("test_get")

        self.assertEqual(logger.name, "test_get")
        self.assertGreater(len(logger.handlers), 0)


if __name__ == "__main__":
    unittest.main()
