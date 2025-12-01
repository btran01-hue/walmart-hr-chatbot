# Walmart HR Chatbot - Backend

🐶 Backend API service for the Walmart HR Chatbot, built with FastAPI and Azure OpenAI.

## Features

- 🤖 Azure OpenAI GPT-4 integration
- 📚 Built-in FAQ knowledge base
- 🎯 Confidence scoring for responses
- 🔗 Microsoft List fallback for low-confidence answers
- ⚡ Fast, async API with FastAPI
- 🛡️ Type-safe with Pydantic models
- 📝 Comprehensive logging

## Setup

### Prerequisites

- Python 3.11+
- uv (Walmart's Python package manager)
- Azure OpenAI API access

### Installation

1. **Create virtual environment and install dependencies:**

```bash
cd backend
uv venv
# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
uv pip install -e . --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com
```

2. **Configure environment variables:**

```bash
cp .env.example .env
```

Edit `.env` with your Azure OpenAI credentials:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
MICROSOFT_LIST_URL=https://walmart.sharepoint.com/sites/yoursite/Lists/HRResources
```

### Running the Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check

```
GET /health
```

Returns service health status.

### Chat

```
POST /api/chat
```

**Request:**

```json
{
  "message": "How do I check my PTO balance?",
  "conversation_history": [
    {
      "role": "user",
      "content": "Previous message"
    },
    {
      "role": "assistant",
      "content": "Previous response"
    }
  ]
}
```

**Response:**

```json
{
  "response": "You can check your PTO balance on the WalmartOne portal...",
  "confidence": 0.95,
  "show_fallback": false,
  "microsoft_list_url": null,
  "sources": ["FAQ Database"]
}
```

### Get Config

```
GET /api/config
```

Returns public configuration for frontend.

## Project Structure

```
backend/
├── main.py                 # FastAPI application & routes
├── config.py              # Configuration management
├── models.py              # Pydantic models
├── chatbot_service.py     # OpenAI integration logic
├── knowledge_base.py      # HR knowledge & FAQs
├── pyproject.toml         # Dependencies
├── .env.example           # Example environment variables
└── README.md              # This file
```

## Configuration

### Confidence Threshold

The `CONFIDENCE_THRESHOLD` setting (default: 0.7) determines when to show the Microsoft List fallback link. If the chatbot's confidence is below this threshold, it will suggest the user check the Microsoft List.

### Knowledge Base

The FAQ database in `knowledge_base.py` provides instant, high-confidence responses for common questions. Add more FAQs to improve response speed and accuracy.

## Development

### Adding New FAQs

Edit `knowledge_base.py` and add entries to `FAQ_DATABASE`:

```python
FAQ_DATABASE = {
    "your_keyword": "Your answer here",
}
```

### Adjusting System Prompt

Edit `HR_KNOWLEDGE_BASE` in `knowledge_base.py` to customize the chatbot's behavior and knowledge.

## Deployment

For production deployment:

1. Set up proper environment variables (no `.env` file)
2. Use a production ASGI server (uvicorn with workers)
3. Configure proper CORS origins
4. Set up logging to a centralized service
5. Add rate limiting and authentication as needed

## Troubleshooting

### Azure OpenAI Connection Issues

- Verify endpoint URL format
- Check API key validity
- Ensure deployment name matches your Azure resource

### CORS Errors

- Update `ALLOWED_ORIGINS` in `.env` to include your frontend URL

## Support

For issues or questions, contact the Walmart Global Tech team or check internal Confluence docs.
