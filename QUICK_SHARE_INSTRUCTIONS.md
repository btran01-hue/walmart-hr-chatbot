# 🚀 Quick Share Instructions - Get Your Team Using the Chatbot!

## Option 1: Share on Your Local Network (5 Minutes!)

This is the **FASTEST** way to let your coworkers test the chatbot.

### Step 1: Find Your Computer's IP Address

```bash
ipconfig
```

Look for **IPv4 Address** - it'll look like: `192.168.1.100` or `10.x.x.x`

Write it down: `_________________`

### Step 2: Update the HTML File

1. Open `chatbot.html` in Notepad
2. Find line 264 (press Ctrl+G and type 264)
3. Change this:
   ```javascript
   const API_URL = 'http://localhost:8000/api/chat';
   ```
   To this (use YOUR IP!):
   ```javascript
   const API_URL = 'http://192.168.1.100:8000/api/chat';  // Your actual IP here!
   ```
4. Save the file (Ctrl+S)

### Step 3: Start Backend for Network Access

```bash
cd walmart-hr-chatbot\backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

⚠️ **Important:** Use `0.0.0.0` not `127.0.0.1` so others can connect!

### Step 4: Share the HTML File

**Option A:** Copy to Shared Drive
```
Copy chatbot.html to: \\LAX2-SHARE\HR-Tools\  (or your network share)
```

**Option B:** Email It
- Attach `chatbot.html` to an email
- Send to your team
- They just open it in Chrome/Edge!

**Option C:** Put on SharePoint
- Upload `chatbot.html` to your SharePoint site
- Share the link

### Step 5: Test It!

1. Open `chatbot.html` from the shared location
2. Ask: "If I leave before my 5th hour, is it half a point?"
3. It should answer correctly! 🎉

---

## Option 2: SharePoint Page (15 Minutes)

### For a More Permanent Solution:

1. **Go to LAX2 SharePoint Site**
   - Navigate to your HR page
   
2. **Create New Page**
   - Click "+ New" → "Page"
   - Choose "Blank" template
   - Title: "LAX2 HR Assistant"

3. **Add Embed Web Part**
   - Click "+" → "Embed"
   - Paste this (update with your server IP):
   ```html
   <iframe src="http://YOUR-SERVER-IP:8000" width="100%" height="600px" frameborder="0"></iframe>
   ```
   - Or add "File viewer" web part and upload chatbot.html

4. **Publish the Page**
   - Click "Publish"
   - Share the link with your team!

---

## Option 3: Microsoft Teams Tab (10 Minutes)

### Add to Your LAX2 Teams Channel:

1. **Open your LAX2 HR Team**
   
2. **Add a New Tab**
   - Click the "+" button at the top
   - Choose "Website"
   
3. **Configure Tab**
   - Name: "HR Assistant"
   - URL: Point to your SharePoint page or network file
   - Click "Save"

4. **Done!**
   - Everyone in the team can now access it!

---

## What Your Team Needs to Know

### Simple Instructions for Users:

```
👋 Welcome to the LAX2 HR Assistant!

How to Use:
1. Open the HR Assistant (chatbot.html or SharePoint page)
2. Type your HR question in the box
3. Press Send or hit Enter
4. Get your answer instantly!

Example Questions:
- "How many points do I get if I leave early?"
- "Do I need to take lunch if I leave at 6th hour?"
- "Can I use PTO for an emergency?"
- "What if I don't have PPTO?"
- "Do I still call off when using PPTO?"

Need Help?
Contact Bronte Tran or submit a request through the HR SharePoint list.
```

---

## Troubleshooting for Users

### "Can't Connect to Server"

**Tell users to check:**
1. Are you on the LAX2 Wi-Fi/network?
2. Is the backend server running? (Check with IT/Bronte)
3. Try refreshing the page (F5)

### "Getting Weird Answers"

**You should:**
1. Check the FAQ document is up to date
2. Restart the backend to reload FAQ
3. Check backend logs for errors

---

## Running 24/7 (For Production)

### If you want it always available:

1. **Request a Dedicated Computer/VM from IT**
   - Explain it's for HR associate support
   - Needs to run Python backend
   
2. **Set Up Auto-Start**
   - Create `start_chatbot.bat`:
   ```batch
   @echo off
   cd C:\walmart-hr-chatbot\backend
   call .venv\Scripts\activate
   uvicorn main:app --host 0.0.0.0 --port 8000
   pause
   ```
   
3. **Add to Windows Startup**
   - Put the .bat file in:
   - `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp`
   - Or use Task Scheduler

4. **Update HTML with Server IP**
   - Use the dedicated server's IP address
   - This stays the same even after reboots

---

## Promotion Ideas

### Let People Know About It:

**Email Announcement:**
```
Subject: 🆕 New! LAX2 HR Assistant Chatbot

Hey Team!

We now have an AI-powered HR Assistant to help answer your questions 24/7!

What it can help with:
✅ Attendance policies (points, PPTO, etc.)
✅ Leave policies  
✅ Benefits questions
✅ And more!

How to access:
[Link to SharePoint page or instructions]

Try asking: "If I leave before my 5th hour, how many points?"

Questions? Contact [Your name]
```

**Teams Announcement:**
- Post in your LAX2 HR channel
- Include screenshot
- Encourage people to try it

**Print Flyer:**
- Put QR code linking to chatbot
- Post in break rooms
- Add to onboarding materials

---

## Next Steps

- [ ] Decide which sharing method to use
- [ ] Update chatbot.html with your server IP
- [ ] Test from another computer
- [ ] Share with 2-3 people first (pilot test)
- [ ] Gather feedback
- [ ] Roll out to full team
- [ ] Create user instructions
- [ ] Monitor usage and update FAQ as needed

---

**Questions? Need help?** I'm here! Just ask! 🐶

Your chatbot is ready to help your team - let's get it out there! 🚀
