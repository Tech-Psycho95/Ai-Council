# AI Council Web Application

A modern web interface for the AI Council multi-agent orchestration system with real AI API integration.

## Features

- 🎨 **Modern UI**: Beautiful, responsive interface built with Vue.js and Tailwind CSS
- 🤖 **Multi-Model Support**: Connect to OpenAI, Anthropic, Google, Groq, and Mistral APIs
- ⚡ **Real-time Chat**: Interactive conversation with AI Council
- 📊 **Cost Analysis**: Real-time cost tracking and trade-off analysis
- 🎯 **Execution Modes**: Fast, Balanced, and Best Quality modes
- 📈 **Performance Metrics**: Track confidence, execution time, and model usage

## Quick Start

### 1. Install Backend Dependencies

```bash
cd web_app/backend
pip install -r requirements.txt
```

### 2. Configure AI APIs

Create a `.env` file in `web_app/backend/`:

```bash
# OpenAI
OPENAI_API_KEY=your_openai_key_here

# Anthropic
ANTHROPIC_API_KEY=your_anthropic_key_here

# Google
GOOGLE_API_KEY=your_google_key_here

# Groq
GROQ_API_KEY=your_groq_key_here

# Mistral
MISTRAL_API_KEY=your_mistral_key_here
```

### 3. Enable Models

Edit `config/ai_council.yaml` (copy from `web_app/config/ai_models.yaml`):

```yaml
models:
  gpt-4:
    enabled: true  # Enable the models you want to use
    provider: openai
    # ... rest of config
```

### 4. Start the Backend

```bash
cd web_app/backend
python main.py
```

The API will be available at `http://localhost:8000`

### 5. Open the Frontend

Simply open `web_app/frontend/index.html` in your browser, or serve it:

```bash
cd web_app/frontend
python -m http.server 3000
```

Then visit `http://localhost:3000`

## API Endpoints

### GET `/api/status`
Get system status and available models

### POST `/api/process`
Process a user request
```json
{
  "query": "Your question here",
  "mode": "balanced"  // fast, balanced, or best_quality
}
```

### POST `/api/estimate`
Estimate cost and time
```json
{
  "query": "Your question here",
  "mode": "balanced"
}
```

### POST `/api/analyze`
Analyze cost-quality trade-offs
```json
{
  "query": "Your question here"
}
```

### WebSocket `/ws`
Real-time communication for streaming responses

## Supported AI Providers

### OpenAI
- GPT-4
- GPT-3.5 Turbo
- **Cost**: $0.03/1K tokens (GPT-4), $0.002/1K tokens (GPT-3.5)
- **Get API Key**: https://platform.openai.com/api-keys

### Anthropic
- Claude 3 Opus
- Claude 3 Sonnet
- **Cost**: $0.015/1K tokens (Opus), $0.003/1K tokens (Sonnet)
- **Get API Key**: https://console.anthropic.com/

### Google
- Gemini Pro
- **Cost**: $0.00125/1K tokens
- **Get API Key**: https://makersuite.google.com/app/apikey

### Groq
- Llama 3 70B
- Mixtral 8x7B
- **Cost**: $0.0006/1K tokens (very fast inference)
- **Get API Key**: https://console.groq.com/

### Mistral
- Mistral Large
- Mistral Medium
- **Cost**: $0.004/1K tokens
- **Get API Key**: https://console.mistral.ai/

## Configuration

### Execution Modes

**Fast Mode**
- Optimized for speed
- Uses faster, cheaper models
- Lower quality threshold
- Best for: Quick queries, simple tasks

**Balanced Mode** (Default)
- Balance of speed and quality
- Standard cost and time
- Good for: Most use cases

**Best Quality Mode**
- Maximum quality
- Uses premium models
- Higher cost and time
- Best for: Complex reasoning, critical tasks

### Cost Limits

Set maximum cost per request in `config/ai_council.yaml`:

```yaml
cost:
  max_cost_per_request: 1.0  # Maximum $1 per request
  currency: USD
  enable_cost_tracking: true
```

## Architecture

```
Frontend (Vue.js)
    ↓
FastAPI Backend
    ↓
AI Council Orchestrator
    ↓
┌─────────────────────────────┐
│  Analysis → Decomposition   │
│  Model Selection → Execution│
│  Arbitration → Synthesis    │
└─────────────────────────────┘
    ↓
Multiple AI APIs (OpenAI, Anthropic, etc.)
```

## Development

### Running Tests

```bash
# Test the orchestrator
python test_orchestrator.py

# Test the API
cd web_app/backend
pytest
```

### Adding New Models

1. Add model configuration to `config/ai_models.yaml`
2. Create adapter in `web_app/backend/ai_adapters.py`
3. Register in the factory

### Customizing the UI

Edit `web_app/frontend/index.html` - it's a single-file Vue.js application with Tailwind CSS.

## Troubleshooting

### "API key not configured"
- Make sure you've created `.env` file with your API keys
- Check that the model is enabled in `config/ai_council.yaml`

### "Connection refused"
- Ensure the backend is running on port 8000
- Check firewall settings

### "CORS error"
- The backend has CORS enabled for all origins
- If using a different port, update `apiUrl` in the frontend

### "Model not available"
- Verify API key is valid
- Check model name matches the provider's API
- Ensure you have credits/quota with the provider

## Production Deployment

### Backend

```bash
# Using Gunicorn
gunicorn web_app.backend.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Using Docker
docker build -t ai-council-backend .
docker run -p 8000:8000 --env-file .env ai-council-backend
```

### Frontend

Deploy the `frontend/index.html` to any static hosting:
- Netlify
- Vercel
- GitHub Pages
- AWS S3 + CloudFront

Update the `apiUrl` in the frontend to point to your production backend.

## Security Notes

- **Never commit API keys** to version control
- Use environment variables for sensitive data
- Implement rate limiting in production
- Add authentication for public deployments
- Monitor API usage and costs

## Cost Optimization

The AI Council automatically optimizes costs by:
- Selecting appropriate models based on task complexity
- Using cheaper models for simple tasks
- Parallel execution to reduce total time
- Caching and reusing results when possible

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: https://github.com/shrixtacy/Ai-Council/issues
- Documentation: See `/docs` folder

---

**Built with ❤️ using AI Council Orchestrator**
