"""FastAPI application for Research Integrator API."""

import os
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.middleware.cors import CORSMiddleware

from ..config import Config
from ..logger import get_logger
from .models import (
    ContextRequest,
    ContextResponse,
    ErrorResponse,
    FetchRequest,
    FetchResponse,
    PreferencesRequest,
    PreferencesResponse,
    SearchRequest,
    SearchResponse,
    SummarizeRequest,
    SummarizeResponse,
)

# Initialize configuration and logger
config = Config()
logger = get_logger("research_integrator.api")

# Security scheme - auto_error=False to handle missing auth manually
security = HTTPBearer(auto_error=False)

# Create FastAPI app
app = FastAPI(
    title="Research Integrator API",
    description="""
    API for integrating research data from multiple sources including PubMed, arXiv, and LLM services.

    This API provides endpoints for searching, fetching, summarizing research papers,
    managing user preferences, and handling context data.
    """,
    version="1.0.0",
    contact={
        "name": "Research Integrator Team",
        "email": "support@research-integrator.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def verify_api_key(credentials: Optional[HTTPAuthorizationCredentials] = Security(security)) -> str:
    """Verify API key from Authorization header.

    Args:
        credentials: HTTP authorization credentials

    Returns:
        The verified API key

    Raises:
        HTTPException: If API key is invalid
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=create_error_response("MISSING_API_KEY", "API key is required"),
        )

    # Extract token from "Bearer TOKEN" format
    token = credentials.credentials

    # For now, we'll accept any non-empty token
    # In production, this should validate against a proper API key store
    if not token or token.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=create_error_response("INVALID_API_KEY", "Invalid API key"),
        )

    logger.info("API key verified", extra={"extra_fields": {"token_prefix": token[:8] + "..."}})
    return token


def create_error_response(code: str, message: str, details: dict = None) -> dict:
    """Create standardized error response.

    Args:
        code: Error code string
        message: User-friendly error message
        details: Optional structured details

    Returns:
        Error response dictionary
    """
    error_response = {
        "code": code,
        "message": message,
    }
    if details:
        error_response["details"] = details

    return error_response


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions with standardized error format."""
    from fastapi.responses import JSONResponse

    logger.error(f"HTTP exception: {exc.detail}", extra={"extra_fields": {"status_code": exc.status_code}})

    # If detail is already in our error format, return it
    if isinstance(exc.detail, dict) and "code" in exc.detail:
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail
        )

    # Otherwise, create a standardized error response
    error_content = create_error_response(
        code="HTTP_ERROR",
        message=str(exc.detail),
        details={"status_code": exc.status_code}
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error_content
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions with standardized error format."""
    from fastapi.responses import JSONResponse

    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)

    error_content = create_error_response(
        code="INTERNAL_ERROR",
        message="An unexpected error occurred",
        details={"error_type": type(exc).__name__}
    )

    return JSONResponse(
        status_code=500,
        content=error_content
    )


@app.post(
    "/search",
    response_model=SearchResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    tags=["Search"],
    summary="Search for research papers",
    description="Search for research papers across multiple sources (PubMed, arXiv, etc.)",
)
async def search_papers(
    request: SearchRequest,
    api_key: str = Security(verify_api_key)
) -> SearchResponse:
    """Search for research papers."""
    logger.info("Search request received", extra={"extra_fields": {"query": request.query}})

    # TODO: Implement actual search logic
    # For now, return a mock response
    return SearchResponse(
        papers=[],
        total=0,
        query=request.query,
        offset=request.offset,
        limit=request.limit,
    )


@app.post(
    "/fetch",
    response_model=FetchResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Paper not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    tags=["Fetch"],
    summary="Fetch paper details",
    description="Fetch detailed information for specific research papers",
)
async def fetch_paper(
    request: FetchRequest,
    api_key: str = Security(verify_api_key)
) -> FetchResponse:
    """Fetch paper details."""
    logger.info("Fetch request received", extra={"extra_fields": {"paper_ids": request.paper_ids}})

    # TODO: Implement actual fetch logic
    # For now, return a mock response
    return FetchResponse(papers=[])


@app.post(
    "/summarize",
    response_model=SummarizeResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    tags=["Summarize"],
    summary="Summarize research papers",
    description="Generate AI-powered summaries of research papers",
)
async def summarize_paper(
    request: SummarizeRequest,
    api_key: str = Security(verify_api_key)
) -> SummarizeResponse:
    """Summarize research papers."""
    logger.info("Summarize request received", extra={"extra_fields": {"paper_id": request.paper_id}})

    # TODO: Implement actual summarization logic
    # For now, return a mock response
    return SummarizeResponse(
        paper_id=request.paper_id,
        summary="This is a mock summary.",
        summary_type=request.summary_type,
        word_count=5,
        generated_at=datetime.now(),
    )


@app.get(
    "/prefs",
    response_model=PreferencesResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    tags=["Preferences"],
    summary="Get user preferences",
    description="Retrieve user preferences and settings",
)
async def get_preferences(
    api_key: str = Security(verify_api_key)
) -> PreferencesResponse:
    """Get user preferences."""
    logger.info("Get preferences request received")

    # TODO: Implement actual preferences retrieval logic
    # For now, return a mock response
    return PreferencesResponse(
        user_id="mock_user",
        preferences=PreferencesRequest(),
        updated_at=datetime.now(),
    )


@app.put(
    "/prefs",
    response_model=PreferencesResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    tags=["Preferences"],
    summary="Update user preferences",
    description="Update user preferences and settings",
)
async def update_preferences(
    request: PreferencesRequest,
    api_key: str = Security(verify_api_key)
) -> PreferencesResponse:
    """Update user preferences."""
    logger.info("Update preferences request received")

    # TODO: Implement actual preferences update logic
    # For now, return a mock response
    return PreferencesResponse(
        user_id="mock_user",
        preferences=request,
        updated_at=datetime.now(),
    )


@app.post(
    "/context",
    response_model=ContextResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    tags=["Context"],
    summary="Manage context data",
    description="Store and retrieve context data for research sessions",
)
async def manage_context(
    request: ContextRequest,
    api_key: str = Security(verify_api_key)
) -> ContextResponse:
    """Manage context data."""
    logger.info("Manage context request received", extra={"extra_fields": {"action": request.action}})

    # TODO: Implement actual context management logic
    # For now, return a mock response
    return ContextResponse(
        session_id=request.session_id or "mock_session",
        action=request.action,
        context_data=request.context_data,
        timestamp=datetime.now(),
    )


@app.get(
    "/context",
    response_model=ContextResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Context not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    tags=["Context"],
    summary="Get context data",
    description="Retrieve stored context data for research sessions",
)
async def get_context(
    session_id: Optional[str] = None,
    api_key: str = Security(verify_api_key)
) -> ContextResponse:
    """Get context data."""
    logger.info("Get context request received", extra={"extra_fields": {"session_id": session_id}})

    # TODO: Implement actual context retrieval logic
    # For now, return a mock response
    return ContextResponse(
        session_id=session_id or "mock_session",
        action="retrieve",
        context_data={},
        timestamp=datetime.now(),
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now()}


if __name__ == "__main__":
    import uvicorn

    # Get port from environment or use default
    port = int(os.getenv("PORT", "8000"))

    uvicorn.run(
        "research_integrator.api.app:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info",
    )
