"""Pydantic models for request/response validation."""

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Single chat message."""

    role: str = Field(..., description="Role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Request payload for chat endpoint."""

    message: str = Field(..., min_length=1, description="User's message")
    conversation_history: list[ChatMessage] = Field(
        default_factory=list, description="Previous conversation history"
    )


class ChatResponse(BaseModel):
    """Response payload from chat endpoint."""

    response: str = Field(..., description="Chatbot's response")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Response confidence")
    show_fallback: bool = Field(
        ..., description="Whether to show Microsoft List fallback link"
    )
    microsoft_list_url: str | None = Field(
        None, description="URL to Microsoft List if fallback is needed"
    )
    sources: list[str] = Field(
        default_factory=list, description="Sources used for the response"
    )


class HealthCheck(BaseModel):
    """Health check response."""

    status: str
    message: str
