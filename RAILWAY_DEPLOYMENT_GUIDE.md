# 🚂 Railway Deployment Guide - HR Chatbot

**Deploy your chatbot to the cloud in ~15 minutes!**  
No installs needed. Everything happens in your browser.

---

## 📋 What You'll Need

- A web browser (Chrome, Edge, etc.)
- Your OpenAI API key (optional but recommended)
- ~15 minutes of time

---

## Part 1: Create a GitHub Account (5 minutes)

### Step 1: Go to GitHub

👉 **https://github.com/signup**

### Step 2: Sign up

1. Enter your **email address** (use your personal email, not Walmart email)
2. Create a **password**
3. Choose a **username** (e.g., `btran-lax2` or whatever you like)
4. Complete the puzzle/verification
5. Click **"Create account"**

### Step 3: Verify your email

1. Check your email inbox
2. Click the verification link GitHub sent you
3. You're in! 🎉

---

## Part 2: Upload Your Chatbot Code to GitHub (5 minutes)

### Step 1: Create a new repository

1. Go to **https://github.com/new**
2. Fill in:
   - **Repository name:** `walmart-hr-chatbot`
   - **Description:** `HR Chatbot for Walmart Associates`
   - Select **Private** (keeps your code private)
3. Click **"Create repository"**

### Step 2: Upload your files

1. On the new repo page, click **"uploading an existing file"** link
2. Open File Explorer on your laptop
3. Navigate to `C:\Users\btran\walmart-hr-chatbot`
4. Select ALL files and folders inside (Ctrl+A)
5. Drag and drop them into the GitHub upload area
6. Wait for upload to complete
7. Scroll down and click **"Commit changes"**

> ⚠️ **Important:** Make sure you upload the `backend` and `frontend` folders!

### Step 3: Verify upload

You should see your files listed:
- `backend/` folder
- `frontend/` folder  
- `docker-compose.yml`
- `README.md`
- etc.

---

## Part 3: Deploy to Railway (5 minutes)

### Step 1: Sign up for Railway

👉 **https://railway.app**

1. Click **"Login"** (top right)
2. Click **"Login with GitHub"**
3. Authorize Railway to access your GitHub
4. You're in! 🎉

### Step 2: Create a new project

1. Click **"New Project"** button
2. Click **"Deploy from GitHub repo"**
3. Select your **walmart-hr-chatbot** repository
4. Railway will detect your code!

### Step 3: Deploy the Backend

1. Click **"Add a Service"** → **"GitHub Repo"**
2. Select your repo again
3. Click on the service that appears
4. Go to **"Settings"** tab
5. Set **Root Directory** to: `backend`
6. Set **Start Command** to: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Step 4: Add Environment Variables

1. Click on your backend service
2. Go to **"Variables"** tab
3. Click **"+ New Variable"** and add these:

| Variable | Value |
|----------|-------|
| `USE_AZURE_OPENAI` | `false` |
| `OPENAI_API_KEY` | `sk-your-actual-key-here` |
| `OPENAI_MODEL` | `gpt-4o-mini` |
| `MICROSOFT_LIST_URL` | `https://walmart.sharepoint.com/sites/HR/Lists/Resources` |
| `ALLOWED_ORIGINS` | `*` |
| `CONFIDENCE_THRESHOLD` | `0.7` |

> 💡 Don't have an OpenAI key? Get one at https://platform.openai.com/api-keys

### Step 5: Deploy the Frontend

1. Click **"+ New"** → **"GitHub Repo"**
2. Select your repo again
3. Click on the new service
4. Go to **"Settings"** tab
5. Set **Root Directory** to: `frontend`
6. Set **Build Command** to: `npm install && npm run build`
7. Set **Start Command** to: `npx serve dist -s -l $PORT`

### Step 6: Add Frontend Variables

1. Go to **"Variables"** tab
2. Add:

| Variable | Value |
|----------|-------|
| `VITE_API_URL` | (copy your backend URL from Step 7) |

### Step 7: Get Your URLs

1. Click on your **backend** service
2. Go to **"Settings"** → **"Networking"**
3. Click **"Generate Domain"**
4. Copy the URL (e.g., `https://walmart-hr-chatbot-backend.up.railway.app`)

5. Do the same for **frontend** service
6. Copy that URL (e.g., `https://walmart-hr-chatbot-frontend.up.railway.app`)

### Step 8: Update Frontend Variable

1. Go back to your **frontend** service → **Variables**
2. Set `VITE_API_URL` to your backend URL from Step 7
3. Railway will auto-redeploy!

---

## 🎉 You're Done!

Your chatbot is now live at your frontend URL!

**Share this link with your team:**
```
https://walmart-hr-chatbot-frontend.up.railway.app
```
(Your actual URL will be different)

---

## 📊 Railway Free Tier Limits

- **500 hours/month** of runtime (enough for a small team)
- **1 GB RAM** per service
- **1 GB disk** storage
- **100 GB bandwidth**

For a small team, this is plenty! If you need more, Railway's paid plan is $5/month.

---

## 🔧 Troubleshooting

### "Build failed" error

1. Click on the failed service
2. Click **"View Logs"**
3. Look for the error message
4. Common fixes:
   - Check Root Directory is set correctly
   - Make sure all files were uploaded to GitHub

### "Cannot connect to backend" on frontend

1. Make sure `VITE_API_URL` is set to your backend Railway URL
2. Make sure backend has `ALLOWED_ORIGINS=*`
3. Redeploy frontend after changing variables

### OpenAI errors

1. Verify your `OPENAI_API_KEY` is correct
2. Make sure you have credits in your OpenAI account
3. Check the backend logs for specific error messages

---

## 🔄 Updating Your Chatbot

Whenever you push changes to GitHub, Railway automatically redeploys!

1. Make changes to your local files
2. Go to GitHub.com → Your repo
3. Upload the changed files
4. Railway detects changes and redeploys (takes ~2-3 minutes)

---

## 📞 Quick Links

| Resource | URL |
|----------|-----|
| GitHub Signup | https://github.com/signup |
| Railway | https://railway.app |
| OpenAI API Keys | https://platform.openai.com/api-keys |
| Railway Docs | https://docs.railway.app |

---

## 💰 Cost Summary

| Item | Cost |
|------|------|
| GitHub | FREE |
| Railway (free tier) | FREE |
| OpenAI API | ~$0.15 per 1000 messages |
| **Total** | **Almost free!** |

---

**Questions? Issues?** Check Railway's docs or reach out to Walmart Global Tech!

🐶 Happy deploying!
