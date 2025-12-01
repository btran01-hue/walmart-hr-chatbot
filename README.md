# 🐶 Walmart HR Chatbot

A production-ready, AI-powered chatbot for Walmart associates to get help with HR-related questions including benefits, payroll, leave policies, and more. Built with FastAPI, React, TypeScript, and Azure OpenAI.

## 🌟 Features

### Backend
- 🤖 **Azure OpenAI Integration** - GPT-4 powered responses
- 📚 **Built-in FAQ Database** - Instant answers for common questions
- 🎯 **Confidence Scoring** - Smart fallback when uncertain
- 🔗 **Microsoft List Integration** - Seamless fallback to SharePoint resources
- ⚡ **Fast API** - Built with FastAPI for high performance
- 🛡️ **Type Safety** - Pydantic models for request/response validation

### Frontend
- ♿ **WCAG 2.2 Level AA Compliant** - Full accessibility support
- 📱 **Responsive Design** - Works on mobile, tablet, and desktop
- 🎨 **Walmart Branding** - Uses official Walmart colors
- ⌨️ **Keyboard Navigation** - Full keyboard support
- 💬 **Real-time Chat** - Smooth conversational interface
- 🔊 **Screen Reader Support** - Proper ARIA labels and semantic HTML

## 🛠️ Tech Stack

### Backend
- Python 3.11+
- FastAPI
- Azure OpenAI (GPT-4)
- Pydantic
- Uvicorn

### Frontend
- React 18
- TypeScript
- Vite
- Tailwind CSS
- Lucide React (icons)

## 🚀 Quick Start

### ⚡ **EASIEST WAY - Use Regular OpenAI (5 minutes!)**

**Too hard to set up Azure?** No problem! Use regular OpenAI instead:

1. Get API key from https://platform.openai.com/ (2 min)
2. Follow **SIMPLE_SETUP.md** for step-by-step instructions
3. You're done! 🎉

**Cost:** ~$0.15 per 1000 messages (super cheap!)

---

### 🏠 **100% FREE - Run Locally with Ollama**

Want zero costs? Run AI on your own computer:

1. Install Ollama from https://ollama.com
2. Follow **SIMPLE_SETUP.md** (Ollama section)
3. Completely free, completely private! 🎉

---

### 🏢 **Enterprise Setup - Walmart Element GenAI**

For production at Walmart:

1. Follow **WALMART_SETUP.md**
2. Request access to Element GenAI
3. Enterprise-approved solution

---

### Prerequisites

- Python 3.11+
- Node.js 18+
- uv (Walmart's Python package manager)
- **ONE OF:**
  - Regular OpenAI API key (easiest!) OR
  - Walmart Element GenAI access OR
  - Ollama installed locally (free!) OR
  - Just use FAQ mode (no AI needed!)

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
uv venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
uv pip install -e . --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com

# Configure environment
cp .env.example .env
# Edit .env with your Azure OpenAI credentials

# Run the server
uvicorn main:app --reload
```

The backend will be available at `http://localhost:8000`

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

## ⚙️ Configuration

### Backend Configuration (`.env`)

```env
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4

# Microsoft List URL
MICROSOFT_LIST_URL=https://walmart.sharepoint.com/sites/yoursite/Lists/HRResources

# CORS (add your frontend URL)
ALLOWED_ORIGINS=http://localhost:3000

# Chatbot behavior
CONFIDENCE_THRESHOLD=0.7  # Show fallback if confidence < 0.7
MAX_TOKENS=500
TEMPERATURE=0.7
```

### Frontend Configuration (`.env`)

```env
# Leave empty for local dev (uses Vite proxy)
VITE_API_URL=

# For production, set to your backend URL:
# VITE_API_URL=https://your-backend-api.com
```

## 📚 Project Structure

```
walmart-hr-chatbot/
├── backend/
│   ├── main.py                 # FastAPI app & routes
│   ├── config.py              # Configuration management
│   ├── models.py              # Pydantic models
│   ├── chatbot_service.py     # OpenAI integration
│   ├── knowledge_base.py      # HR knowledge & FAQs
│   ├── pyproject.toml         # Python dependencies
│   ├── .env.example           # Example config
│   └── README.md              # Backend docs
│
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── api.ts             # API client
│   │   ├── types.ts           # TypeScript types
│   │   └── App.tsx            # Root component
│   ├── package.json           # npm dependencies
│   ├── .env.example           # Example config
│   └── README.md              # Frontend docs
│
└── README.md                  # This file
```

## 🎯 How It Works

1. **User asks a question** in the chat interface
2. **Frontend sends request** to backend API
3. **Backend checks FAQ database** for instant answers
4. If no FAQ match, **queries Azure OpenAI GPT-4**
5. **Calculates confidence score** based on response certainty
6. If confidence < threshold, **shows Microsoft List fallback**
7. **Response displayed** in chat with optional fallback banner

## 💬 API Endpoints

### Health Check
```
GET /health
```

### Chat
```
POST /api/chat
```
**Request:**
```json
{
  "message": "How do I check my PTO balance?",
  "conversation_history": []
}
```

**Response:**
```json
{
  "response": "You can check your PTO balance...",
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

## 🛡️ Security Considerations

- 🔐 **API Keys**: Never commit `.env` files
- 🎯 **CORS**: Configure allowed origins properly
- 📝 **Logging**: Sensitive data should not be logged
- 🔒 **Authentication**: Add auth middleware for production
- ⏱️ **Rate Limiting**: Implement rate limiting for API endpoints

## ♿ Accessibility (WCAG 2.2 Level AA)

The frontend is fully compliant with WCAG 2.2 Level AA standards:

- ⌨️ **Keyboard Navigation**: Tab, Enter, Shift+Enter support
- 🔊 **Screen Readers**: ARIA labels, roles, and live regions
- 🎨 **Color Contrast**: Minimum 4.5:1 ratio for all text
- 🎯 **Focus Indicators**: Clear 2px blue focus rings
- 🏷️ **Form Labels**: All inputs properly labeled
- 📱 **Responsive**: Works across all device sizes

## 📝 Customization

### Adding FAQs

Edit `backend/knowledge_base.py`:

```python
FAQ_DATABASE = {
    "pto": "Your answer about PTO...",
    "new_topic": "Your new answer...",
}
```

### Adjusting System Prompt

Edit `HR_KNOWLEDGE_BASE` in `backend/knowledge_base.py` to customize the chatbot's behavior.

### Changing Colors

Edit `frontend/tailwind.config.js`:

```javascript
colors: {
  'walmart-blue': '#0071ce',
  'walmart-yellow': '#ffc220',
}
```

### Confidence Threshold

Adjust `CONFIDENCE_THRESHOLD` in `backend/.env` (default: 0.7)

## 🚀 Deployment

### Backend

1. Set up Azure Web App or container service
2. Configure environment variables (no `.env` file)
3. Use production ASGI server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

### Frontend

1. Build: `npm run build`
2. Deploy `dist/` folder to:
   - Azure Static Web Apps
   - Walmart's internal hosting
   - Any static hosting service

## 🐞 Troubleshooting

### Backend won't start
- Check Python version (3.11+)
- Verify Azure OpenAI credentials in `.env`
- Check if port 8000 is already in use

### Frontend can't connect to backend
- Ensure backend is running on port 8000
- Check CORS settings in backend `.env`
- Verify proxy configuration in `vite.config.ts`

### Low confidence responses
- Expand FAQ database
- Adjust `CONFIDENCE_THRESHOLD`
- Improve system prompt with more context

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
- [WCAG 2.2 Guidelines](https://www.w3.org/WAI/WCAG22/quickref/)
- [Tailwind CSS](https://tailwindcss.com/)

## 🐶 Support

For questions or issues:
- Check the backend and frontend README files
- Search Walmart's internal Confluence
- Contact Walmart Global Tech team

## 📝 License

Internal Walmart Global Tech project.

---

**Built with ❤️ by Walmart Global Tech for Walmart Associates**
