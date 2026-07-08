"""Tool: list available DuckDB tables and their columns."""

from __future__ import annotations

import json
from pathlib import Path

import os

import duckdb
from agents import RunContextWrapper, function_tool

from app.agents.bp_agent import BPAgentContext


def _resolve_db_path() -> Path:
    env = os.getenv("DATA_PATH")
    if env:
        return Path(env) / "model.duckdb"
    parts = Path(__file__).resolve().parts
    repo_root = Path(*parts[: len(parts) - 4])
    return repo_root / "data" / "processed" / "model.duckdb"

DB_PATH = _resolve_db_path()


@function_tool(description_override=(
    "List all tables in the BP model database with their column names and types. "
    "Use this to discover what data is available before writing SQL queries."
))
async def list_tables(ctx: RunContextWrapper[BPAgentContext]) -> str:
    try:
        con = duckdb.connect(str(DB_PATH), read_only=True)
        tables = con.execute(
            "SELECT table_name FROM information_schema.tables "
            "WHERE table_schema = 'main' ORDER BY table_name"
        ).fetchall()
        schema = {}
        for (table_name,) in tables:
            cols = con.execute(
                "SELECT column_name, data_type FROM information_schema.columns "
                f"WHERE table_name = '{table_name}' ORDER BY ordinal_position"
            ).fetchall()
            schema[table_name] = [{"name": c, "type": t} for c, t in cols]
        con.close()
        return json.dumps(schema, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})
