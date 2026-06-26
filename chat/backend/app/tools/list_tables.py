"""Tool: list available DuckDB tables and their columns."""

from __future__ import annotations

import json
from pathlib import Path

import duckdb
from agents import RunContextWrapper, function_tool

from app.agents.bp_agent import BPAgentContext

DB_PATH = Path(__file__).resolve().parents[4] / "data" / "processed" / "model.duckdb"


@function_tool(description_override=(
    "List all tables in the BP model database with their column names and types. "
    "Use this to discover what data is available before writing SQL queries."
))
async def list_tables(ctx: RunContextWrapper[BPAgentContext]) -> str:
    """Return schema information for all tables."""
    try:
        con = duckdb.connect(str(DB_PATH), read_only=True)
        tables = con.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'main' ORDER BY table_name"
        ).fetchall()

        schema = {}
        for (table_name,) in tables:
            columns = con.execute(
                f"SELECT column_name, data_type FROM information_schema.columns "
                f"WHERE table_name = '{table_name}' ORDER BY ordinal_position"
            ).fetchall()
            schema[table_name] = [{"name": col, "type": dtype} for col, dtype in columns]

        con.close()
        return json.dumps(schema, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})
