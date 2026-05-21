# Sage &mdash; LLM Chatbot

A conversational AI assistant built with FastAPI and Claude (Anthropic). Includes a clean browser-based chat UI and a REST API.

## Features

- Multi-turn conversation with session memory
- Anthropic prompt caching on the system prompt to reduce token costs
- Browser UI — no extra dependencies (pure HTML/CSS/JS)
- REST API for programmatic access
- `/history`, `/clear`, and `/sessions` management endpoints

## Quick Start

```bash
# Clone and install
git clone https://github.com/mrnwaiwu/llm-chatbot.git
cd llm-chatbot
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Run
uvicorn main:app --reload
```

Open `http://localhost:8000` in your browser to chat.  
API docs at `http://localhost:8000/docs`.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Browser chat UI |
| POST | `/chat` | Send a message, get a reply |
| GET | `/history/{session_id}` | Full message history |
| POST | `/clear` | Clear a session |
| GET | `/sessions` | List active sessions |

### Chat via API

```bash
curl -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"session_id": "demo", "message": "Explain recursion simply"}'
```

```json
{
  "session_id": "demo",
  "response": "Recursion is when a function calls itself...",
  "usage": { "input_tokens": 142, "output_tokens": 87 }
}
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | — | Required. Get one at console.anthropic.com |
| `MODEL` | `claude-sonnet-4-6` | Claude model to use |
| `MAX_TOKENS` | `1024` | Max tokens per response |
