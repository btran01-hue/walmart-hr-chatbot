# 🚀 Quick Setup Guide - Walmart HR Chatbot

Follow these steps to get your HR chatbot up and running!

## 📦 Step 1: Get Azure OpenAI Credentials

You'll need access to Azure OpenAI. Contact your Walmart Azure admin or:

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your Azure OpenAI resource
3. Get your:
   - Endpoint URL (e.g., `https://your-resource.openai.azure.com/`)
   - API Key (from Keys and Endpoint section)
   - Deployment Name (e.g., `gpt-4`)

## 🔧 Step 2: Backend Setup

### Install Python dependencies

```bash
cd backend

# Create virtual environment with uv
uv venv

# Activate it
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies (using Walmart's PyPI)
uv pip install -e . --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com
```

### Configure environment

```bash
# Copy example config
cp .env.example .env

# Edit .env with your favorite editor
notepad .env  # Windows
vim .env      # Linux/Mac
```

**Fill in these required values:**

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-actual-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
MICROSOFT_LIST_URL=https://walmart.sharepoint.com/sites/HR/Lists/Resources
```

### Test the backend

```bash
# Start the server
uvicorn main:app --reload

# You should see:
# INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Test it:**

Open your browser and go to:
- Health check: http://localhost:8000/health
- API docs: http://localhost:8000/docs

## 🎨 Step 3: Frontend Setup

Open a **NEW terminal** (keep backend running!):

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

You should see:
```
➜  Local:   http://localhost:3000/
```

## 🎉 Step 4: Test It Out!

1. Open http://localhost:3000 in your browser
2. You should see the Walmart HR Assistant chat interface
3. Try asking:
   - "How do I check my PTO balance?"
   - "Tell me about benefits"
   - "What is Live Better U?"

## ✅ Verification Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Can see chat interface
- [ ] Can send messages
- [ ] Getting responses from the bot
- [ ] Microsoft List link shows when appropriate

## 🐞 Common Issues

### "ModuleNotFoundError" in backend

**Solution:**
```bash
# Make sure you're in the virtual environment
cd backend
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Reinstall dependencies
uv pip install -e . --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com
```

### "Cannot connect to backend" in frontend

**Solution:**
1. Make sure backend is running on port 8000
2. Check backend terminal for errors
3. Verify CORS settings in `backend/.env`:
   ```env
   ALLOWED_ORIGINS=http://localhost:3000
   ```

### "Invalid API key" error

**Solution:**
1. Double-check your Azure OpenAI API key in `backend/.env`
2. Make sure there are no extra spaces or quotes
3. Verify the endpoint URL is correct

### Port already in use

**Backend (port 8000):**
```bash
# Use a different port
uvicorn main:app --reload --port 8001

# Update frontend proxy in vite.config.ts
```

**Frontend (port 3000):**
```bash
# Use a different port
npm run dev -- --port 3001
```

### npm install fails at Walmart

**Solution:**
```bash
# Set proxy for npm
npm config set proxy http://sysproxy.wal-mart.com:8080
npm config set https-proxy http://sysproxy.wal-mart.com:8080

# Try again
npm install
```

## 🔒 Security Reminder

**NEVER commit your `.env` file!**

The `.gitignore` is already set up to exclude it, but double-check:

```bash
git status
# Make sure .env is NOT listed
```

## 📚 Next Steps

1. **Customize FAQs**: Edit `backend/knowledge_base.py`
2. **Adjust styling**: Modify `frontend/tailwind.config.js`
3. **Add more features**: Check the main README.md
4. **Test accessibility**: Use keyboard navigation, screen readers
5. **Deploy**: See deployment section in README.md

## 🐶 Need Help?

- Check the main [README.md](./README.md)
- Check backend [README.md](./backend/README.md)
- Check frontend [README.md](./frontend/README.md)
- Search Walmart's Confluence
- Contact Walmart Global Tech team

---

**Happy coding! 🎉 Your HR chatbot is ready to help associates!**
