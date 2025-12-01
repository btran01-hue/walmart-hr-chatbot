# 🚀 SUPER SIMPLE Setup - 2 Commands!

**Get your chatbot running in 2 minutes with just 2 commands!**

---

## ⚡ **Just 2 Steps!**

### **Step 1: Install Streamlit** (1 minute)

```bash
cd C:\Users\btran\walmart-hr-chatbot
pip install streamlit python-dotenv openai
```

### **Step 2: Run the Chatbot!** (30 seconds)

```bash
streamlit run simple_chatbot.py
```

**That's it!** 🎉

Your browser will automatically open with the chatbot!

---

## 🎯 **What You Get:**

- ✅ **Simple UI** - Clean chat interface
- ✅ **FAQ Answers** - Instant responses for common questions
- ✅ **AI Powered** - Uses your OpenAI API key from `.env`
- ✅ **Fallback Links** - Shows Microsoft List when needed
- ✅ **No npm** - No frontend build needed!
- ✅ **No complex setup** - Just Python!

---

## 📝 **Test Questions:**

Try asking:
- "What is PTO?"
- "How do I check my benefits?"
- "Tell me about Live Better U"
- "What's the pay schedule?"

---

## 🔧 **How It Works:**

1. Reads your `.env` file from `backend/.env`
2. Uses your OpenAI API key
3. Checks FAQ database first (instant answers)
4. Falls back to OpenAI for other questions
5. Shows Microsoft List link when confidence is low

---

## 🐛 **Troubleshooting:**

### **"No module named 'streamlit'"**
```bash
pip install streamlit python-dotenv openai
```

### **"OpenAI API key not configured"**
- Make sure you created the `.env` file in `backend/` folder
- Make sure your API key is in there
- The chatbot will still work with FAQ-only mode!

### **Can't access the page**
- Streamlit will show you the URL (usually http://localhost:8501)
- Copy/paste that URL into your browser

### **At Walmart (proxy issues)**
```bash
set HTTP_PROXY=http://sysproxy.wal-mart.com:8080
set HTTPS_PROXY=http://sysproxy.wal-mart.com:8080
pip install streamlit python-dotenv openai
```

---

## ⏸️ **To Stop the Chatbot:**

Press `Ctrl + C` in the terminal

---

## 🔄 **To Restart:**

```bash
streamlit run simple_chatbot.py
```

---

## 🎓 **What's Different from the Full Version?**

| Feature | Full Version | Simple Version |
|---------|--------------|----------------|
| Setup Time | 30+ min | 2 min |
| Commands | 10+ | 2 |
| Files | 31 files | 1 file |
| npm needed | Yes | No |
| Frontend build | Yes | No |
| Features | Same | Same |

---

## ✅ **You're Done!**

Just run:
```bash
cd C:\Users\btran\walmart-hr-chatbot
pip install streamlit python-dotenv openai
streamlit run simple_chatbot.py
```

Enjoy your chatbot! 🐶🎾
