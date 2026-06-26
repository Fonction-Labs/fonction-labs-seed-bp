"""FastAPI entrypoint for the BP Chat backend."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from chatkit.server import StreamingResult

from app.memory_store import MemoryStore
from app.server import BPChatServer

app = FastAPI(title="BP Chat Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

store = MemoryStore()
server = BPChatServer(store=store)


@app.post("/chatkit")
async def chatkit_endpoint(request: Request):
    body = await request.body()
    result = await server.process(body, context=None)

    if isinstance(result, StreamingResult):
        return StreamingResponse(
            result,
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
        )
    return result.json


@app.get("/health")
async def health():
    return {"status": "ok"}
