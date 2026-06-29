"""FastAPI entrypoint for the BP Chat backend."""

from __future__ import annotations

import logging
import os
import traceback

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse, Response

from chatkit.server import StreamingResult, NonStreamingResult

from app.auth import require_auth
from app.memory_store import MemoryStore
from app.server import BPChatServer

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("bp_chat")

app = FastAPI(title="BP Chat Backend")

_raw_origins = os.getenv("ALLOWED_ORIGINS", "*")
_origins = [o.strip() for o in _raw_origins.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

store = MemoryStore()
server = BPChatServer(store=store)


@app.post("/chatkit", dependencies=[Depends(require_auth)])
async def chatkit_endpoint(request: Request):
    body = await request.body()
    logger.info("→ /chatkit request: %s", body[:500])
    try:
        result = await server.process(body, context=None)
        logger.info("← result type: %s", type(result).__name__)

        if isinstance(result, StreamingResult):
            async def log_stream():
                try:
                    async for chunk in result:
                        logger.debug("  stream chunk (%d bytes)", len(chunk))
                        yield chunk
                except Exception as e:
                    logger.error("STREAM ERROR: %s", traceback.format_exc())
                    raise

            return StreamingResponse(
                log_stream(),
                media_type="text/event-stream",
                headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
            )
        logger.info("  non-streaming result: %s", type(result).__name__)
        if isinstance(result, NonStreamingResult):
            return Response(content=result.json, media_type="application/json")
        return Response(content=b"{}", media_type="application/json")

    except Exception:
        logger.error("CHATKIT ERROR:\n%s", traceback.format_exc())
        return JSONResponse(status_code=500, content={"error": traceback.format_exc()})


@app.get("/health")
async def health():
    return {"status": "ok"}
