# 🚀 Deployment Guide - Share Your Chatbot!

## Quick Options for Sharing

Here are your options from **easiest to most advanced**:

---

## ⚡ Option 1: Simple HTML File (Easiest - 5 Minutes)

**Best for:** Quick testing with a few people, demos

### What You Need:
1. The `chatbot.html` file
2. Backend running on your computer
3. Users on the same network

### Steps:

**1. Find Your Computer's IP Address:**
```bash
ipconfig
# Look for "IPv4 Address" - something like 192.168.1.100
```

**2. Update the Backend URL in chatbot.html:**

Open `chatbot.html` and find this line (around line 200):
```javascript
const BACKEND_URL = 'http://127.0.0.1:8000';
```

Change it to your IP:
```javascript
const BACKEND_URL = 'http://192.168.1.100:8000';  // Your actual IP
```

**3. Start Backend on Network Interface:**
```bash
cd walmart-hr-chatbot/backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

**4. Share the HTML file:**
- Copy `chatbot.html` to a shared network drive
- Or email it to users
- They open it in their browser!

**Pros:** Super simple, no deployment needed
**Cons:** Only works while your computer is on and running the backend

---

## 📁 Option 2: SharePoint Deployment (Recommended for LAX2)

**Best for:** Permanent deployment accessible to all associates

### Steps:

**1. Prepare the Files:**

Create a standalone HTML file with the backend URL:

```html
<!-- Save as: LAX2_HR_Chatbot.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LAX2 HR Assistant</title>
    <!-- Copy all styles from chatbot.html -->
</head>
<body>
    <!-- Copy all HTML from chatbot.html -->
    <script>
        // Update this to your deployed backend URL
        const BACKEND_URL = 'http://YOUR-SERVER-IP:8000';
        
        // Rest of the JavaScript from chatbot.html
    </script>
</body>
</html>
```

**2. Upload to SharePoint:**

1. Go to your LAX2 SharePoint site
2. Navigate to **Site Contents** → **Site Pages**
3. Click **+ New** → **Web Part Page**
4. Or upload as a file to a document library
5. Add a **Script Editor Web Part**
6. Paste your HTML code

**3. Backend Deployment:**

You need a server to run the backend. Options:
- Use a dedicated Windows computer at LAX2
- Request a VM from IT
- Use Walmart's cloud infrastructure

---

## 🖥️ Option 3: Dedicated Server (Most Reliable)

**Best for:** Production use, many users

### Backend Setup on Windows Server:

**1. Get a Server:**
- Request a Windows VM from Walmart IT
- Or use a spare computer at LAX2

**2. Install Requirements:**
```bash
# Install Python 3.11+
# Download from python.org

# Install uv
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**3. Deploy Backend:**
```bash
# Copy your walmart-hr-chatbot folder to the server
cd C:\Apps\walmart-hr-chatbot\backend

# Install dependencies
uv pip install -r requirements.txt --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com

# Copy your .env file with settings

# Run as a service (keeps running)
uvicorn main:app --host 0.0.0.0 --port 8000
```

**4. Make it Run at Startup:**

Create `start_chatbot_backend.bat`:
```batch
@echo off
cd C:\Apps\walmart-hr-chatbot\backend
call .venv\Scripts\activate
uvicorn main:app --host 0.0.0.0 --port 8000 --log-level info
```

Add to Windows Task Scheduler:
- Run at system startup
- Run whether user is logged in or not

**5. Share with Users:**
- Give them the server IP: `http://SERVER-IP:8000`
- Update `chatbot.html` with this URL
- Host HTML on SharePoint or shared drive

---

## 🌐 Option 4: React Frontend (Most Professional)

**Best for:** Polished, professional interface

### Build and Deploy React App:

**1. Build the Frontend:**
```bash
cd walmart-hr-chatbot/frontend

# Install dependencies
npm install

# Update API URL in src/api.ts
# Change to your backend URL

# Build for production
npm run build
```

**2. Deploy Built Files:**

The `dist` folder contains your app. You can:
- Host on SharePoint
- Host on any web server (IIS, Apache, nginx)
- Copy to a network share

**Example with IIS (Windows):**
1. Install IIS on your server
2. Copy `dist` folder to `C:\inetpub\wwwroot\hr-chatbot`
3. Create new website in IIS Manager
4. Point to the folder
5. Users access via `http://SERVER-NAME/hr-chatbot`

---

## 📱 Option 5: Microsoft Teams Integration

**Best for:** Using within Teams

### Quick Teams Deployment:

**1. Create a Teams Tab:**
1. Go to your LAX2 Teams channel
2. Click **+** to add a tab
3. Choose **Website**
4. Enter your chatbot URL
5. Name it "HR Assistant"

**2. Or use Power Apps:**
1. Create a new Power App
2. Add an **HTML Text** control
3. Embed your chatbot HTML
4. Share the app with your team

---

## 🔧 Configuration for Network Access

### Update CORS Settings:

In `backend/.env`, add your server URL:
```env
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000,http://YOUR-SERVER-IP:8000,https://teams.wal-mart.com
```

### Firewall Rules:

If users can't connect, you may need to:
1. Open port 8000 in Windows Firewall
2. Request IT to allow access
3. Or use a different port (like 80 or 443)

---

## 📊 Recommended Setup for LAX2

**For Quick Start (This Week):**
1. Use Option 1 (Simple HTML)
2. Run backend on your computer during work hours
3. Share HTML file via email or network drive

**For Production (Next Week):**
1. Request a VM or dedicated computer from IT
2. Deploy backend as a service (Option 3)
3. Host HTML on SharePoint (Option 2)
4. Add as a Teams tab (Option 5)

**For Best Experience (When You Have Time):**
1. Build React frontend (Option 4)
2. Deploy to IIS or SharePoint
3. Create Teams app integration
4. Add to OneWalmart portal

---

## 🔒 Security Considerations

### For Internal Use:
- ✅ Backend runs on internal network only
- ✅ No external access needed (unless using OpenAI API)
- ✅ FAQ data stays on your network
- ✅ Use Ollama for 100% offline operation

### For API Keys:
- ⚠️ Keep `.env` file secure
- ⚠️ Don't commit API keys to git
- ⚠️ Consider using Walmart's Element GenAI instead of personal OpenAI key

---

## 📝 Quick Share Checklist

- [ ] Backend is running and accessible
- [ ] Updated `BACKEND_URL` in chatbot.html to server IP
- [ ] Tested from another computer on the network
- [ ] FAQ document is up to date
- [ ] Created documentation for users
- [ ] Shared access instructions with team
- [ ] Set up monitoring/logging (optional)
- [ ] Created backup of FAQ document

---

## 💡 Pro Tips

1. **Start Small:** Test with 5-10 users first
2. **Gather Feedback:** Ask what questions they have
3. **Update FAQ:** Add new Q&As based on feedback
4. **Monitor Usage:** Check backend logs to see what people ask
5. **Promote It:** Create a flyer, send an email, post in Teams

---

## 🆘 Troubleshooting

**"Can't connect to backend"**
- Check firewall settings
- Verify backend is running: `http://SERVER-IP:8000/health`
- Check CORS settings in .env

**"Getting wrong answers"**
- Update FAQ document
- Restart backend to reload FAQ
- Check backend logs for errors

**"Too slow"**
- Consider using Ollama locally
- Or use gpt-3.5-turbo instead of gpt-4
- Check network/proxy settings

---

Need help with any of these options? I'm here to help! 🐶
