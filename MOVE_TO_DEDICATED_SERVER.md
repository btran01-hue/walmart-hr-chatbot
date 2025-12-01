# 🖥️ Move to Dedicated Server - Step-by-Step Guide

## Overview

This guide will help you move the chatbot from your laptop to a dedicated server so it runs 24/7!

---

## 📋 **Phase 1: Get a Dedicated Computer/Server**

### **Option A: Request a VM from IT (Recommended)**

**Email Template to IT:**

```
Subject: Request for Windows VM - HR Chatbot Application

Hi IT Team,

I'm requesting a Windows virtual machine to host an internal HR chatbot 
application for LAX2 associates.

Requirements:
- Operating System: Windows Server 2019/2022 or Windows 10/11
- RAM: 4GB minimum (8GB preferred)
- Storage: 20GB
- Network: Internal LAX2 network access
- Ports needed: 8000 (HTTP)
- Purpose: Host Python-based HR assistant chatbot for associates
- Availability: 24/7 uptime required
- Access: Remote Desktop access for setup and maintenance

This application will:
- Answer common HR questions for LAX2 associates
- Reduce HR ticket volume
- Provide 24/7 self-service support
- Use internal network only (no external access needed)

Please let me know:
1. Timeline for provisioning
2. Server name/IP address when ready
3. Remote Desktop connection details
4. Any firewall rules I need to request

Thank you!
[Your Name]
LAX2 [Your Title]
```

**What to expect:**
- Response time: 1-5 business days
- You'll get: Server name, IP address, login credentials
- They might ask: What software you need (answer: Python 3.11+)

---

### **Option B: Use a Spare Computer at LAX2**

**Requirements:**
- Computer that can stay on 24/7
- Connected to LAX2 network
- Windows 10/11 or Windows Server
- Located in a secure area (not someone's desk!)

**Where to find one:**
- Check with IT for unused computers
- Old manager workstation that's not being used
- Dedicated computer in server room/closet

---

## 🔧 **Phase 2: Prepare the Server**

### **Step 1: Connect to the Server**

**If it's a VM:**
```
1. Open Remote Desktop Connection (search "mstsc" in Windows)
2. Enter server name or IP: SERVER-NAME or 10.x.x.x
3. Login with credentials IT provided
```

**If it's a physical computer:**
- Just log in directly at the computer

---

### **Step 2: Install Required Software**

#### **A. Install Python**

1. Download Python 3.11+ from:
   - Internal software center (if available)
   - Or: https://www.python.org/downloads/

2. Run installer:
   - ✅ Check "Add Python to PATH"
   - ✅ Check "Install for all users"
   - Click "Install Now"

3. Verify installation:
   ```cmd
   python --version
   ```
   Should show: `Python 3.11.x` or higher

#### **B. Install UV (Python package manager)**

Open PowerShell as Administrator:
```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

Or if that doesn't work:
```cmd
pip install uv
```

---

### **Step 3: Copy Chatbot Files to Server**

#### **Method 1: Network Copy (Easiest)**

**On your laptop:**
```cmd
# Share the folder temporarily
# Right-click walmart-hr-chatbot folder → Properties → Sharing → Share
```

**On the server:**
```cmd
# Create destination folder
mkdir C:\Apps
cd C:\Apps

# Copy from your laptop (replace with your computer name/IP)
xcopy \\YOUR-LAPTOP\walmart-hr-chatbot C:\Apps\walmart-hr-chatbot /E /I
```

#### **Method 2: USB Drive**

1. Copy `walmart-hr-chatbot` folder to USB drive
2. Plug USB into server
3. Copy to `C:\Apps\walmart-hr-chatbot`

#### **Method 3: SharePoint/OneDrive**

1. Zip the `walmart-hr-chatbot` folder
2. Upload to OneDrive or SharePoint
3. Download on the server
4. Extract to `C:\Apps\walmart-hr-chatbot`

---

### **Step 4: Install Python Dependencies**

**On the server:**

```cmd
cd C:\Apps\walmart-hr-chatbot\backend

# Create virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\activate

# Install dependencies
uv pip install fastapi uvicorn openai python-dotenv pydantic pydantic-settings httpx python-docx --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com
```

**Verify it works:**
```cmd
uvicorn main:app --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

Press `Ctrl+C` to stop (we'll set up auto-start next)

---

## ⚙️ **Phase 3: Configure Auto-Start**

### **Create Startup Script**

I'll create this file for you! Save this as:
`C:\Apps\walmart-hr-chatbot\START_CHATBOT_SERVICE.bat`

```batch
@echo off
echo Starting LAX2 HR Chatbot Service...
echo.

cd C:\Apps\walmart-hr-chatbot\backend
call .venv\Scripts\activate

echo ========================================
echo LAX2 HR Chatbot is now running!
echo ========================================
echo.
echo Server will be available at:
echo http://THIS-SERVER-IP:8000
echo.
echo This window must stay open.
echo DO NOT CLOSE THIS WINDOW!
echo.
echo To stop the server, press Ctrl+C
echo ========================================
echo.

uvicorn main:app --host 0.0.0.0 --port 8000 --log-level info

pause
```

---

### **Set Up Windows Task Scheduler (Auto-Start on Boot)**

**On the server:**

1. **Open Task Scheduler:**
   - Press Windows key
   - Type "Task Scheduler"
   - Open it

2. **Create New Task:**
   - Click "Create Task" (not Basic Task)
   - Name: `LAX2 HR Chatbot Service`
   - Description: `Starts the HR Assistant chatbot backend`
   - ✅ Check "Run whether user is logged on or not"
   - ✅ Check "Run with highest privileges"
   - Configure for: Windows 10/Server 2016

3. **Triggers Tab:**
   - Click "New"
   - Begin the task: "At startup"
   - ✅ Check "Enabled"
   - Click OK

4. **Actions Tab:**
   - Click "New"
   - Action: "Start a program"
   - Program/script: `C:\Apps\walmart-hr-chatbot\START_CHATBOT_SERVICE.bat`
   - Start in: `C:\Apps\walmart-hr-chatbot`
   - Click OK

5. **Conditions Tab:**
   - ❌ Uncheck "Start the task only if the computer is on AC power"
   - ❌ Uncheck "Stop if the computer switches to battery power"

6. **Settings Tab:**
   - ✅ Check "Allow task to be run on demand"
   - ✅ Check "If the task fails, restart every: 1 minute"
   - ✅ "Attempt to restart up to: 3 times"
   - Click OK

7. **Enter Password:**
   - Enter the server's administrator password
   - Click OK

**Test it:**
- Right-click the task → "Run"
- Check if chatbot starts
- Open browser: `http://localhost:8000/health`
- Should see: `{"status":"healthy"}`

---

## 🌐 **Phase 4: Get the Server IP Address**

**On the server:**

```cmd
ipconfig
```

Look for **IPv4 Address** under your network adapter.

Example: `10.123.45.67` or `192.168.1.150`

**Write it down:** `_____________________`

This is what you'll use in chatbot.html!

---

## 🔄 **Phase 5: Update chatbot.html**

### **Option A: Use the Script (Easiest)**

**On your laptop:**

1. Update `UPDATE_CHATBOT_IP.bat`
2. Run it
3. Enter the **server IP** (not your laptop IP!)
4. It will update chatbot.html

### **Option B: Manual Update**

**On your laptop:**

1. Open `chatbot.html` in Notepad
2. Press `Ctrl+H` (Find and Replace)
3. Find: `http://192.168.1.100:8000` (your old laptop IP)
4. Replace: `http://10.123.45.67:8000` (new server IP)
5. Click "Replace All"
6. Save

---

## 🔥 **Phase 6: Configure Windows Firewall**

**On the server:**

### **Open PowerShell as Administrator:**

```powershell
# Allow incoming connections on port 8000
New-NetFirewallRule -DisplayName "LAX2 HR Chatbot" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```

Or **manually:**

1. Open "Windows Defender Firewall with Advanced Security"
2. Click "Inbound Rules" → "New Rule"
3. Rule Type: Port
4. Protocol: TCP
5. Port: 8000
6. Action: Allow the connection
7. Profile: Check all (Domain, Private, Public)
8. Name: LAX2 HR Chatbot
9. Finish

---

## ✅ **Phase 7: Test Everything**

### **On the server:**

```cmd
# Start the chatbot
C:\Apps\walmart-hr-chatbot\START_CHATBOT_SERVICE.bat
```

### **On your laptop:**

```cmd
# Test the health endpoint
curl http://SERVER-IP:8000/health
```

Should return:
```json
{"status":"healthy","message":"HR Chatbot API is running"}
```

### **On another computer:**

1. Open the updated `chatbot.html`
2. Ask: "If I leave before my 5th hour, how many points?"
3. Should get correct answer!

---

## 📢 **Phase 8: Update Your Team**

### **Send Update Email:**

```
Subject: ✅ HR Chatbot Now Available 24/7!

Hey Team!

Good news! The HR Assistant chatbot is now running 24/7 on a dedicated server.

What changed:
✅ Now available anytime (not just when my laptop is on)
✅ Faster and more reliable
✅ Same great features!

How to access:
- Use the chatbot.html file I'm attaching (updated version)
- Or access from: [SharePoint link if you set that up]

Nothing else changes - just download and open the new file!

Questions? Let me know!
```

**Attach:** The updated `chatbot.html` with the server IP

---

## 🔧 **Maintenance & Monitoring**

### **Check if it's running:**

```cmd
# On the server
tasklist | findstr uvicorn
```

Should show a Python process running.

### **View logs:**

Logs appear in the Task Scheduler window or the console if running manually.

### **Restart if needed:**

1. Open Task Scheduler
2. Find "LAX2 HR Chatbot Service"
3. Right-click → "End" → "Run"

### **Update FAQ:**

1. Update `C:\Users\btran\Downloads\People Connect FAQ.docx` on YOUR laptop
2. Copy the updated file to the server:
   ```cmd
   copy "C:\Users\btran\Downloads\People Connect FAQ.docx" "C:\Apps\walmart-hr-chatbot\People Connect FAQ.docx"
   ```
3. Restart the chatbot service

---

## 📝 **Troubleshooting**

### **Can't connect from other computers:**

- ✅ Check firewall rule is created
- ✅ Verify server is running: `http://SERVER-IP:8000/health`
- ✅ Ping the server: `ping SERVER-IP`
- ✅ Check if port 8000 is listening: `netstat -an | findstr 8000`

### **Chatbot stops after server reboot:**

- ✅ Verify Task Scheduler task is enabled
- ✅ Check task history in Task Scheduler
- ✅ Make sure task is set to "Run whether user is logged on or not"

### **Getting errors:**

- ✅ Check Python is installed
- ✅ Verify .env file exists in backend folder
- ✅ Check dependencies are installed
- ✅ View logs in Task Scheduler

---

## ✨ **You're Done!**

### **What you now have:**

✅ Chatbot running 24/7 on dedicated server
✅ Auto-starts when server reboots
✅ Accessible to all LAX2 associates
✅ No dependency on your laptop
✅ Professional, production-ready setup!

---

## 📋 **Quick Checklist**

- [ ] Got server from IT or found spare computer
- [ ] Installed Python 3.11+
- [ ] Copied chatbot files to C:\Apps\walmart-hr-chatbot
- [ ] Installed dependencies with uv
- [ ] Created START_CHATBOT_SERVICE.bat
- [ ] Set up Task Scheduler auto-start
- [ ] Configured Windows Firewall
- [ ] Got server IP address
- [ ] Updated chatbot.html with server IP
- [ ] Tested from another computer
- [ ] Sent update email to team
- [ ] Documented server details for future reference

---

Need help with any step? Just ask! 🐶
