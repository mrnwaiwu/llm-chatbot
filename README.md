# Sage &mdash; LLM Chatbot

A conversational AI assistant built with FastAPI and Claude (Anthropic). Includes a streaming browser UI and a REST API.

## Features

- Multi-turn conversation with session memory
- **Streaming responses** — tokens appear in real-time in the browser UI
- Anthropic prompt caching on the system prompt to reduce token costs
- Browser UI at `/` — no frontend framework needed
- Both streaming (`/chat/stream`) and non-streaming (`/chat`) endpoints
- `/history`, `/clear`, and `/sessions` management endpoints

## Quick Start

```bash
git clone https://github.com/mrnwaiwu/llm-chatbot.git
cd llm-chatbot
pip install -r requirements.txt
cp .env.example .env   # add your ANTHROPIC_API_KEY
uvicorn main:app --reload
```

Open `http://localhost:8000` to chat. API docs at `http://localhost:8000/docs`.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Browser chat UI |
| POST | `/chat` | Send a message, receive full response |
| POST | `/chat/stream` | Stream response via SSE |
| GET | `/history/{session_id}` | Full message history |
| POST | `/clear` | Clear a session |
| GET | `/sessions` | List active sessions |

### Streaming via API

```bash
curl -N -X POST http://localhost:8000/chat/stream \
  -H 'Content-Type: application/json' \
  -d '{"session_id": "demo", "message": "Explain recursion"}'
```

```
data: {"text": "Rec"}
data: {"text": "ursion"}
data: {"text": " is..."}
...
data: {"done": true}
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | — | Required. Get one at console.anthropic.com |
| `MODEL` | `claude-sonnet-4-6` | Claude model to use |
| `MAX_TOKENS` | `1024` | Max tokens per response |
