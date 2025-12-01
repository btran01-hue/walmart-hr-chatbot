"""Chatbot service using local Ollama (100% free, runs on your computer)."""

import requests
from knowledge_base import get_system_prompt, search_faq
from models import ChatMessage, ChatResponse
from config import settings


class ChatbotService:
    """Service for handling chatbot interactions with Ollama."""

    def __init__(self):
        """Initialize Ollama client."""
        self.ollama_url = "http://localhost:11434/api/chat"
        self.model = "llama3.2:3b"  # Fast, small model (or use 'llama3.2' for larger)

    def _calculate_confidence(self, response_text: str, message: str) -> float:
        """
        Calculate confidence score for the response.
        
        This is a simplified heuristic. In production, you might:
        - Use OpenAI's logprobs
        - Implement a separate classification model
        - Use semantic similarity scores
        """
        # Check if response contains uncertainty phrases
        uncertainty_phrases = [
            "i'm not sure",
            "i don't know",
            "unclear",
            "cannot confirm",
            "recommend contacting",
            "please contact",
            "check with hr",
        ]
        
        response_lower = response_text.lower()
        
        # If response contains uncertainty, lower confidence
        if any(phrase in response_lower for phrase in uncertainty_phrases):
            return 0.5
        
        # If response is very short, might be unsure
        if len(response_text.split()) < 10:
            return 0.6
        
        # Check if we have a FAQ match (high confidence)
        if search_faq(message):
            return 0.95
        
        # Default moderate-high confidence
        return 0.8

    async def get_response(
        self, message: str, conversation_history: list[ChatMessage]
    ) -> ChatResponse:
        """
        Get chatbot response using local Ollama.
        
        Args:
            message: User's question
            conversation_history: Previous conversation messages
            
        Returns:
            ChatResponse with answer and metadata
        """
        # Check FAQ first for instant responses
        faq_answer = search_faq(message)
        if faq_answer:
            return ChatResponse(
                response=faq_answer,
                confidence=0.95,
                show_fallback=False,
                microsoft_list_url=None,
                sources=["FAQ Database"],
            )

        # Build messages for Ollama
        messages = [
            {"role": "system", "content": get_system_prompt()},
        ]

        # Add conversation history
        for msg in conversation_history[-10:]:  # Keep last 10 messages for context
            messages.append({"role": msg.role, "content": msg.content})

        # Add current message
        messages.append({"role": "user", "content": message})

        try:
            # Call Ollama API (running locally)
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                },
                timeout=30,  # Local LLM might take a bit longer
            )
            response.raise_for_status()
            
            result = response.json()
            assistant_message = result["message"]["content"]
            
            # Calculate confidence
            confidence = self._calculate_confidence(assistant_message, message)
            
            # Determine if we should show fallback
            show_fallback = confidence < settings.confidence_threshold
            
            return ChatResponse(
                response=assistant_message,
                confidence=confidence,
                show_fallback=show_fallback,
                microsoft_list_url=settings.microsoft_list_url if show_fallback else None,
                sources=["Ollama Local LLM"],
            )

        except requests.exceptions.ConnectionError:
            # Ollama not running
            return ChatResponse(
                response="The local AI service isn't running. Please start Ollama or check the HR resources list for help.",
                confidence=0.0,
                show_fallback=True,
                microsoft_list_url=settings.microsoft_list_url,
                sources=[],
            )
        except Exception as e:
            # Fallback response on error
            return ChatResponse(
                response=f"I'm having trouble processing your request right now. Please check the HR resources list for assistance.",
                confidence=0.0,
                show_fallback=True,
                microsoft_list_url=settings.microsoft_list_url,
                sources=[],
            )


# Singleton instance
chatbot_service = ChatbotService()
