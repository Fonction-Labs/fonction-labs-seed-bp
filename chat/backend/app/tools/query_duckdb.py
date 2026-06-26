"""Tool: execute read-only SQL queries against model.duckdb."""

from __future__ import annotations

import json
from pathlib import Path

import duckdb
from agents import RunContextWrapper, function_tool

from app.agents.bp_agent import BPAgentContext

DB_PATH = Path(__file__).resolve().parents[4] / "data" / "processed" / "model.duckdb"


@function_tool(description_override=(
    "Execute a read-only SQL SELECT query against the BP financial model DuckDB database. "
    "Returns results as a JSON array of objects. Use list_tables first to discover the schema."
))
async def query_duckdb(ctx: RunContextWrapper[BPAgentContext], sql: str) -> str:
    """Execute a SELECT query on model.duckdb."""
    sql_stripped = sql.strip().rstrip(";")

    forbidden = ["INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER", "TRUNCATE"]
    first_word = sql_stripped.split()[0].upper() if sql_stripped else ""
    if first_word in forbidden:
        return json.dumps({"error": "Only SELECT queries are allowed."})

    try:
        con = duckdb.connect(str(DB_PATH), read_only=True)
        result = con.execute(sql_stripped).fetchdf()
        con.close()

        if len(result) > 200:
            result = result.head(200)
            truncated = True
        else:
            truncated = False

        records = json.loads(result.to_json(orient="records", date_format="iso"))
        response = {"rows": records, "count": len(records)}
        if truncated:
            response["truncated"] = True
            response["note"] = "Results truncated to 200 rows. Add LIMIT or WHERE to narrow."
        return json.dumps(response, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})
