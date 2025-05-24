"""Tests for the Research Integrator API."""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

import pytest
from fastapi.testclient import TestClient
from datetime import datetime

from research_integrator.api.app import app
from research_integrator.api.models import (
    ContextActionEnum,
    SummaryTypeEnum,
)


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def auth_headers():
    """Create authorization headers for testing."""
    return {"Authorization": "Bearer test_api_key"}


class TestAuthentication:
    """Test authentication functionality."""

    def test_missing_auth_header(self, client):
        """Test request without authorization header."""
        response = client.post("/search", json={"query": "test"})
        assert response.status_code == 401
        data = response.json()
        assert data["code"] == "MISSING_API_KEY"
        assert "API key is required" in data["message"]

    def test_empty_auth_header(self, client):
        """Test request with empty authorization header."""
        response = client.post(
            "/search",
            json={"query": "test"},
            headers={"Authorization": "Bearer"}
        )
        assert response.status_code == 401
        data = response.json()
        assert data["code"] == "MISSING_API_KEY"
        assert "API key is required" in data["message"]

    def test_invalid_auth_header(self, client):
        """Test request with invalid authorization header."""
        response = client.post(
            "/search",
            json={"query": "test"},
            headers={"Authorization": "Bearer   "}  # Empty token with spaces
        )
        assert response.status_code == 401
        data = response.json()
        assert data["code"] == "INVALID_API_KEY"
        assert "Invalid API key" in data["message"]

    def test_valid_auth_header(self, client, auth_headers):
        """Test request with valid authorization header."""
        response = client.post(
            "/search",
            json={"query": "test"},
            headers=auth_headers
        )
        assert response.status_code == 200


class TestSearchEndpoint:
    """Test search endpoint functionality."""

    def test_search_basic_request(self, client, auth_headers):
        """Test basic search request."""
        response = client.post(
            "/search",
            json={"query": "machine learning"},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["query"] == "machine learning"
        assert data["total"] == 0
        assert data["papers"] == []
        assert data["offset"] == 0
        assert data["limit"] == 20

    def test_search_with_parameters(self, client, auth_headers):
        """Test search request with parameters."""
        request_data = {
            "query": "healthcare AI",
            "sources": ["pubmed", "arxiv"],
            "limit": 10,
            "offset": 5,
            "filters": {
                "date_from": "2020-01-01",
                "date_to": "2023-12-31",
                "journal": "Nature"
            }
        }
        response = client.post(
            "/search",
            json=request_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["query"] == "healthcare AI"
        assert data["limit"] == 10
        assert data["offset"] == 5

    def test_search_invalid_limit(self, client, auth_headers):
        """Test search request with invalid limit."""
        response = client.post(
            "/search",
            json={"query": "test", "limit": 101},
            headers=auth_headers
        )
        assert response.status_code == 422  # Validation error

    def test_search_missing_query(self, client, auth_headers):
        """Test search request without query."""
        response = client.post(
            "/search",
            json={},
            headers=auth_headers
        )
        assert response.status_code == 422  # Validation error


class TestFetchEndpoint:
    """Test fetch endpoint functionality."""

    def test_fetch_basic_request(self, client, auth_headers):
        """Test basic fetch request."""
        response = client.post(
            "/fetch",
            json={"paper_ids": ["pubmed:12345678", "arxiv:2301.12345"]},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["papers"] == []

    def test_fetch_with_full_text(self, client, auth_headers):
        """Test fetch request with full text option."""
        response = client.post(
            "/fetch",
            json={
                "paper_ids": ["pubmed:12345678"],
                "include_full_text": True
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["papers"] == []

    def test_fetch_missing_paper_ids(self, client, auth_headers):
        """Test fetch request without paper IDs."""
        response = client.post(
            "/fetch",
            json={},
            headers=auth_headers
        )
        assert response.status_code == 422  # Validation error


class TestSummarizeEndpoint:
    """Test summarize endpoint functionality."""

    def test_summarize_basic_request(self, client, auth_headers):
        """Test basic summarize request."""
        response = client.post(
            "/summarize",
            json={"paper_id": "pubmed:12345678"},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["paper_id"] == "pubmed:12345678"
        assert data["summary"] == "This is a mock summary."
        assert data["summary_type"] == "brief"
        assert data["word_count"] == 5
        assert "generated_at" in data

    def test_summarize_with_parameters(self, client, auth_headers):
        """Test summarize request with parameters."""
        response = client.post(
            "/summarize",
            json={
                "paper_id": "arxiv:2301.12345",
                "summary_type": "detailed",
                "max_length": 500
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["paper_id"] == "arxiv:2301.12345"
        assert data["summary_type"] == "detailed"

    def test_summarize_invalid_max_length(self, client, auth_headers):
        """Test summarize request with invalid max length."""
        response = client.post(
            "/summarize",
            json={
                "paper_id": "pubmed:12345678",
                "max_length": 1001  # Too high
            },
            headers=auth_headers
        )
        assert response.status_code == 422  # Validation error

    def test_summarize_missing_paper_id(self, client, auth_headers):
        """Test summarize request without paper ID."""
        response = client.post(
            "/summarize",
            json={},
            headers=auth_headers
        )
        assert response.status_code == 422  # Validation error


class TestPreferencesEndpoint:
    """Test preferences endpoint functionality."""

    def test_get_preferences(self, client, auth_headers):
        """Test get preferences request."""
        response = client.get("/prefs", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == "mock_user"
        assert "preferences" in data
        assert "updated_at" in data

    def test_update_preferences(self, client, auth_headers):
        """Test update preferences request."""
        preferences_data = {
            "default_sources": ["pubmed", "arxiv"],
            "default_limit": 25,
            "summary_preferences": {
                "default_type": "detailed",
                "max_length": 300
            },
            "notification_settings": {
                "email_notifications": True,
                "search_alerts": False
            }
        }
        response = client.put(
            "/prefs",
            json=preferences_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == "mock_user"
        assert data["preferences"]["default_limit"] == 25

    def test_update_preferences_invalid_limit(self, client, auth_headers):
        """Test update preferences with invalid limit."""
        response = client.put(
            "/prefs",
            json={"default_limit": 101},  # Too high
            headers=auth_headers
        )
        assert response.status_code == 422  # Validation error


class TestContextEndpoint:
    """Test context endpoint functionality."""

    def test_manage_context_store(self, client, auth_headers):
        """Test store context request."""
        context_data = {
            "action": "store",
            "session_id": "test_session_123",
            "context_data": {
                "search_history": ["machine learning", "healthcare AI"],
                "current_papers": ["pubmed:12345678"],
                "research_focus": "AI in medical diagnosis"
            }
        }
        response = client.post(
            "/context",
            json=context_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == "test_session_123"
        assert data["action"] == "store"
        assert "timestamp" in data

    def test_manage_context_update(self, client, auth_headers):
        """Test update context request."""
        context_data = {
            "action": "update",
            "session_id": "test_session_123",
            "context_data": {
                "search_history": ["machine learning", "healthcare AI", "neural networks"]
            }
        }
        response = client.post(
            "/context",
            json=context_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["action"] == "update"

    def test_manage_context_delete(self, client, auth_headers):
        """Test delete context request."""
        context_data = {
            "action": "delete",
            "session_id": "test_session_123"
        }
        response = client.post(
            "/context",
            json=context_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["action"] == "delete"

    def test_get_context(self, client, auth_headers):
        """Test get context request."""
        response = client.get(
            "/context",
            params={"session_id": "test_session_123"},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == "test_session_123"
        assert data["action"] == "retrieve"

    def test_get_context_no_session_id(self, client, auth_headers):
        """Test get context request without session ID."""
        response = client.get("/context", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == "mock_session"

    def test_manage_context_missing_action(self, client, auth_headers):
        """Test context request without action."""
        response = client.post(
            "/context",
            json={"session_id": "test_session"},
            headers=auth_headers
        )
        assert response.status_code == 422  # Validation error


class TestHealthEndpoint:
    """Test health endpoint functionality."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data


class TestErrorHandling:
    """Test error handling functionality."""

    def test_error_response_format(self, client):
        """Test that error responses follow the standard format."""
        response = client.post("/search", json={"query": "test"})
        assert response.status_code == 401
        data = response.json()
        assert "code" in data
        assert "message" in data
        assert isinstance(data["code"], str)
        assert isinstance(data["message"], str)


class TestOpenAPISpec:
    """Test OpenAPI specification."""

    def test_openapi_json_accessible(self, client):
        """Test that OpenAPI JSON is accessible."""
        response = client.get("/api/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert data["openapi"] == "3.1.0"  # FastAPI uses OpenAPI 3.1.0
        assert data["info"]["title"] == "Research Integrator API"

    def test_docs_accessible(self, client):
        """Test that Swagger UI docs are accessible."""
        response = client.get("/api/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_redoc_accessible(self, client):
        """Test that ReDoc docs are accessible."""
        response = client.get("/api/redoc")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
