"""Sample tests for the HR Chatbot API.

Run with: pytest test_main.py
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from main import app
from models import ChatResponse


client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "message" in data


def test_get_config():
    """Test config endpoint."""
    response = client.get("/api/config")
    assert response.status_code == 200
    data = response.json()
    assert "microsoft_list_url" in data
    assert "confidence_threshold" in data


@patch("chatbot_service.chatbot_service.get_response")
async def test_chat_endpoint(mock_get_response):
    """Test chat endpoint with mocked AI response."""
    # Mock the AI response
    mock_response = ChatResponse(
        response="You can check your PTO on WalmartOne portal.",
        confidence=0.95,
        show_fallback=False,
        microsoft_list_url=None,
        sources=["FAQ Database"],
    )
    mock_get_response.return_value = mock_response

    # Send chat request
    response = client.post(
        "/api/chat",
        json={
            "message": "How do I check my PTO?",
            "conversation_history": [],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "confidence" in data
    assert data["show_fallback"] is False


def test_chat_endpoint_validation():
    """Test chat endpoint input validation."""
    # Empty message should fail validation
    response = client.post(
        "/api/chat",
        json={
            "message": "",
            "conversation_history": [],
        },
    )
    assert response.status_code == 422  # Validation error

    # Missing required field
    response = client.post(
        "/api/chat",
        json={
            "conversation_history": [],
        },
    )
    assert response.status_code == 422


def test_faq_search():
    """Test FAQ database search."""
    from knowledge_base import search_faq

    # Should find PTO FAQ
    result = search_faq("How do I check my PTO balance?")
    assert result is not None
    assert "PTO" in result or "pto" in result.lower()

    # Should find benefits FAQ
    result = search_faq("What benefits does Walmart offer?")
    assert result is not None

    # Should return None for unknown topic
    result = search_faq("What's the weather today?")
    assert result is None
