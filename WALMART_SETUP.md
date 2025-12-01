# 🐶 Walmart HR Chatbot - Walmart-Specific Setup

**Updated for Walmart's Element GenAI LLM Gateway**

---

## 🎯 TL;DR - Quick Start

1. **Request access:** https://dx.walmart.com/elementgenai/llm_gateway (choose SANDBOX)
2. **Get your API key** (usually within hours)
3. **Update `.env` file** with your credentials
4. **Run the app!**

---

## 📋 Step 1: Request Element GenAI Access

### Go to the Onboarding Portal

👉 **https://dx.walmart.com/elementgenai/llm_gateway**

### Fill Out the Form

**Choose Environment:**
- ✅ **SANDBOX** - Start here! (Instant access, no approvals needed)
  - Good for: Testing, POC, learning
  - Duration: 60 days
  - No prerequisites
  - ⚠️ Don't use real associate data!

- 🔧 **NON-PROD** - For actual development
  - Needs: APM-ID, SSP (can be draft)

- 🚀 **PROD** - Production only
  - Needs: Approved SSP, TCA, Legal review, etc.

**For this HR chatbot, start with SANDBOX!**

### What You'll Provide

```
Project Name: HR Chatbot for Associates
Use Case: Answer common HR questions (benefits, PTO, payroll)
Model Needed: gpt-4.1-mini (or gpt-4)
Expected Usage: Low volume for testing
Environment: SANDBOX
Authentication: API Key (simplest option)
```

### After Submission

- **SANDBOX:** Usually approved within hours
- You'll receive:
  - API Key
  - Endpoint URL
  - Model deployment names

---

## 📋 Step 2: Configure Your Backend

### Update `.env` File

```bash
cd walmart-hr-chatbot/backend
cp .env.example .env
```

Edit `.env` with your Element GenAI credentials:

```env
# Walmart Element GenAI LLM Gateway
AZURE_OPENAI_ENDPOINT=https://wmtllmgateway.stage.walmart.com/wmtllmgateway
AZURE_OPENAI_API_KEY=your-actual-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4.1-mini@2025-04-14
AZURE_OPENAI_API_VERSION=2024-10-21

# Microsoft List URL (update with your actual SharePoint list)
MICROSOFT_LIST_URL=https://walmart.sharepoint.com/sites/HR/Lists/Resources

# CORS (for local development)
ALLOWED_ORIGINS=http://localhost:3000

# Chatbot settings
CONFIDENCE_THRESHOLD=0.7
MAX_TOKENS=500
TEMPERATURE=0.7
```

### Available Models

Check current models here:  
https://gecgithub01.walmart.com/MLPlatforms/elementGenAI/wiki/Walmart-LLM-Gateway#models-available-via-llm-gateway

Common ones:
- `gpt-4.1-mini@2025-04-14` (good balance of cost/performance)
- `gpt-4@2024-05-13` (more powerful, more expensive)
- `gpt-35-turbo@2024-01-25` (cheaper, faster)

---

## 📋 Step 3: Install & Run

### Backend Setup

```bash
cd backend

# Create virtual environment
uv venv

# Activate it
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Install dependencies
uv pip install -e . --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com

# Run!
uvicorn main:app --reload
```

### Frontend Setup (new terminal)

```bash
cd frontend

# Install dependencies
npm install

# Run!
npm run dev
```

### Open in Browser

👉 **http://localhost:3000**

Try asking:
- "How do I check my PTO balance?"
- "What benefits does Walmart offer?"
- "Tell me about Live Better U"

---

## 🔧 Walmart Network Considerations

### If You're Behind Walmart's Proxy

You might need to set proxy environment variables:

**Windows (PowerShell):**
```powershell
$env:HTTP_PROXY="http://sysproxy.wal-mart.com:8080"
$env:HTTPS_PROXY="http://sysproxy.wal-mart.com:8080"
```

**Windows (CMD):**
```cmd
set HTTP_PROXY=http://sysproxy.wal-mart.com:8080
set HTTPS_PROXY=http://sysproxy.wal-mart.com:8080
```

**Mac/Linux:**
```bash
export HTTP_PROXY=http://sysproxy.wal-mart.com:8080
export HTTPS_PROXY=http://sysproxy.wal-mart.com:8080
```

Then run `uvicorn` again.

### If npm install fails

```bash
npm config set proxy http://sysproxy.wal-mart.com:8080
npm config set https-proxy http://sysproxy.wal-mart.com:8080
npm install
```

---

## 📊 Element GenAI Endpoints

| Environment | Endpoint |
|-------------|----------|
| **SANDBOX** | https://wmtllmgateway.stage.walmart.com/wmtllmgateway |
| **NON-PROD** | https://wmtllmgateway.stage.walmart.com/wmtllmgateway |
| **PROD** | https://wmtllmgateway.prod.walmart.com/wmtllmgateway |

---

## 🆘 Get Help

### Fastest Support: Slack

💬 **#element-genai-support**

This is the official Element GenAI support channel. The team is super responsive!

### Email Support

📧 **ElementGenAISupport@email.wal-mart.com**

### Documentation

📖 **Element GenAI Docs:** https://dx.walmart.com/elementgenai/documentation

📖 **Onboarding Guide:** https://dx.walmart.com/elementgenai/documentation/confluence/1648545176

📖 **Code Examples:** https://gecgithub01.walmart.com/MLPlatforms/elementGenAI/tree/main/examples/llm_gateway

---

## 🐛 Troubleshooting

### ❌ "Invalid API key" Error

**Check:**
1. API key is correct (no extra spaces)
2. Using the right environment endpoint (sandbox vs prod)
3. API key hasn't expired

**Fix:**
```env
# Make sure no quotes around the key!
AZURE_OPENAI_API_KEY=abc123  # Good
AZURE_OPENAI_API_KEY="abc123"  # Bad
```

### ❌ "Deployment not found" Error

**Check:**
1. Deployment name is correct (case-sensitive!)
2. Model is available in your environment
3. You have access to that model

**Fix:**
```env
# Use exact deployment name from Element GenAI
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4.1-mini@2025-04-14
```

### ❌ Connection Timeout

**Cause:** Walmart proxy/firewall

**Fix:** Set proxy environment variables (see above)

### ❌ Rate Limit Error (429)

**Cause:** Too many requests for your quota

**Fix:**
1. **SANDBOX:** Quota is limited, wait a bit
2. **Request higher quota:** Contact #element-genai-support
3. **Consider PTU:** For guaranteed throughput

### ❌ Can't Access dx.walmart.com

**Cause:** Need to be on Walmart network

**Fix:**
1. Connect to Walmart VPN
2. Use a Walmart workstation
3. Contact IT if still blocked

---

## 🚀 Moving to Production

When you're ready to deploy for real:

### 1. Request NON-PROD Access

You'll need:
- **APM-ID** (Application Portfolio Management ID)
- **SSP** (Solution Security Plan) - can be draft

### 2. Test in NON-PROD

Validate everything works with the production-like environment.

### 3. Request PROD Access

You'll need:
- ✅ Approved SSP with AI/ML Model Review
- ✅ TCA (Technical Control Assessment)
- ✅ Legal Review approval
- ✅ Leadership approval for costs
- ✅ Change Request (CRQ)

**Timeline:** Plan 4-6 weeks for all approvals

### 4. Update Environment Variables

Change to production endpoint:
```env
AZURE_OPENAI_ENDPOINT=https://wmtllmgateway.prod.walmart.com/wmtllmgateway
AZURE_OPENAI_API_KEY=your-prod-api-key
```

---

## 💰 Cost Considerations

### PayGo (Pay-As-You-Go)

- 💵 Charged per token (prompt + completion)
- ⚡ No throughput guarantees
- 📊 Good for: Low volume, unpredictable usage

### PTU (Provisioned Throughput Units)

- 💵 Fixed monthly cost
- ⚡ Guaranteed throughput
- 📊 Good for: High volume, predictable usage
- ⏰ Takes ~1 week to provision

**For HR chatbot:** Start with PayGo, move to PTU if usage grows!

---

## 📞 Quick Reference

| Need | Where to Go |
|------|-------------|
| Request access | https://dx.walmart.com/elementgenai/llm_gateway |
| Get help | Slack: #element-genai-support |
| Documentation | https://dx.walmart.com/elementgenai/documentation |
| Code examples | https://gecgithub01.walmart.com/MLPlatforms/elementGenAI |
| Legal review | https://jira.walmart.com/servicedesk/customer/portal/9099 |
| Email support | ElementGenAISupport@email.wal-mart.com |

---

## ✅ Checklist

- [ ] Requested Element GenAI access (SANDBOX)
- [ ] Received API key
- [ ] Updated `.env` file
- [ ] Installed backend dependencies
- [ ] Installed frontend dependencies
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Can send messages and get responses
- [ ] Updated Microsoft List URL

---

**Once you get your API key, you're 5 minutes away from a working chatbot! 🎉**

Let me know if you get stuck! 🐶
