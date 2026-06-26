"""Small agent that generates thread titles from the first user message."""

from __future__ import annotations

from agents import Agent

title_agent = Agent(
    name="title_generator",
    instructions=(
        "Generate a short title (max 6 words, in French) for a conversation "
        "based on the user's first message. Return only the title, nothing else."
    ),
    model="gpt-5.4-mini",
)
