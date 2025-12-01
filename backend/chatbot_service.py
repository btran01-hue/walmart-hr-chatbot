"""Chatbot service integrating OpenAI or Azure OpenAI."""

import json
import os
import httpx
from openai import OpenAI, AzureOpenAI
from config import settings
from knowledge_base import get_system_prompt
from models import ChatMessage, ChatResponse


class ChatbotService:
    """Service for handling chatbot interactions."""

    def __init__(self):
        """Initialize OpenAI client (Azure or regular OpenAI)."""
        # Check if we're using Azure or regular OpenAI
        use_azure = os.getenv("USE_AZURE_OPENAI", "true").lower() == "true"
        
        # Configure proxy if needed (for Walmart network)
        http_proxy = os.getenv("HTTP_PROXY")
        https_proxy = os.getenv("HTTPS_PROXY")
        http_client = None
        
        if http_proxy or https_proxy:
            # Create HTTP client with proxy support
            http_client = httpx.Client(
                proxies={
                    "http://": http_proxy,
                    "https://": https_proxy,
                } if http_proxy and https_proxy else None,
                verify=False,  # Disable SSL verification for corporate proxy
            )
        
        if use_azure:
            # Azure OpenAI (Walmart Element GenAI or direct Azure)
            self.client = AzureOpenAI(
                api_key=settings.azure_openai_api_key,
                api_version=settings.azure_openai_api_version,
                azure_endpoint=settings.azure_openai_endpoint,
                http_client=http_client,
            )
            self.deployment_name = settings.azure_openai_deployment_name
            self.use_azure = True
        else:
            # Regular OpenAI (easier setup!)
            self.client = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                http_client=http_client,
            )
            self.deployment_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            self.use_azure = False

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
            "submit your request",
            "sharepoint list",
        ]
        
        response_lower = response_text.lower()
        
        # If response contains uncertainty, lower confidence
        if any(phrase in response_lower for phrase in uncertainty_phrases):
            return 0.5
        
        # If response is very short, might be unsure
        if len(response_text.split()) < 10:
            return 0.6
        
        # If response is specific and detailed, high confidence
        if len(response_text.split()) > 30:
            return 0.85
        
        # Default moderate-high confidence
        return 0.8

    async def get_response(
        self, message: str, conversation_history: list[ChatMessage]
    ) -> ChatResponse:
        """
        Get chatbot response for user message.
        
        Args:
            message: User's question
            conversation_history: Previous conversation messages
            
        Returns:
            ChatResponse with answer and metadata
        """
        # Build messages for OpenAI (FAQ content is now in the system prompt)
        messages = [
            {"role": "system", "content": get_system_prompt()},
        ]

        # Add conversation history
        for msg in conversation_history[-10:]:  # Keep last 10 messages for context
            messages.append({"role": msg.role, "content": msg.content})

        # Add current message
        messages.append({"role": "user", "content": message})

        try:
            # Call OpenAI (Azure or regular)
            if self.use_azure:
                response = self.client.chat.completions.create(
                    model=self.deployment_name,  # Azure uses deployment name
                    messages=messages,
                    max_tokens=settings.max_tokens,
                    temperature=settings.temperature,
                )
            else:
                response = self.client.chat.completions.create(
                    model=self.deployment_name,  # Regular OpenAI uses model name
                    messages=messages,
                    max_tokens=settings.max_tokens,
                    temperature=settings.temperature,
                )

            assistant_message = response.choices[0].message.content or ""
            
            # Calculate confidence
            confidence = self._calculate_confidence(assistant_message, message)
            
            # Determine if we should show fallback
            show_fallback = confidence < settings.confidence_threshold
            
            return ChatResponse(
                response=assistant_message,
                confidence=confidence,
                show_fallback=show_fallback,
                microsoft_list_url=settings.microsoft_list_url if show_fallback else None,
                sources=["OpenAI GPT-4" if not self.use_azure else "Azure OpenAI GPT-4"],
            )

        except Exception as e:
            # Fallback response on error
            return ChatResponse(
                response=f"I'm having trouble processing your request right now. Please submit your question to the LAX2 HR team using the link below, and they will respond to you as soon as possible.",
                confidence=0.0,
                show_fallback=True,
                microsoft_list_url=settings.microsoft_list_url,
                sources=[],
            )


# Singleton instance
chatbot_service = ChatbotService()
