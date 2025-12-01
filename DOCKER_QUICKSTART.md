# 🐳 Docker Quick Start - HR Chatbot

**Deploy the chatbot in 5 minutes!** No Azure login needed.

---

## 📋 Prerequisites

1. **Docker Desktop** installed on the server/computer
   - Download: https://www.docker.com/products/docker-desktop/
   - Or on Linux: `sudo apt install docker.io docker-compose`

2. **OpenAI API Key** (optional but recommended)
   - Get one at: https://platform.openai.com/api-keys
   - Cost: ~$0.15 per 1000 messages (super cheap!)
   - Without it, the chatbot will still work with FAQ-only mode

---

## 🚀 Deploy in 3 Steps

### Step 1: Create your `.env` file

```bash
cd walmart-hr-chatbot
copy .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

### Step 2: Build and run

```bash
docker-compose up -d --build
```

This will:
- Build the backend container (Python/FastAPI)
- Build the frontend container (React/Nginx)
- Start both services
- Connect them together

### Step 3: Access the chatbot!

Open your browser to: **http://localhost**

That's it! 🎉

---

## 🌐 Making it Available to Everyone

Once running, other people can access it at:

```
http://YOUR-SERVER-IP
```

To find your server's IP:
- Windows: `ipconfig` (look for IPv4 Address)
- Linux: `hostname -I`

### Example:
If your server IP is `10.20.30.40`, share this link:
```
http://10.20.30.40
```

---

## 📊 Useful Commands

| Command | Description |
|---------|-------------|
| `docker-compose up -d` | Start the chatbot (detached) |
| `docker-compose down` | Stop the chatbot |
| `docker-compose logs -f` | View live logs |
| `docker-compose logs backend` | View backend logs only |
| `docker-compose restart` | Restart all services |
| `docker-compose up -d --build` | Rebuild and restart |

---

## 🔧 Troubleshooting

### "Port 80 is already in use"

Something else is using port 80. Either:
1. Stop that service, OR
2. Change the port in `docker-compose.yml`:
   ```yaml
   ports:
     - "8080:80"  # Changed from 80:80
   ```
   Then access at `http://localhost:8080`

### "Cannot connect to Docker daemon"

Make sure Docker Desktop is running!

### Backend health check failing

Check if OpenAI API key is valid:
```bash
docker-compose logs backend
```

### Frontend shows blank page

Clear browser cache or try incognito mode.

---

## 🔄 Updating the Chatbot

When you make changes to the code:

```bash
docker-compose down
docker-compose up -d --build
```

---

## 🛡️ Production Tips

### Run on Server Boot (Linux)

```bash
sudo systemctl enable docker
```

Docker Compose services with `restart: unless-stopped` will auto-start.

### Run on Server Boot (Windows)

1. Open Docker Desktop settings
2. Enable "Start Docker Desktop when you log in"
3. The containers will restart automatically

### Using a Domain Name

If you have a domain, update nginx to use it:
1. Edit `frontend/nginx.conf`
2. Change `server_name _` to `server_name yourdomain.walmart.com`
3. Rebuild: `docker-compose up -d --build`

---

## 🎯 Architecture

```
┌─────────────────────────────────────────────────┐
│                   YOUR SERVER                    │
│  ┌─────────────────────────────────────────────┐│
│  │              Docker Network                 ││
│  │  ┌─────────────┐      ┌─────────────┐      ││
│  │  │  Frontend   │      │   Backend   │      ││
│  │  │   (Nginx)   │─────▶│  (FastAPI)  │      ││
│  │  │   Port 80   │      │  Port 8000  │      ││
│  │  └─────────────┘      └─────────────┘      ││
│  └─────────────────────────────────────────────┘│
└─────────────────────────────────────────────────┘
              ▲
              │ http://server-ip
              │
        ┌─────┴─────┐
        │   Users   │
        │ (Browser) │
        └───────────┘
```

---

## 💰 Cost Estimate

| Item | Cost |
|------|------|
| Server | Free (use existing Walmart server) |
| Docker | Free |
| OpenAI API | ~$0.15 per 1000 messages |
| **Total** | **Basically free!** |

---

## 🆘 Need Help?

1. Check the logs: `docker-compose logs -f`
2. Restart everything: `docker-compose restart`
3. Nuclear option: `docker-compose down && docker-compose up -d --build`

---

**Happy chatting! 🐶**
