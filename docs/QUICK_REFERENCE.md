# AI Council - Quick Reference Card

## 🚀 Start the Application

```bash
# Backend (if not running)
cd web_app/backend
python main.py

# Frontend
start web_app/frontend/index.html
```

## 🔑 API Keys Location

```
web_app/backend/.env
```

## 📍 Important URLs

- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Frontend**: web_app/frontend/index.html
- **Status Check**: http://localhost:8000/api/status

## 🧪 Quick Tests

```bash
# Test orchestrator
python test_orchestrator.py

# Test web app
python test_web_app.py

# Test API endpoint
python -c "import requests; print(requests.get('http://localhost:8000/api/status').json())"
```

## 📝 Configuration Files

| File | Purpose |
|------|---------|
| `config/ai_council.yaml` | Main configuration |
| `web_app/backend/.env` | API keys |
| `web_app/backend/requirements.txt` | Dependencies |

## 🎯 Execution Modes

| Mode | Speed | Cost | Quality | Use For |
|------|-------|------|---------|---------|
| Fast | ⚡⚡⚡ | $ | ⭐⭐ | Quick queries |
| Balanced | ⚡⚡ | $$ | ⭐⭐⭐ | Most tasks |
| Best Quality | ⚡ | $$$ | ⭐⭐⭐⭐ | Complex reasoning |

## 💰 Cost Estimates

| Provider | Model | Cost/1K tokens |
|----------|-------|----------------|
| Groq | Llama 3 | $0.0006 |
| Groq | Mixtral | $0.0002 |
| Google | Gemini | $0.0013 |
| OpenAI | GPT-3.5 | $0.002 |
| OpenAI | GPT-4 | $0.03 |

## 🔧 Common Commands

```bash
# Install dependencies
pip install -r web_app/backend/requirements.txt

# Install AI Council
pip install -e .

# Start backend
python web_app/backend/main.py

# Run tests
python test_orchestrator.py
python test_web_app.py

# Check logs
# (View terminal where backend is running)
```

## 📊 API Endpoints

```bash
# Get status
GET http://localhost:8000/api/status

# Process request
POST http://localhost:8000/api/process
Body: {"query": "Your question", "mode": "balanced"}

# Estimate cost
POST http://localhost:8000/api/estimate
Body: {"query": "Your question", "mode": "fast"}

# Analyze trade-offs
POST http://localhost:8000/api/analyze
Body: {"query": "Your question"}
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Backend won't start | `pip install -r web_app/backend/requirements.txt` |
| "API key not configured" | Check `web_app/backend/.env` |
| "401 Unauthorized" | Verify API key is correct |
| Frontend shows "offline" | Ensure backend is running on port 8000 |
| Using mock models | Check backend logs for "Creating real adapter" |

## 📚 Documentation

| File | What It Covers |
|------|----------------|
| `FINAL_SUMMARY.md` | Complete overview |
| `ORCHESTRATOR_GUIDE.md` | Orchestrator usage |
| `WEB_APP_SETUP.md` | 5-minute setup |
| `WEB_APP_COMPLETE.md` | Full web app guide |
| `REAL_AI_SETUP_COMPLETE.md` | Real AI configuration |

## 🎨 Customization

```bash
# Add new model
1. Edit config/ai_council.yaml
2. Add API key to web_app/backend/.env
3. Restart backend

# Change UI colors
Edit web_app/frontend/index.html
Search for: bg-blue-600, bg-purple-600

# Adjust cost limits
Edit config/ai_council.yaml
Set: max_cost_per_request
```

## 🔐 Security Checklist

- [ ] API keys in `.env` (not in code)
- [ ] `.env` in `.gitignore`
- [ ] Never commit API keys
- [ ] Set spending limits in provider dashboards
- [ ] Monitor usage regularly

## 📞 Get Help

1. Check documentation files
2. Review backend terminal logs
3. Test API keys in provider consoles
4. Visit http://localhost:8000/docs
5. Open GitHub issue

## ✅ Quick Health Check

```bash
# 1. Backend running?
curl http://localhost:8000/

# 2. Models available?
curl http://localhost:8000/api/status

# 3. Can process requests?
curl -X POST http://localhost:8000/api/process \
  -H "Content-Type: application/json" \
  -d '{"query":"test","mode":"fast"}'
```

## 🎯 Example Queries

```
"What is quantum computing?"
"Explain recursion with examples"
"Write a Python function for binary search"
"Compare microservices vs monolithic architecture"
"What are the pros and cons of TypeScript?"
```

## 🚦 Status Indicators

| Color | Meaning |
|-------|---------|
| 🟢 Green | Operational |
| 🟡 Yellow | Degraded |
| 🔴 Red | Offline |

---

**Quick Start**: `python web_app/backend/main.py` → Open `web_app/frontend/index.html` → Start chatting!
