# 🐶 Super Simple Setup - No Azure Needed!

**Get your HR chatbot running in 5 minutes with regular OpenAI or run it locally for FREE!**

---

## ⚡ **Option 1: Regular OpenAI (Easiest - 5 Minutes)**

### Why This is Easier:
- ✅ No enterprise approvals needed
- ✅ Sign up and get API key in 2 minutes
- ✅ Pay-as-you-go (super cheap: ~$0.15 per 1000 messages)
- ✅ Same powerful GPT-4 models
- ✅ Works from anywhere (no VPN needed)

### **Step 1: Get OpenAI API Key** (2 minutes)

1. Go to **https://platform.openai.com/**
2. Click **Sign up** (or log in if you have an account)
3. Go to **API Keys** section
4. Click **"Create new secret key"**
5. **Copy the key** (starts with `sk-...`)
   - ⚠️ Save it somewhere safe! You can't see it again!

### **Step 2: Set Up Backend** (2 minutes)

```bash
cd walmart-hr-chatbot/backend

# Copy the simple config
copy .env.simple .env  # Windows
cp .env.simple .env    # Mac/Linux
```

**Edit `.env` file and add your API key:**

```env
USE_AZURE_OPENAI=false
OPENAI_API_KEY=sk-proj-abc123...  # Your actual key here!
OPENAI_MODEL=gpt-4o-mini
```

**That's it for config!** The rest of the settings are already set.

### **Step 3: Run the App** (1 minute)

```bash
# Make sure you're in the backend directory
cd walmart-hr-chatbot/backend

# Activate virtual environment (if not already)
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Run backend
uvicorn main:app --reload
```

**New terminal for frontend:**

```bash
cd walmart-hr-chatbot/frontend
npm run dev
```

### **Step 4: Open in Browser**

👉 **http://localhost:3000**

**That's it! You're done!** 🎉

---

## 🏠 **Option 2: Run Locally with Ollama (100% Free!)**

### Why Run Locally:
- ✅ **Completely FREE** - no API costs ever
- ✅ **Private** - data never leaves your computer
- ✅ **Works offline** - no internet needed
- ✅ **No API keys** - nothing to configure
- ⚠️ Slower than cloud APIs
- ⚠️ Needs decent computer (8GB+ RAM recommended)

### **Step 1: Install Ollama** (3 minutes)

**Windows:**
```bash
# Download and install from:
https://ollama.com/download/windows
```

**Mac:**
```bash
# Download and install from:
https://ollama.com/download/mac
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### **Step 2: Download a Model** (5 minutes)

```bash
# Download a small, fast model (1.5GB)
ollama pull llama3.2:3b

# OR download a larger, smarter model (4GB)
ollama pull llama3.2
```

### **Step 3: Test Ollama**

```bash
# Make sure it's working
ollama run llama3.2:3b "Hello, how are you?"
```

You should get a response!

### **Step 4: Modify Backend for Ollama**

Create a new file `walmart-hr-chatbot/backend/chatbot_service_ollama.py`:

```python
"""Chatbot service using local Ollama."""

import requests
from knowledge_base import get_system_prompt, search_faq
from models import ChatMessage, ChatResponse
from config import settings


class ChatbotService:
    """Service for handling chatbot interactions with Ollama."""

    def __init__(self):
        """Initialize Ollama client."""
        self.ollama_url = "http://localhost:11434/api/chat"
        self.model = "llama3.2:3b"

    def _calculate_confidence(self, response_text: str, message: str) -> float:
        """Calculate confidence score."""
        uncertainty_phrases = [
            "i'm not sure", "i don't know", "unclear",
            "cannot confirm", "recommend contacting",
            "please contact", "check with hr",
        ]
        
        response_lower = response_text.lower()
        if any(phrase in response_lower for phrase in uncertainty_phrases):
            return 0.5
        if len(response_text.split()) < 10:
            return 0.6
        if search_faq(message):
            return 0.95
        return 0.8

    async def get_response(
        self, message: str, conversation_history: list[ChatMessage]
    ) -> ChatResponse:
        """Get chatbot response using Ollama."""
        # Check FAQ first
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
        messages = [{"role": "system", "content": get_system_prompt()}]
        for msg in conversation_history[-10:]:
            messages.append({"role": msg.role, "content": msg.content})
        messages.append({"role": "user", "content": message})

        try:
            # Call Ollama API
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                },
                timeout=30,
            )
            response.raise_for_status()
            
            result = response.json()
            assistant_message = result["message"]["content"]
            
            confidence = self._calculate_confidence(assistant_message, message)
            show_fallback = confidence < settings.confidence_threshold
            
            return ChatResponse(
                response=assistant_message,
                confidence=confidence,
                show_fallback=show_fallback,
                microsoft_list_url=settings.microsoft_list_url if show_fallback else None,
                sources=["Ollama Local LLM"],
            )

        except Exception as e:
            return ChatResponse(
                response="I'm having trouble right now. Please check the HR resources list.",
                confidence=0.0,
                show_fallback=True,
                microsoft_list_url=settings.microsoft_list_url,
                sources=[],
            )


chatbot_service = ChatbotService()
```

### **Step 5: Update main.py to use Ollama**

In `backend/main.py`, change the import:

```python
# Change this line:
from chatbot_service import chatbot_service

# To this:
from chatbot_service_ollama import chatbot_service
```

### **Step 6: Run It!**

```bash
# Make sure Ollama is running (it should auto-start)
# Run backend
cd backend
uvicorn main:app --reload

# Run frontend (new terminal)
cd frontend
npm run dev
```

**Open http://localhost:3000** - You're running AI locally! 🚀

---

## 🎯 **Option 3: FAQ-Only Mode (No AI at All!)**

### Why FAQ-Only:
- ✅ **Zero cost** - no AI needed
- ✅ **Instant responses** - no API calls
- ✅ **100% reliable** - predefined answers
- ✅ **Great starting point** - add AI later
- ⚠️ Limited to pre-written Q&A

### **How to Enable:**

Edit `backend/chatbot_service.py` and modify `get_response`:

```python
async def get_response(
    self, message: str, conversation_history: list[ChatMessage]
) -> ChatResponse:
    """Get chatbot response - FAQ only mode."""
    # Check FAQ database
    faq_answer = search_faq(message)
    
    if faq_answer:
        return ChatResponse(
            response=faq_answer,
            confidence=0.95,
            show_fallback=False,
            microsoft_list_url=None,
            sources=["FAQ Database"],
        )
    else:
        # No AI fallback - just show the list
        return ChatResponse(
            response="I don't have a specific answer for that question. Please check our HR resources for more information.",
            confidence=0.0,
            show_fallback=True,
            microsoft_list_url=settings.microsoft_list_url,
            sources=["FAQ Database"],
        )
```

Now it only uses the FAQ database in `knowledge_base.py`!

---

## 📊 **Comparison**

| Option | Cost | Speed | Setup Time | Best For |
|--------|------|-------|------------|----------|
| **Regular OpenAI** | ~$0.15/1K msgs | ⚡⚡⚡ Fast | 5 min | Production ready |
| **Ollama (Local)** | $0 Free | ⚡ Medium | 10 min | Privacy, offline |
| **FAQ Only** | $0 Free | ⚡⚡⚡ Instant | 2 min | Simple, predictable |
| **Azure/Element** | Varies | ⚡⚡⚡ Fast | Days/weeks | Enterprise approved |

---

## 🎓 **My Recommendation**

### **For Getting Started Fast:**
1. ✅ Use **Regular OpenAI** (5 min setup, works great)
2. ✅ Test it out, show it to stakeholders
3. ✅ Switch to Azure/Element GenAI later when you have approvals

### **For Zero Cost:**
1. ✅ Use **FAQ-Only Mode** first (add your HR Q&A)
2. ✅ Add **Ollama** when you want AI features
3. ✅ Switch to cloud AI if you need better responses

---

## 🐛 **Troubleshooting**

### OpenAI API Key Not Working

**Check:**
- No quotes around the key in `.env`
- No extra spaces
- Key starts with `sk-`
- You have billing set up (even $5 credit works)

### Ollama Not Responding

**Fix:**
```bash
# Check if Ollama is running
ollama list

# Restart Ollama (Windows - check system tray)
# Mac/Linux:
sudo systemctl restart ollama
```

### Still Getting Errors

**Check backend logs:**
```bash
# Look at the terminal where uvicorn is running
# Errors will show there
```

---

## ✅ **Quick Start Commands**

### Regular OpenAI Setup
```bash
cd walmart-hr-chatbot/backend
cp .env.simple .env
# Edit .env with your OpenAI key
uvicorn main:app --reload

# New terminal:
cd walmart-hr-chatbot/frontend
npm run dev
```

### Ollama Setup
```bash
# Install Ollama from https://ollama.com
ollama pull llama3.2:3b

# Update backend to use Ollama (see instructions above)
cd walmart-hr-chatbot/backend
uvicorn main:app --reload

# New terminal:
cd walmart-hr-chatbot/frontend
npm run dev
```

---

**Any of these options will get you a working chatbot TODAY! Pick the one that sounds easiest to you! 🐶**

Need help with any of these? Let me know! 🎾
