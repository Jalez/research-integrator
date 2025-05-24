#!/usr/bin/env python3
"""Script to run the Research Integrator API server."""

import os
import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

import uvicorn
from research_integrator.api.app import app

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.getenv("PORT", "8000"))

    print(f"Starting Research Integrator API server on port {port}")
    print(f"API documentation will be available at: http://localhost:{port}/api/docs")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info",
    )
