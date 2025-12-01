# 🔄 Switch Between AI Providers

Easy guide to switch between different AI backends.

---

## 🎯 Quick Switch Options

### **1. Regular OpenAI (Easiest)**

**Setup:**
```bash
cp .env.simple .env
```

Edit `.env`:
```env
USE_AZURE_OPENAI=false
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o-mini
```

**No code changes needed!** Just restart the backend.

---

### **2. Azure OpenAI / Walmart Element GenAI**

**Setup:**
```bash
cp .env.example .env
```

Edit `.env`:
```env
USE_AZURE_OPENAI=true
AZURE_OPENAI_ENDPOINT=https://wmtllmgateway.stage.walmart.com/wmtllmgateway
AZURE_OPENAI_API_KEY=your-element-genai-key
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4.1-mini@2025-04-14
AZURE_OPENAI_API_VERSION=2024-10-21
```

**No code changes needed!** Just restart the backend.

---

### **3. Ollama (Local, Free)**

**Setup:**
1. Install Ollama from https://ollama.com
2. Download a model:
   ```bash
   ollama pull llama3.2:3b
   ```

3. Change import in `main.py`:
   ```python
   # Line ~10 in main.py
   # Change from:
   from chatbot_service import chatbot_service
   
   # To:
   from chatbot_service_ollama import chatbot_service
   ```

4. Restart backend - done!

---

### **4. FAQ-Only (No AI)**

**Option A: Modify chatbot_service.py**

In `chatbot_service.py`, replace the `get_response` method:

```python
async def get_response(
    self, message: str, conversation_history: list[ChatMessage]
) -> ChatResponse:
    """Get chatbot response - FAQ only mode."""
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
        return ChatResponse(
            response="I don't have a specific answer for that question. Please check our HR resources for more information.",
            confidence=0.0,
            show_fallback=True,
            microsoft_list_url=settings.microsoft_list_url,
            sources=["FAQ Database"],
        )
```

**Option B: Just expand the FAQ database**

Add more entries to `knowledge_base.py` FAQ_DATABASE!

---

## 📊 Feature Comparison

| Provider | Cost | Speed | Quality | Setup Time |
|----------|------|-------|---------|------------|
| Regular OpenAI | 💵 $0.15/1K | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | 5 min |
| Azure/Element | 💵 Varies | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Days |
| Ollama Local | 🆓 Free | ⚡⚡ | ⭐⭐⭐⭐ | 10 min |
| FAQ Only | 🆓 Free | ⚡⚡⚡ | ⭐⭐⭐ | 2 min |

---

## 👨‍💻 **Recommended Workflow**

### **Phase 1: Development (Use Regular OpenAI)**
```bash
USE_AZURE_OPENAI=false
OPENAI_API_KEY=sk-...
```
- Fast setup
- Works from anywhere
- Easy to test

### **Phase 2: Demo (Use Ollama if cost is a concern)**
```python
# Switch to chatbot_service_ollama
from chatbot_service_ollama import chatbot_service
```
- Zero cost
- Works offline
- Good enough for demos

### **Phase 3: Production (Switch to Element GenAI)**
```bash
USE_AZURE_OPENAI=true
AZURE_OPENAI_ENDPOINT=https://wmtllmgateway.prod.walmart.com/wmtllmgateway
```
- Enterprise approved
- Better security
- Cost tracking

---

## ✅ **Testing Your Switch**

After switching providers:

1. **Restart backend:**
   ```bash
   # Kill uvicorn (Ctrl+C)
   # Restart:
   uvicorn main:app --reload
   ```

2. **Test the health endpoint:**
   ```bash
   curl http://localhost:8000/health
   ```

3. **Send a test message:**
   - Open http://localhost:3000
   - Ask: "What is PTO?"
   - Check if you get a response

4. **Check the logs:**
   - Look at terminal where uvicorn is running
   - Should see "Generated response with confidence: ..."

---

**Pro tip:** Keep multiple `.env` files for different providers:

```bash
.env.openai      # Regular OpenAI
.env.element     # Walmart Element GenAI  
.env.local       # For local testing

# Switch between them:
cp .env.openai .env
```

Easy peasy! 🐶🎾
