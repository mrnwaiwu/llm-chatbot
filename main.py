from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Sage - LLM Chatbot",
    description="Conversational AI assistant powered by Claude, with streaming support",
    version="2.0.0",
)

client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = os.getenv("MODEL", "claude-sonnet-4-6")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))

SYSTEM_PROMPT = """You are Sage, a friendly and knowledgeable AI assistant.
You help users understand complex topics, answer questions, brainstorm ideas,
and have meaningful conversations. Keep responses clear and helpful.
Use examples when they aid understanding."""

# In-memory session store: session_id -> message history
sessions: dict[str, list[dict]] = {}


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ClearRequest(BaseModel):
    session_id: str


@app.get("/")
async def serve_ui():
    return FileResponse("static/index.html")


@app.post("/chat")
async def chat(req: ChatRequest):
    """Send a message and get a complete response (non-streaming)."""
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    history = sessions.setdefault(req.session_id, [])
    history.append({"role": "user", "content": req.message})

    response = await client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=history,
    )

    reply = response.content[0].text
    history.append({"role": "assistant", "content": reply})

    return {
        "session_id": req.session_id,
        "response": reply,
        "usage": {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        },
    }


@app.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    """Stream Claude's response token-by-token using Server-Sent Events."""
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    history = sessions.setdefault(req.session_id, [])
    history.append({"role": "user", "content": req.message})

    # Snapshot history for the stream closure
    history_snapshot = list(history)
    collected: list[str] = []

    async def event_generator():
        async with client.messages.stream(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=[
                {
                    "type": "text",
                    "text": SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=history_snapshot,
        ) as stream:
            async for text in stream.text_stream:
                collected.append(text)
                yield f"data: {json.dumps({'text': text})}\n\n"

        # Persist the full reply once streaming is complete
        full_reply = "".join(collected)
        history.append({"role": "assistant", "content": full_reply})
        yield f"data: {json.dumps({'done': True})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/history/{session_id}")
async def get_history(session_id: str):
    """Return the full message history for a session."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"session_id": session_id, "messages": sessions[session_id]}


@app.post("/clear")
async def clear_session(req: ClearRequest):
    """Clear the conversation history for a session."""
    sessions.pop(req.session_id, None)
    return {"message": f"Session {req.session_id} cleared"}


@app.get("/sessions")
async def list_sessions():
    """List active session IDs and their message counts."""
    return {
        "sessions": [
            {"session_id": sid, "message_count": len(msgs)}
            for sid, msgs in sessions.items()
        ]
    }


app.mount("/static", StaticFiles(directory="static"), name="static")
