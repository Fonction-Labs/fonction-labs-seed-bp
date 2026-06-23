from __future__ import annotations
import json
from pathlib import Path

import duckdb
import yaml

from fonction_bp.config import Paths
from fonction_bp.utils import _json_default, fmt_eur, fmt_pct, save_json


def _rows(con: duckdb.DuckDBPyConnection, query: str) -> list[dict]:
    return [dict(zip([c[0] for c in cur.description], row)) for cur in [con.execute(query)] for row in cur.fetchall()]


def run(paths: Paths, scenario: str = "vc_case") -> None:
    con = duckdb.connect(str(paths.duckdb_path))

    annual = _rows(con, "SELECT * FROM annual_summary ORDER BY year")
    kpis = _rows(con, "SELECT * FROM dashboard_kpis")
    revenue_monthly = _rows(con, "SELECT * FROM revenue_monthly ORDER BY month")
    milestones = _rows(con, "SELECT * FROM year_end_milestones ORDER BY year")
    capacity = _rows(con, "SELECT * FROM delivery_capacity ORDER BY month")
    cash = _rows(con, "SELECT * FROM cash_monthly ORDER BY month")
    use_of_funds = _rows(con, "SELECT *, amount / SUM(amount) OVER () AS share FROM use_of_funds ORDER BY amount DESC")
    funnel = _rows(con, "SELECT * FROM attio_funnel")

    # Selected quarterly data derived explicitly to avoid ambiguity.
    q_rows = _rows(con, "SELECT * FROM quarterly_summary ORDER BY year, quarter")
    for q in q_rows:
        val = con.execute("SELECT ending_arr, enterprise_accounts_end, live_use_cases FROM revenue_monthly WHERE month = ?", [q["quarter_end_month"]]).fetchone()
        q["ending_arr"], q["enterprise_accounts_end"], q["live_use_cases"] = val

    vc_yaml = paths.assumptions_dir / "vc_case.yaml"
    actuals_end_month = None
    if vc_yaml.exists():
        raw = yaml.safe_load(vc_yaml.read_text())
        val = raw.get("actuals_end_month")
        if val:
            actuals_end_month = str(val)

    dashboard = {
        "metadata": {
            "title": "Fonction Labs — Seed BP Dashboard",
            "scenario": "VC Case",
            "model_version": "pipeline_v2",
            "actuals_end_month": actuals_end_month,
            "note": "Dashboard generated from model.duckdb. Excel workbooks are outputs, not source data.",
        },
        "kpis": kpis,
        "annual_summary": annual,
        "revenue_monthly": revenue_monthly,
        "quarters": q_rows,
        "year_end_milestones": milestones,
        "delivery_capacity": capacity,
        "cash_monthly": cash,
        "use_of_funds": use_of_funds,
        "attio_funnel": funnel,
        "unit_economics": [
            {"phase": "Discover", "timing": "3 weeks", "driver": "Workshop fee", "assumption": "10k€ / enterprise client"},
            {"phase": "Deploy", "timing": "3 months", "driver": "0→1 deployment fee", "assumption": "40k€ / use case"},
            {"phase": "Run & Scale", "timing": "After go-live", "driver": "Platform subscription", "assumption": "10k€ / month / live use case"},
            {"phase": "FDE support", "timing": "Optional", "driver": "Billable FDE support", "assumption": "1,150€ / day"},
        ],
        "trajectory": [
            {"year": 2026, "theme": "Deployment proof", "text": "Revenue already generated, first enterprise deployments, platform motion starts."},
            {"year": 2027, "theme": "Platform transition", "text": "Enterprise accounts convert into recurring use case subscriptions."},
            {"year": 2028, "theme": "Use case expansion", "text": "Growth is driven by account expansion and higher FDE leverage."},
        ],
    }
    save_json(paths.model_outputs_json, dashboard)
    paths.dashboard_data_js.write_text("window.DASHBOARD_DATA = " + json.dumps(dashboard, ensure_ascii=False, indent=2, default=_json_default) + ";\n", encoding="utf-8")
    con.close()
