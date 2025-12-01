# 🔵 Azure OpenAI Setup Guide for Walmart

Complete guide to setting up Azure OpenAI for the HR Chatbot at Walmart.

---

## 🎯 Option 1: If You Already Have Azure OpenAI Access

Great! Skip to **Step 2** below.

---

## 🎯 Option 2: If You DON'T Have Azure OpenAI Access Yet

### At Walmart, You Need to Request Access

Azure OpenAI is a **gated service** - you can't just create it yourself. Here's how:

#### **Method A: Search Walmart's Confluence for Azure OpenAI Docs**

Walmart likely has internal documentation about requesting Azure OpenAI access:

1. Go to Walmart's Confluence
2. Search for:
   - "Azure OpenAI request"
   - "Azure OpenAI access"
   - "OpenAI service request"
   - "Cognitive Services OpenAI"

#### **Method B: Contact Walmart Azure Team**

1. **Find your Azure admin** - Check with your team lead or manager
2. **Submit a service request** - Use Walmart's internal ticketing system
3. **Justify the use case** - Explain you're building an HR chatbot for associates

#### **Method C: Use Existing Walmart Azure OpenAI Resource**

Walmart might already have Azure OpenAI resources provisioned:

1. Ask your team if there's a **shared Azure OpenAI resource**
2. Check Walmart's internal Azure portal for existing resources
3. Get the credentials from whoever manages it

#### **What to Include in Your Request:**

```
Subject: Azure OpenAI Access Request for HR Chatbot

Purpose: Building an AI-powered HR chatbot for Walmart associates
Use Case: Answer common HR questions (benefits, PTO, payroll)
Model Needed: GPT-4 or GPT-3.5-Turbo
Expected Usage: ~1000 requests/day initially
Business Justification: Reduce HR support ticket volume, improve associate experience
Cost Center: [Your cost center]
```

---

## 📋 Step 1: Request Azure OpenAI Access (if needed)

If you need to request access yourself:

### Apply for Azure OpenAI Access

1. **Go to the application form:**
   - https://aka.ms/oai/access

2. **Fill out the form:**
   - Company: Walmart Inc.
   - Use case: HR chatbot for employee support
   - Business email: your.email@walmart.com

3. **Wait for approval** (can take 1-2 weeks)

> **Note:** At Walmart, this might be handled by your Azure admin team instead!

---

## 📋 Step 2: Create Azure OpenAI Resource

Once you have access:

### Using Azure Portal (GUI)

1. **Go to Azure Portal:**
   - https://portal.azure.com
   - Sign in with your Walmart credentials

2. **Create Resource:**
   - Click "Create a resource"
   - Search for "Azure OpenAI"
   - Click "Create"

3. **Fill in the details:**
   ```
   Subscription: [Your Walmart subscription]
   Resource Group: Create new → "walmart-hr-chatbot-rg"
   Region: East US (or whatever's available)
   Name: walmart-hr-chatbot-openai
   Pricing Tier: Standard S0
   ```

4. **Review + Create:**
   - Click "Review + create"
   - Click "Create"
   - Wait for deployment (1-2 minutes)

### Using Azure CLI (Terminal)

```bash
# Login to Azure
az login

# Set your subscription (if you have multiple)
az account set --subscription "Your-Walmart-Subscription"

# Create resource group
az group create \
  --name walmart-hr-chatbot-rg \
  --location eastus

# Create Azure OpenAI resource
az cognitiveservices account create \
  --name walmart-hr-chatbot-openai \
  --resource-group walmart-hr-chatbot-rg \
  --kind OpenAI \
  --sku S0 \
  --location eastus
```

---

## 📋 Step 3: Deploy a Model

You need to deploy a model (like GPT-4) to actually use it.

### Using Azure Portal

1. **Go to your OpenAI resource:**
   - Navigate to your resource in Azure Portal
   - Or search for "walmart-hr-chatbot-openai"

2. **Go to Model Deployments:**
   - Click "Model deployments" in the left sidebar
   - Click "Create new deployment"

3. **Deploy GPT-4:**
   ```
   Select a model: gpt-4 (or gpt-35-turbo if GPT-4 not available)
   Deployment name: gpt-4
   Model version: Latest (e.g., 0613)
   Deployment type: Standard
   Tokens per minute rate limit: 10K (adjust based on needs)
   ```

4. **Click "Create"**
   - Wait for deployment (1-2 minutes)

### Using Azure CLI

```bash
# List available models
az cognitiveservices account deployment list \
  --name walmart-hr-chatbot-openai \
  --resource-group walmart-hr-chatbot-rg

# Deploy GPT-4
az cognitiveservices account deployment create \
  --name walmart-hr-chatbot-openai \
  --resource-group walmart-hr-chatbot-rg \
  --deployment-name gpt-4 \
  --model-name gpt-4 \
  --model-version "0613" \
  --model-format OpenAI \
  --sku-capacity 10 \
  --sku-name "Standard"
```

---

## 📋 Step 4: Get Your Credentials

Now get the info you need for your `.env` file!

### Using Azure Portal

1. **Go to your OpenAI resource**
   - Navigate to "walmart-hr-chatbot-openai"

2. **Click "Keys and Endpoint" (left sidebar)**

3. **Copy these values:**
   - **Endpoint:** `https://walmart-hr-chatbot-openai.openai.azure.com/`
   - **Key 1:** `abc123...` (click "Show" to reveal)
   - **Location/Region:** `eastus` (or whatever you chose)

4. **Note your deployment name:**
   - Go to "Model deployments"
   - Copy the deployment name (e.g., "gpt-4")

### Using Azure CLI

```bash
# Get endpoint
az cognitiveservices account show \
  --name walmart-hr-chatbot-openai \
  --resource-group walmart-hr-chatbot-rg \
  --query "properties.endpoint" \
  --output tsv

# Get API key
az cognitiveservices account keys list \
  --name walmart-hr-chatbot-openai \
  --resource-group walmart-hr-chatbot-rg \
  --query "key1" \
  --output tsv
```

---

## 📋 Step 5: Configure Your Backend

Now put those credentials in your `.env` file!

```bash
cd backend
cp .env.example .env
```

Edit `.env` with these values:

```env
# From Step 4 - Keys and Endpoint
AZURE_OPENAI_ENDPOINT=https://walmart-hr-chatbot-openai.openai.azure.com/
AZURE_OPENAI_API_KEY=your-actual-api-key-here

# From Step 3 - your deployment name
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4

# API version (use this one, it's stable)
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Your Microsoft List URL
MICROSOFT_LIST_URL=https://walmart.sharepoint.com/sites/yoursite/Lists/HRResources

# CORS (for local dev)
ALLOWED_ORIGINS=http://localhost:3000

# Chatbot settings
CONFIDENCE_THRESHOLD=0.7
MAX_TOKENS=500
TEMPERATURE=0.7
```

---

## 📋 Step 6: Test It!

```bash
# Make sure you're in the backend directory
cd backend

# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Run the backend
uvicorn main:app --reload
```

**Test the health check:**

Open browser → http://localhost:8000/health

Should see:
```json
{
  "status": "healthy",
  "message": "HR Chatbot API is running"
}
```

**Test the API docs:**

Open browser → http://localhost:8000/docs

You should see the FastAPI interactive docs!

**Test a chat request:**

1. Go to http://localhost:8000/docs
2. Click on `POST /api/chat`
3. Click "Try it out"
4. Use this request:
   ```json
   {
     "message": "What is PTO?",
     "conversation_history": []
   }
   ```
5. Click "Execute"
6. Should get a response about PTO!

---

## 🐛 Troubleshooting Common Issues

### ❌ "Resource not found" or 404 Error

**Problem:** Endpoint URL is wrong

**Solution:**
```bash
# Check your endpoint in Azure Portal
# Should look like: https://YOUR-RESOURCE-NAME.openai.azure.com/
# NOT: https://api.openai.com/  (that's regular OpenAI, not Azure!)
```

### ❌ "Invalid API key" or 401 Error

**Problem:** API key is wrong or has extra spaces

**Solution:**
```bash
# In .env file, make sure there are NO quotes around the key
# WRONG:
AZURE_OPENAI_API_KEY="abc123"

# RIGHT:
AZURE_OPENAI_API_KEY=abc123

# Also check for extra spaces
```

### ❌ "Deployment not found" Error

**Problem:** Deployment name doesn't match

**Solution:**
```bash
# Check your deployment name in Azure Portal
# Go to Model deployments → copy the exact name
# It's case-sensitive!

# Update .env:
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4  # Use YOUR deployment name
```

### ❌ "Rate limit exceeded" Error

**Problem:** Too many requests

**Solution:**
```bash
# Increase the rate limit in Azure Portal:
# 1. Go to your deployment
# 2. Click "Edit deployment"
# 3. Increase "Tokens per minute rate limit"
# 4. Save

# Or add retry logic in your code (already included!)
```

### ❌ "Cannot connect" at Walmart

**Problem:** Proxy/firewall blocking Azure

**Solution:**
```bash
# Set Walmart proxy for this terminal session:
# Windows (PowerShell):
$env:HTTPS_PROXY="http://sysproxy.wal-mart.com:8080"
$env:HTTP_PROXY="http://sysproxy.wal-mart.com:8080"

# Windows (CMD):
set HTTPS_PROXY=http://sysproxy.wal-mart.com:8080
set HTTP_PROXY=http://sysproxy.wal-mart.com:8080

# Mac/Linux:
export HTTPS_PROXY=http://sysproxy.wal-mart.com:8080
export HTTP_PROXY=http://sysproxy.wal-mart.com:8080

# Then run uvicorn again
```

### ❌ Can't access Azure Portal at Walmart

**Problem:** Need VPN or specific network

**Solution:**
- Connect to Walmart VPN if working remotely
- Use a Walmart workstation
- Contact IT if still blocked

---

## 🆘 Still Stuck? Try These

### Option A: Use a Different Azure Subscription

If Walmart's Azure has restrictions:

1. Use a personal Azure account (free trial)
2. Get Azure OpenAI access for that account
3. Use it for development
4. Switch to Walmart's Azure for production later

### Option B: Use Regular OpenAI (Temporary)

While waiting for Azure access, you can use regular OpenAI:

1. **Get OpenAI API key:**
   - Go to https://platform.openai.com/
   - Sign up / login
   - Create API key

2. **Modify `backend/chatbot_service.py`:**

```python
# Change this:
from openai import AzureOpenAI
self.client = AzureOpenAI(...)

# To this:
from openai import OpenAI
self.client = OpenAI(api_key="your-openai-api-key")

# In get_response(), change:
response = self.client.chat.completions.create(
    model="gpt-4",  # Instead of deployment_name
    messages=messages,
    ...
)
```

3. **Update .env:**
```env
OPENAI_API_KEY=sk-...
```

### Option C: Ask on Walmart's Internal Channels

- Post in Walmart's internal Slack/Teams
- Search Confluence for "Azure OpenAI"
- Contact the Azure admin team
- Ask your manager for help

---

## 📞 Need More Help?

Let me know:
- What error message you're seeing
- What step you're stuck on
- Whether you have Azure OpenAI access
- If you're on Walmart network/VPN

I'll help you get unstuck! 🐶

---

**Once you get this working, the rest is smooth sailing! 🚀**
