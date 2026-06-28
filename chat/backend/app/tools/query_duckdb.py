"""Tool: execute read-only SQL queries against model.duckdb."""

from __future__ import annotations

import json
from pathlib import Path

import duckdb
from agents import RunContextWrapper, function_tool

from app.agents.bp_agent import BPAgentContext

# Relative to this file: backend/app/tools/ → up 4 levels → repo root → data/processed/
DB_PATH = Path(__file__).resolve().parents[4] / "data" / "processed" / "model.duckdb"


@function_tool(description_override=(
    "Execute a read-only SQL SELECT query against the BP financial model DuckDB database. "
    "Returns results as a JSON array of objects. Use list_tables first to discover the schema."
))
async def query_duckdb(ctx: RunContextWrapper[BPAgentContext], sql: str) -> str:
    sql_stripped = sql.strip().rstrip(";")
    first_word = sql_stripped.split()[0].upper() if sql_stripped else ""
    if first_word in {"INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER", "TRUNCATE"}:
        return json.dumps({"error": "Only SELECT queries are allowed."})
    try:
        con = duckdb.connect(str(DB_PATH), read_only=True)
        cursor = con.execute(sql_stripped)
        columns = [d[0] for d in cursor.description]
        rows = cursor.fetchmany(200)
        has_more = len(rows) == 200 and cursor.fetchone() is not None
        con.close()
        records = [dict(zip(columns, row)) for row in rows]
        response: dict = {"rows": records, "count": len(records)}
        if has_more:
            response["truncated"] = True
            response["note"] = "Results truncated to 200 rows."
        return json.dumps(response, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})
