"""In-memory thread/message store for ChatKit v1.6.x."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from chatkit.store import Store, NotFoundError
from chatkit.types import Page, ThreadMetadata, ThreadItem, Attachment


def _now() -> datetime:
    return datetime.now(timezone.utc)


class MemoryStore(Store):
    def __init__(self) -> None:
        self._threads: dict[str, ThreadMetadata] = {}
        self._items: dict[str, list[ThreadItem]] = {}
        self._attachments: dict[str, Attachment] = {}

    async def load_thread(self, thread_id: str, context: Any) -> ThreadMetadata:
        if thread_id not in self._threads:
            raise NotFoundError(f"Thread {thread_id} not found")
        return self._threads[thread_id]

    async def save_thread(self, thread: ThreadMetadata, context: Any) -> None:
        self._threads[thread.id] = thread
        if thread.id not in self._items:
            self._items[thread.id] = []

    async def load_thread_items(
        self,
        thread_id: str,
        after: str | None,
        limit: int,
        order: str,
        context: Any,
    ) -> Page[ThreadItem]:
        if thread_id not in self._items:
            return Page(data=[], has_more=False)
        items = list(self._items[thread_id])
        if order == "desc":
            items = list(reversed(items))
        if after:
            idx = next((i for i, item in enumerate(items) if item.id == after), None)
            if idx is not None:
                items = items[idx + 1:]
        has_more = len(items) > limit
        items = items[:limit]
        last_id = items[-1].id if items else None
        return Page(data=items, has_more=has_more, after=last_id)

    async def add_thread_item(self, thread_id: str, item: ThreadItem, context: Any) -> None:
        if thread_id not in self._items:
            self._items[thread_id] = []
        self._items[thread_id].append(item)

    async def save_item(self, thread_id: str, item: ThreadItem, context: Any) -> None:
        if thread_id not in self._items:
            self._items[thread_id] = []
        for i, existing in enumerate(self._items[thread_id]):
            if existing.id == item.id:
                self._items[thread_id][i] = item
                return
        self._items[thread_id].append(item)

    async def load_item(self, thread_id: str, item_id: str, context: Any) -> ThreadItem:
        for item in self._items.get(thread_id, []):
            if item.id == item_id:
                return item
        raise NotFoundError(f"Item {item_id} not found in thread {thread_id}")

    async def delete_thread(self, thread_id: str, context: Any) -> None:
        self._threads.pop(thread_id, None)
        self._items.pop(thread_id, None)

    async def delete_thread_item(self, thread_id: str, item_id: str, context: Any) -> None:
        if thread_id in self._items:
            self._items[thread_id] = [
                i for i in self._items[thread_id] if i.id != item_id
            ]

    async def load_threads(
        self,
        limit: int,
        after: str | None,
        order: str,
        context: Any,
    ) -> Page[ThreadMetadata]:
        threads = list(self._threads.values())
        if order == "desc":
            threads = list(reversed(threads))
        if after:
            idx = next((i for i, t in enumerate(threads) if t.id == after), None)
            if idx is not None:
                threads = threads[idx + 1:]
        has_more = len(threads) > limit
        threads = threads[:limit]
        last_id = threads[-1].id if threads else None
        return Page(data=threads, has_more=has_more, after=last_id)

    async def save_attachment(self, attachment: Attachment, context: Any) -> None:
        self._attachments[attachment.id] = attachment

    async def load_attachment(self, attachment_id: str, context: Any) -> Attachment:
        if attachment_id not in self._attachments:
            raise NotFoundError(f"Attachment {attachment_id} not found")
        return self._attachments[attachment_id]

    async def delete_attachment(self, attachment_id: str, context: Any) -> None:
        self._attachments.pop(attachment_id, None)
