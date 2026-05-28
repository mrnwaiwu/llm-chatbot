# Usage Guide

## Quick Start

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open `http://localhost:8000` in your browser.

## Configuration

Set the following environment variables:

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
| `MODEL` | Claude model to use (default: `claude-sonnet-4-6`) |
| `MAX_TOKENS` | Max tokens per response (default: `2048`) |
| `STREAM` | Enable streaming responses (`true`/`false`) |

## API Endpoints

### POST /chat
Send a chat message.

```json
{
  "message": "Hello, Claude!",
  "history": []
}
```

### GET /health
Returns service health status.

## Notes

- Conversation history is maintained per session via in-memory store
- Token limits are enforced server-side before sending to the API
- All user input is sanitized before prompt construction
