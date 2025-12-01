# 🚀 Deployment Guide - Walmart HR Chatbot

This guide covers deploying the HR Chatbot to production environments at Walmart.

## 📋 Pre-Deployment Checklist

### Backend
- [ ] Azure OpenAI resource provisioned
- [ ] API keys securely stored (Azure Key Vault recommended)
- [ ] Microsoft List URL configured
- [ ] CORS origins set to production frontend URL
- [ ] Environment variables configured
- [ ] FAQ database reviewed and updated
- [ ] Tests passing (`pytest`)

### Frontend
- [ ] Backend API URL configured
- [ ] Build tested locally (`npm run build`)
- [ ] Accessibility tested (keyboard nav, screen readers)
- [ ] All WCAG 2.2 Level AA requirements verified
- [ ] Mobile responsive design tested
- [ ] Browser compatibility tested

## 🏢 Deployment Options

### Option 1: Azure (Recommended for Walmart)

#### Backend: Azure App Service

1. **Create App Service:**
```bash
az webapp create \
  --resource-group walmart-hr-chatbot-rg \
  --plan walmart-hr-chatbot-plan \
  --name walmart-hr-chatbot-api \
  --runtime "PYTHON:3.11"
```

2. **Configure environment variables:**
```bash
az webapp config appsettings set \
  --resource-group walmart-hr-chatbot-rg \
  --name walmart-hr-chatbot-api \
  --settings \
    AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/" \
    AZURE_OPENAI_API_KEY="@Microsoft.KeyVault(SecretUri=...)" \
    AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4" \
    MICROSOFT_LIST_URL="https://walmart.sharepoint.com/..." \
    ALLOWED_ORIGINS="https://your-frontend.azurestaticapps.net"
```

3. **Deploy:**
```bash
cd backend
az webapp up --name walmart-hr-chatbot-api
```

4. **Configure startup command:**
```bash
az webapp config set \
  --resource-group walmart-hr-chatbot-rg \
  --name walmart-hr-chatbot-api \
  --startup-file "uvicorn main:app --host 0.0.0.0 --port 8000"
```

#### Frontend: Azure Static Web Apps

1. **Build the frontend:**
```bash
cd frontend
npm run build
```

2. **Deploy to Azure Static Web Apps:**
```bash
az staticwebapp create \
  --name walmart-hr-chatbot-frontend \
  --resource-group walmart-hr-chatbot-rg \
  --source ./dist \
  --location "Central US"
```

3. **Configure environment variable:**
```bash
az staticwebapp appsettings set \
  --name walmart-hr-chatbot-frontend \
  --setting-names VITE_API_URL="https://walmart-hr-chatbot-api.azurewebsites.net"
```

### Option 2: Docker Containers

#### Backend Dockerfile

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy dependencies
COPY pyproject.toml ./

# Install uv and dependencies
RUN pip install uv && \
    uv pip install --system -e . \
    --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple \
    --allow-insecure-host pypi.ci.artifacts.walmart.com

# Copy application
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Frontend Dockerfile

Create `frontend/Dockerfile`:

```dockerfile
# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

Create `frontend/nginx.conf`:

```nginx
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

#### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - AZURE_OPENAI_ENDPOINT=${AZURE_OPENAI_ENDPOINT}
      - AZURE_OPENAI_API_KEY=${AZURE_OPENAI_API_KEY}
      - AZURE_OPENAI_DEPLOYMENT_NAME=${AZURE_OPENAI_DEPLOYMENT_NAME}
      - MICROSOFT_LIST_URL=${MICROSOFT_LIST_URL}
      - ALLOWED_ORIGINS=http://localhost:80
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    environment:
      - VITE_API_URL=http://localhost:8000
    depends_on:
      - backend
    restart: unless-stopped
```

Deploy:
```bash
docker-compose up -d
```

## 🔒 Security Best Practices

### 1. API Key Management

**Use Azure Key Vault:**

```bash
# Create Key Vault
az keyvault create \
  --name walmart-hr-chatbot-kv \
  --resource-group walmart-hr-chatbot-rg

# Store API key
az keyvault secret set \
  --vault-name walmart-hr-chatbot-kv \
  --name openai-api-key \
  --value "your-api-key"

# Reference in App Service
AZURE_OPENAI_API_KEY="@Microsoft.KeyVault(SecretUri=https://walmart-hr-chatbot-kv.vault.azure.net/secrets/openai-api-key)"
```

### 2. HTTPS Only

Ensure all production endpoints use HTTPS:

```bash
az webapp update \
  --resource-group walmart-hr-chatbot-rg \
  --name walmart-hr-chatbot-api \
  --https-only true
```

### 3. Authentication (Optional)

Add Azure AD authentication for associate-only access:

```python
# In main.py
from fastapi_azure_auth import SingleTenantAzureAuthorizationCodeBearer

azure_scheme = SingleTenantAzureAuthorizationCodeBearer(
    app_client_id="your-client-id",
    tenant_id="walmart-tenant-id",
    scopes=["api://your-app-id/access"],
)

@app.post("/api/chat", dependencies=[Depends(azure_scheme)])
async def chat(request: ChatRequest):
    # ...
```

### 4. Rate Limiting

Add rate limiting to prevent abuse:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/chat")
@limiter.limit("10/minute")
async def chat(request: ChatRequest):
    # ...
```

## 📊 Monitoring & Logging

### Application Insights

```bash
# Create Application Insights
az monitor app-insights component create \
  --app walmart-hr-chatbot-insights \
  --location centralus \
  --resource-group walmart-hr-chatbot-rg

# Get instrumentation key
az monitor app-insights component show \
  --app walmart-hr-chatbot-insights \
  --resource-group walmart-hr-chatbot-rg \
  --query instrumentationKey
```

Add to backend:

```python
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging

logger.addHandler(AzureLogHandler(
    connection_string='InstrumentationKey=your-key'
))
```

### Key Metrics to Monitor

- API response times
- Error rates
- Azure OpenAI token usage
- User session counts
- Confidence score distributions
- Fallback trigger rates

## 🔄 CI/CD Pipeline

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy HR Chatbot

on:
  push:
    branches: [ main ]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install uv
          uv pip install -e .
      
      - name: Run tests
        run: |
          cd backend
          pytest
      
      - name: Deploy to Azure
        uses: azure/webapps-deploy@v2
        with:
          app-name: walmart-hr-chatbot-api
          publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install and build
        run: |
          cd frontend
          npm ci
          npm run build
      
      - name: Deploy to Azure Static Web Apps
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          action: "upload"
          app_location: "frontend"
          output_location: "dist"
```

## 🧪 Production Testing

Before going live:

1. **Load Testing:**
```bash
# Using Apache Bench
ab -n 1000 -c 10 https://your-backend-api.azurewebsites.net/api/chat
```

2. **Accessibility Testing:**
- Use NVDA/JAWS screen readers
- Test keyboard navigation
- Run axe DevTools audit
- Verify WCAG 2.2 Level AA compliance

3. **Browser Testing:**
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## 📱 Mobile Considerations

- Ensure responsive design works on all devices
- Test on iOS and Android
- Verify touch targets are at least 44x44px
- Check performance on slower connections

## 🔧 Maintenance

### Regular Tasks

- **Weekly:** Review logs and error rates
- **Monthly:** Update FAQ database based on common questions
- **Quarterly:** Review and update Azure OpenAI model version
- **As needed:** Adjust confidence threshold based on feedback

### Scaling

If traffic increases:

```bash
# Scale up App Service
az appservice plan update \
  --name walmart-hr-chatbot-plan \
  --resource-group walmart-hr-chatbot-rg \
  --sku P1V2

# Scale out (add instances)
az appservice plan update \
  --name walmart-hr-chatbot-plan \
  --resource-group walmart-hr-chatbot-rg \
  --number-of-workers 3
```

## 🆘 Troubleshooting Production Issues

### Backend not responding

1. Check App Service logs:
```bash
az webapp log tail \
  --name walmart-hr-chatbot-api \
  --resource-group walmart-hr-chatbot-rg
```

2. Restart the app:
```bash
az webapp restart \
  --name walmart-hr-chatbot-api \
  --resource-group walmart-hr-chatbot-rg
```

### High error rates

1. Check Application Insights
2. Verify Azure OpenAI quota not exceeded
3. Check CORS configuration
4. Review recent deployments

## 📞 Support Contacts

- **Azure Support:** Internal Walmart Azure team
- **OpenAI Issues:** Azure OpenAI support
- **Application Issues:** Walmart Global Tech team

---

**Ready for production! 🚀**
