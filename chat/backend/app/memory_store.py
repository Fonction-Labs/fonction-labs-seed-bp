"""In-memory thread/message store for ChatKit."""

from __future__ import annotations

import uuid
from typing import Any

from chatkit.store import Store, NotFoundError
from chatkit.types import ThreadMetadata


class MemoryStore(Store):
    def __init__(self) -> None:
        self._threads: dict[str, ThreadMetadata] = {}
        self._items: dict[str, list[Any]] = {}

    async def load_threads(self) -> list[ThreadMetadata]:
        return list(self._threads.values())

    async def load_thread(self, thread_id: str) -> ThreadMetadata:
        if thread_id not in self._threads:
            raise NotFoundError(f"Thread {thread_id} not found")
        return self._threads[thread_id]

    async def save_thread(self, thread: ThreadMetadata) -> ThreadMetadata:
        if not thread.id:
            thread.id = str(uuid.uuid4())
        self._threads[thread.id] = thread
        if thread.id not in self._items:
            self._items[thread.id] = []
        return thread

    async def delete_thread(self, thread_id: str) -> None:
        self._threads.pop(thread_id, None)
        self._items.pop(thread_id, None)

    async def load_thread_items(self, thread_id: str) -> list[Any]:
        if thread_id not in self._items:
            raise NotFoundError(f"Thread {thread_id} not found")
        return self._items[thread_id]

    async def add_thread_item(self, thread_id: str, item: Any) -> Any:
        if thread_id not in self._items:
            self._items[thread_id] = []
        self._items[thread_id].append(item)
        return item

    async def save_item(self, thread_id: str, item: Any) -> Any:
        if thread_id not in self._items:
            self._items[thread_id] = []
        # Update existing or append
        for i, existing in enumerate(self._items[thread_id]):
            if getattr(existing, "id", None) == getattr(item, "id", None):
                self._items[thread_id][i] = item
                return item
        self._items[thread_id].append(item)
        return item

    async def load_item(self, thread_id: str, item_id: str) -> Any:
        if thread_id in self._items:
            for item in self._items[thread_id]:
                if getattr(item, "id", None) == item_id:
                    return item
        raise NotFoundError(f"Item {item_id} not found in thread {thread_id}")

    async def delete_thread_item(self, thread_id: str, item_id: str) -> None:
        if thread_id in self._items:
            self._items[thread_id] = [
                i for i in self._items[thread_id] if getattr(i, "id", None) != item_id
            ]

    async def save_attachment(self, attachment_id: str, data: bytes, context: Any = None) -> None:
        pass

    async def load_attachment(self, attachment_id: str, context: Any = None) -> bytes:
        raise NotFoundError(f"Attachment {attachment_id} not found")

    async def delete_attachment(self, attachment_id: str, context: Any = None) -> None:
        pass
