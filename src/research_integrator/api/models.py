"""Pydantic models for API request/response schemas."""

from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SourceEnum(str, Enum):
    """Enumeration of paper sources."""
    PUBMED = "pubmed"
    ARXIV = "arxiv"
    OTHER = "other"


class SummaryTypeEnum(str, Enum):
    """Enumeration of summary types."""
    BRIEF = "brief"
    DETAILED = "detailed"
    TECHNICAL = "technical"


class ContextActionEnum(str, Enum):
    """Enumeration of context actions."""
    STORE = "store"
    UPDATE = "update"
    DELETE = "delete"
    RETRIEVE = "retrieve"


# Error Response Models
class ErrorResponse(BaseModel):
    """Standard error response model."""
    code: str = Field(..., description="Error code string")
    message: str = Field(..., description="User-friendly error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Optional structured details about the error")


# Paper Model
class Paper(BaseModel):
    """Paper model representing a research paper."""
    id: str = Field(..., description="Unique identifier for the paper")
    title: str = Field(..., description="Title of the paper")
    authors: Optional[List[str]] = Field(None, description="List of authors")
    abstract: Optional[str] = Field(None, description="Abstract of the paper")
    source: SourceEnum = Field(..., description="Source of the paper")
    publication_date: Optional[date] = Field(None, description="Publication date")
    journal: Optional[str] = Field(None, description="Journal name")
    doi: Optional[str] = Field(None, description="Digital Object Identifier")
    url: Optional[str] = Field(None, description="URL to the paper")
    keywords: Optional[List[str]] = Field(None, description="Keywords associated with the paper")


# Search Models
class SearchFilters(BaseModel):
    """Search filters model."""
    date_from: Optional[date] = Field(None, description="Filter papers from this date")
    date_to: Optional[date] = Field(None, description="Filter papers to this date")
    journal: Optional[str] = Field(None, description="Filter by journal name")


class SearchRequest(BaseModel):
    """Search request model."""
    query: str = Field(..., description="Search query")
    sources: List[str] = Field(default=["all"], description="Sources to search in")
    limit: int = Field(default=20, ge=1, le=100, description="Maximum number of results to return")
    offset: int = Field(default=0, ge=0, description="Number of results to skip")
    filters: Optional[SearchFilters] = Field(None, description="Additional search filters")


class SearchResponse(BaseModel):
    """Search response model."""
    papers: List[Paper] = Field(..., description="List of papers matching the search")
    total: int = Field(..., description="Total number of papers found")
    query: str = Field(..., description="Original search query")
    offset: int = Field(..., description="Number of results skipped")
    limit: int = Field(..., description="Maximum number of results returned")


# Fetch Models
class FetchRequest(BaseModel):
    """Fetch request model."""
    paper_ids: List[str] = Field(..., description="List of paper IDs to fetch")
    include_full_text: bool = Field(default=False, description="Whether to include full text if available")


class FetchResponse(BaseModel):
    """Fetch response model."""
    papers: List[Paper] = Field(..., description="List of fetched papers with detailed information")


# Summarize Models
class SummarizeRequest(BaseModel):
    """Summarize request model."""
    paper_id: str = Field(..., description="ID of the paper to summarize")
    summary_type: SummaryTypeEnum = Field(default=SummaryTypeEnum.BRIEF, description="Type of summary to generate")
    max_length: int = Field(default=200, ge=50, le=1000, description="Maximum length of summary in words")


class SummarizeResponse(BaseModel):
    """Summarize response model."""
    paper_id: str = Field(..., description="ID of the summarized paper")
    summary: str = Field(..., description="Generated summary")
    summary_type: SummaryTypeEnum = Field(..., description="Type of summary generated")
    word_count: int = Field(..., description="Number of words in the summary")
    generated_at: datetime = Field(..., description="Timestamp when summary was generated")


# Preferences Models
class SummaryPreferences(BaseModel):
    """Summary preferences model."""
    default_type: SummaryTypeEnum = Field(default=SummaryTypeEnum.BRIEF, description="Default summary type")
    max_length: int = Field(default=200, ge=50, le=1000, description="Default maximum summary length")


class NotificationSettings(BaseModel):
    """Notification settings model."""
    email_notifications: bool = Field(default=True, description="Enable email notifications")
    search_alerts: bool = Field(default=False, description="Enable search alerts")


class PreferencesRequest(BaseModel):
    """Preferences request model."""
    default_sources: Optional[List[str]] = Field(None, description="Default sources for searches")
    default_limit: Optional[int] = Field(None, ge=1, le=100, description="Default number of results per search")
    summary_preferences: Optional[SummaryPreferences] = Field(None, description="Summary preferences")
    notification_settings: Optional[NotificationSettings] = Field(None, description="Notification settings")


class PreferencesResponse(BaseModel):
    """Preferences response model."""
    user_id: str = Field(..., description="User identifier")
    preferences: PreferencesRequest = Field(..., description="User preferences")
    updated_at: datetime = Field(..., description="Timestamp when preferences were last updated")


# Context Models
class ContextRequest(BaseModel):
    """Context request model."""
    action: ContextActionEnum = Field(..., description="Action to perform on context data")
    session_id: Optional[str] = Field(None, description="Session identifier")
    context_data: Optional[Dict[str, Any]] = Field(None, description="Context data to store or update")


class ContextResponse(BaseModel):
    """Context response model."""
    session_id: str = Field(..., description="Session identifier")
    action: ContextActionEnum = Field(..., description="Action that was performed")
    context_data: Optional[Dict[str, Any]] = Field(None, description="Current context data")
    timestamp: datetime = Field(..., description="Timestamp of the operation")
