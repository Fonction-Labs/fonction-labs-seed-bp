"""ChatKit server for the BP assistant."""

from __future__ import annotations

from typing import Any, AsyncIterator

from agents import Runner
from chatkit.server import ChatKitServer
from chatkit.agents import AgentContext, stream_agent_response
from chatkit.types import ThreadMetadata, ThreadStreamEvent, UserMessageItem

from app.agents.bp_agent import BPAgentContext, create_bp_agent
from app.tools.query_duckdb import query_duckdb
from app.tools.list_tables import list_tables
from app.tools.read_context import read_context
from app.tools.get_assumptions import get_assumptions


bp_agent = create_bp_agent(tools=[query_duckdb, list_tables, read_context, get_assumptions])


class BPChatServer(ChatKitServer):
    async def respond(
        self,
        thread: ThreadMetadata,
        input_user_message: UserMessageItem | None,
        context: Any,
    ) -> AsyncIterator[ThreadStreamEvent]:
        # Build input for the agent from the new message only
        input_items: list[dict] = []
        if input_user_message is not None:
            text = _extract_text(input_user_message)
            if text:
                input_items = [{"role": "user", "content": text}]

        if not input_items:
            return

        agent_ctx = AgentContext(
            thread=thread,
            store=self.store,
            request_context=context,
        )

        bp_context = BPAgentContext(thread_id=thread.id)

        result = Runner.run_streamed(
            bp_agent,
            input=input_items,
            context=bp_context,
        )

        async for event in stream_agent_response(agent_ctx, result):
            yield event


def _extract_text(item: UserMessageItem) -> str:
    """Extract plain text from a UserMessageItem's content."""
    parts = []
    for block in (item.content or []):
        if hasattr(block, "text"):
            parts.append(block.text)
        elif isinstance(block, dict) and "text" in block:
            parts.append(block["text"])
    return " ".join(parts)
