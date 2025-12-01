"""FastAPI application for HR Chatbot."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

from config import settings
from models import ChatRequest, ChatResponse, HealthCheck
from chatbot_service import chatbot_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Walmart HR Chatbot API",
    description="AI-powered chatbot for Walmart HR inquiries",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint."""
    return HealthCheck(
        status="healthy",
        message="HR Chatbot API is running",
    )


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process chat message and return AI response.
    
    Args:
        request: ChatRequest containing user message and conversation history
        
    Returns:
        ChatResponse with AI-generated response and metadata
    """
    try:
        logger.info(f"Received chat request: {request.message[:50]}...")
        
        response = await chatbot_service.get_response(
            message=request.message,
            conversation_history=request.conversation_history,
        )
        
        logger.info(
            f"Generated response with confidence: {response.confidence:.2f}"
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your request",
        )


@app.get("/api/config")
async def get_config():
    """Get public configuration for the frontend."""
    return {
        "microsoft_list_url": settings.microsoft_list_url,
        "confidence_threshold": settings.confidence_threshold,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
