# 🛠️ DIY Setup - No IT Help Needed!

## You Can Do This Yourself! 🐶

Since IT doesn't know how to help, let's set this up ourselves. It's actually super easy!

---

## 🖥️ **What You Need:**

### **Option 1: Spare Computer at LAX2** (Best!)

Do you have access to:
- Old computer that nobody uses?
- Computer in a back office that stays on?
- Any Windows PC that can stay on 24/7?

✅ **This is the best option!**

### **Option 2: Your Own Laptop** (Works too!)

If no spare computer:
- Use your work laptop
- Keep it plugged in at work
- Set it to never sleep
- Leave it at your desk overnight

### **Option 3: Personal Computer** (If allowed)

- Bring an old laptop/desktop from home
- Keep it at LAX2
- Connect to LAX2 network
- Let it run 24/7

---

## 📋 **Complete DIY Setup (30 Minutes)**

### **Step 1: Prepare the Computer** (5 minutes)

#### **Find/Borrow a Computer:**

Ask around:
- "Hey, do we have any old computers not being used?"
- Check with your manager
- Look in storage/back offices
- Ask IT for old equipment they're retiring

#### **Set It Up:**

1. **Place it somewhere safe:**
   - Not on someone's desk (they'll want to use it!)
   - Secure area (office, back room)
   - Near ethernet cable (wired is better than WiFi)
   - Near power outlet

2. **Connect it:**
   - Plug in power (MUST stay plugged in!)
   - Connect to network (ethernet or WiFi)
   - Login to Windows

---

### **Step 2: Configure Windows to Stay On** (5 minutes)

**On the computer:**

1. **Disable Sleep Mode:**
   ```
   Settings → System → Power & Sleep
   
   When plugged in, PC goes to sleep after: NEVER
   When plugged in, turn off screen after: NEVER
   ```

2. **Disable Auto-Restart:**
   ```
   Settings → Update & Security → Windows Update → Advanced Options
   
   Uncheck: Restart this device as soon as possible when a restart is required
   ```

3. **Set to Auto-Login (Optional but helpful):**
   ```
   Press Windows + R
   Type: netplwiz
   Uncheck: "Users must enter a username and password"
   Click OK
   Enter password
   ```

---

### **Step 3: Copy Chatbot to the Computer** (10 minutes)

**Choose a method:**

#### **Method A: USB Drive** (Easiest)

**On your laptop:**
1. Copy `walmart-hr-chatbot` folder to USB drive
2. Walk to the dedicated computer

**On the dedicated computer:**
1. Plug in USB drive
2. Copy `walmart-hr-chatbot` to `C:\Apps\`
3. Done!

#### **Method B: Network Share**

**On your laptop:**
1. Right-click `walmart-hr-chatbot` folder
2. Properties → Sharing → Share
3. Share with Everyone, Read access
4. Note the network path (e.g., `\\BTRAN-LAPTOP\walmart-hr-chatbot`)

**On the dedicated computer:**
1. Open File Explorer
2. Type in address bar: `\\BTRAN-LAPTOP\walmart-hr-chatbot`
3. Copy the folder to `C:\Apps\`

#### **Method C: OneDrive/SharePoint**

1. Zip the `walmart-hr-chatbot` folder
2. Upload to OneDrive or SharePoint
3. Download on dedicated computer
4. Extract to `C:\Apps\`

---

### **Step 4: Install Python** (5 minutes)

**On the dedicated computer:**

1. **Download Python:**
   - Open browser
   - Go to: https://www.python.org/downloads/
   - Click "Download Python 3.11.x" (or latest)

2. **Install Python:**
   - Run the installer
   - ✅ **IMPORTANT:** Check "Add Python to PATH"
   - ✅ Check "Install for all users"
   - Click "Install Now"
   - Wait for it to finish

3. **Verify it worked:**
   ```cmd
   Open Command Prompt
   Type: python --version
   Should show: Python 3.11.x or higher
   ```

---

### **Step 5: Install Chatbot Dependencies** (5 minutes)

**On the dedicated computer:**

```cmd
# Open Command Prompt as Administrator
# Right-click Start → Command Prompt (Admin)

cd C:\Apps\walmart-hr-chatbot\backend

# Create virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\activate

# Install dependencies (this might take a few minutes)
pip install fastapi uvicorn openai python-dotenv pydantic pydantic-settings httpx python-docx
```

**You'll see:**
```
Collecting fastapi...
Downloading fastapi-x.x.x.whl
...
Successfully installed fastapi uvicorn ...
```

**If it fails due to proxy:**
```cmd
set HTTP_PROXY=http://sysproxy.wal-mart.com:8080
set HTTPS_PROXY=http://sysproxy.wal-mart.com:8080

pip install fastapi uvicorn openai python-dotenv pydantic pydantic-settings httpx python-docx --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

---

### **Step 6: Test It Works** (2 minutes)

**On the dedicated computer:**

```cmd
cd C:\Apps\walmart-hr-chatbot\backend
.venv\Scripts\activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

**You should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
INFO:     Application startup complete.
```

**Test it:**
1. Open browser on that computer
2. Go to: http://localhost:8000/health
3. Should see: `{"status":"healthy","message":"HR Chatbot API is running"}`

✅ **IT WORKS!** Press Ctrl+C to stop (we'll set up auto-start next)

---

## ⚙️ **Make It Start Automatically**

### **Option A: Windows Startup Folder** (Super Easy!)

1. **Copy the start script:**
   ```
   Copy: C:\Apps\walmart-hr-chatbot\START_CHATBOT_SERVICE.bat
   To: C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp
   ```

2. **That's it!** It will start when the computer boots!

3. **Test it:**
   - Restart the computer
   - Wait 1 minute
   - Check if chatbot is running: http://localhost:8000/health

### **Option B: Task Scheduler** (More Reliable)

1. **Open Task Scheduler:**
   - Press Windows key
   - Type "Task Scheduler"
   - Open it

2. **Create Basic Task:**
   - Click "Create Basic Task"
   - Name: LAX2 HR Chatbot
   - Trigger: When the computer starts
   - Action: Start a program
   - Program: `C:\Apps\walmart-hr-chatbot\START_CHATBOT_SERVICE.bat`
   - Finish

3. **Edit the task for more reliability:**
   - Right-click the task → Properties
   - General tab:
     - ✅ Run whether user is logged on or not
     - ✅ Run with highest privileges
   - Settings tab:
     - ✅ If the task fails, restart every 1 minute
     - ✅ Attempt to restart up to 3 times
   - OK (enter password if asked)

---

## 🌐 **Get the Computer's IP Address**

**On the dedicated computer:**

```cmd
ipconfig
```

Look for **IPv4 Address**

Example: `10.123.45.67` or `192.168.1.150`

**Write it down:** `_________________________`

**Important:** Make sure this computer has a **static IP** or you'll have to update chatbot.html every time it changes!

### **How to Set Static IP (If Needed):**

1. **Check current IP:**
   ```
   ipconfig /all
   ```
   Note: IP Address, Subnet Mask, Default Gateway, DNS Servers

2. **Set static IP:**
   ```
   Settings → Network & Internet → Ethernet (or WiFi)
   → Click your connection
   → IP Settings → Edit
   → Choose Manual
   → Enable IPv4
   → Enter the same IP, subnet, gateway, DNS
   → Save
   ```

---

## 🔥 **Configure Windows Firewall**

**On the dedicated computer:**

### **Easy Way (PowerShell):**

```powershell
# Open PowerShell as Administrator
# Right-click Start → Windows PowerShell (Admin)

New-NetFirewallRule -DisplayName "LAX2 HR Chatbot" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```

### **Manual Way:**

1. Search "Windows Defender Firewall"
2. Click "Advanced settings"
3. Click "Inbound Rules" → "New Rule"
4. Port → TCP → Specific local ports: 8000
5. Allow the connection
6. Check all profiles (Domain, Private, Public)
7. Name: LAX2 HR Chatbot
8. Finish

---

## 📱 **Update chatbot.html with New IP**

**On your laptop:**

1. **Run the update script:**
   ```cmd
   cd walmart-hr-chatbot
   UPDATE_CHATBOT_IP.bat
   ```

2. **Enter the dedicated computer's IP**
   (The one you wrote down earlier)

3. **Done!** chatbot.html is updated

---

## ✅ **Test From Another Computer**

**On your laptop or coworker's computer:**

1. Open the updated `chatbot.html`
2. Ask: "If I leave before my 5th hour, how many points?"
3. Should get the correct answer!

✅ **IT WORKS!**

---

## 📧 **Roll Out to Your Team**

**Send this email:**

```
Subject: LAX2 HR Assistant - Now Available 24/7!

Hey team!

Great news! The HR Assistant chatbot is now available 24/7!

How to access:
1. Download the attached chatbot.html file
2. Open it in Chrome or Edge
3. Ask any HR question!

Try asking:
- "How many points if I leave early?"
- "Do I need lunch if I leave at 6th hour?"
- "Can I use PTO for emergencies?"

This is running on a dedicated computer now, so it's 
available anytime - day or night!

Let me know if you have any issues.

Thanks!
[Your Name]
```

**Attach:** The updated `chatbot.html`

---

## 🎯 **Ongoing Maintenance**

### **Check if it's running:**

**On the dedicated computer:**
```cmd
tasklist | findstr python
```

Should show a Python process.

### **Restart if needed:**

1. Go to the dedicated computer
2. Double-click: `C:\Apps\walmart-hr-chatbot\START_CHATBOT_SERVICE.bat`

Or:
1. Restart the computer (it will auto-start)

### **Update FAQ:**

1. Edit your FAQ document on your laptop
2. Copy the updated FAQ to the dedicated computer:
   ```
   Copy to: C:\Apps\walmart-hr-chatbot\People Connect FAQ.docx
   ```
3. Restart the chatbot

---

## 🔧 **Troubleshooting**

### **Problem: Can't connect from other computers**

✅ **Check firewall:**
- Make sure port 8000 is open (see firewall section above)

✅ **Ping the computer:**
```cmd
ping DEDICATED-COMPUTER-IP
```
Should get replies.

✅ **Check if chatbot is running:**
- Go to the dedicated computer
- Open browser: http://localhost:8000/health
- Should see: `{"status":"healthy"}`

### **Problem: Chatbot stops after reboot**

✅ **Check auto-start:**
- Make sure START_CHATBOT_SERVICE.bat is in Startup folder
- Or Task Scheduler task is enabled

### **Problem: Computer keeps going to sleep**

✅ **Disable sleep again:**
- Settings → Power & Sleep → Never
- Make sure it's set to "Never" for both battery and plugged in

---

## 💡 **Pro Tips**

### **Label the Computer:**

Put a note on it:
```
LAX2 HR CHATBOT SERVER
DO NOT TURN OFF!
Contact: [Your Name] if issues
```

### **Document Everything:**

Create a simple document:
```
LAX2 HR Chatbot Server

Location: [Where it is physically]
IP Address: [The IP]
Login: [Username]
Password: [Password - keep secure!]

To restart:
1. Go to the computer
2. Run: C:\Apps\walmart-hr-chatbot\START_CHATBOT_SERVICE.bat

Contact: [Your name/phone]
```

Keep this document somewhere safe!

### **Monitor It:**

Check it once a day:
- Open: http://COMPUTER-IP:8000/health
- Should see: `{"status":"healthy"}`

---

## 📊 **Total Cost: $0**

✅ No IT required
✅ No server costs
✅ Just use existing hardware
✅ 24/7 availability
✅ Professional solution!

---

## ✅ **You're Done!**

### **What you now have:**

✅ Dedicated computer running the chatbot
✅ Auto-starts when computer boots
✅ Available 24/7 to all associates
✅ No dependency on your laptop
✅ No IT help needed!

**Congratulations! You did it yourself! 🎉**

---

## 📋 **Quick Checklist**

- [ ] Found a spare computer or set aside your laptop
- [ ] Disabled sleep mode
- [ ] Copied chatbot files to C:\Apps\walmart-hr-chatbot
- [ ] Installed Python 3.11+
- [ ] Installed dependencies with pip
- [ ] Tested chatbot works (http://localhost:8000/health)
- [ ] Set up auto-start (Startup folder or Task Scheduler)
- [ ] Configured Windows Firewall (port 8000)
- [ ] Got the computer's IP address
- [ ] Set static IP (if needed)
- [ ] Updated chatbot.html with new IP
- [ ] Tested from another computer
- [ ] Labeled the computer "DO NOT TURN OFF"
- [ ] Sent update email to team with new chatbot.html
- [ ] Documented server details for future reference

**All done? You're a star! 🌟**

---

Need help with any step? Just ask! 🐶
