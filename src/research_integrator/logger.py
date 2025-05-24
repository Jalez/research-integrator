"""Structured JSON logging configuration."""

import json
import logging
import logging.handlers
import os
from pathlib import Path
from typing import Any, Dict


class JSONFormatter(logging.Formatter):
    """Custom formatter that outputs log records as JSON."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON string.

        Args:
            record: The log record to format.

        Returns:
            JSON formatted log string.
        """
        log_data: Dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields if present
        if hasattr(record, "extra_fields"):
            log_data.update(record.extra_fields)

        return json.dumps(log_data, ensure_ascii=False)


def setup_logger(
    name: str = "research_integrator",
    level: str = "INFO",
    log_file: str = "logs/research_integrator.log",
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
    console_output: bool = True,
    json_format: bool = True,
) -> logging.Logger:
    """Set up structured logging with console and rotating file handlers.

    Args:
        name: Logger name.
        level: Logging level (DEBUG, INFO, WARNING, ERROR).
        log_file: Path to log file.
        max_bytes: Maximum size of log file before rotation.
        backup_count: Number of backup files to keep.
        console_output: Whether to output to console.
        json_format: Whether to use JSON formatting.

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger(name)

    # Clear any existing handlers
    logger.handlers.clear()

    # Set logging level
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(numeric_level)

    # Create formatters
    if json_format:
        formatter = JSONFormatter(datefmt="%Y-%m-%d %H:%M:%S")
        console_formatter = JSONFormatter(datefmt="%Y-%m-%d %H:%M:%S")
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

    # Create console handler
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    # Create rotating file handler
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8"
    )
    file_handler.setLevel(numeric_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Prevent propagation to root logger
    logger.propagate = False

    return logger


def get_logger(name: str = "research_integrator") -> logging.Logger:
    """Get logger instance.

    Args:
        name: Logger name.

    Returns:
        Logger instance.
    """
    return logging.getLogger(name)
