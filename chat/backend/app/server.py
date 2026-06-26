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
        agent_context_data = BPAgentContext(thread_id=thread.id)

        items = await self.store.load_thread_items(thread.id)
        input_items = self._to_agent_input(items)

        result = Runner.run_streamed(
            bp_agent,
            input=input_items,
            context=agent_context_data,
        )

        agent_ctx = AgentContext(
            thread=thread,
            store=self.store,
            request_context=context,
        )

        async for event in stream_agent_response(agent_ctx, result):
            yield event

    def _to_agent_input(self, items: list) -> list:
        """Convert stored ChatKit items to OpenAI Responses API input format."""
        input_items = []
        for item in items:
            if hasattr(item, "role"):
                if item.role == "user":
                    content = getattr(item, "content", None) or ""
                    if isinstance(content, list):
                        text_parts = [p.get("text", "") for p in content if isinstance(p, dict) and p.get("type") == "text"]
                        content = " ".join(text_parts)
                    input_items.append({"role": "user", "content": content})
                elif item.role == "assistant":
                    content = getattr(item, "content", None) or ""
                    if isinstance(content, list):
                        text_parts = [p.get("text", "") for p in content if isinstance(p, dict) and p.get("type") == "text"]
                        content = " ".join(text_parts)
                    input_items.append({"role": "assistant", "content": content})
        return input_items
