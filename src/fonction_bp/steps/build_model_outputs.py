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

    # COGS breakdown monthly.
    cogs_monthly = _rows(con, "SELECT * FROM cogs_monthly ORDER BY month")

    # Gross margin monthly for chart.
    gm_monthly = _rows(con, """
        SELECT r.month, r.year, r.total_revenue, c.total_cogs,
               r.total_revenue - c.total_cogs AS gross_profit,
               CASE WHEN r.total_revenue = 0 THEN NULL
                    ELSE (r.total_revenue - c.total_cogs) / r.total_revenue END AS gross_margin
        FROM revenue_monthly r
        LEFT JOIN cogs_monthly c USING(month)
        ORDER BY r.month
    """)

    # Headcount summary for team growth viz.
    headcount_monthly = _rows(con, "SELECT month, year, total_headcount_equivalent, total_payroll_cost FROM headcount_monthly ORDER BY month")

    # Invoiced revenue breakdown for traction display.
    invoiced_monthly = _rows(con, "SELECT * FROM invoiced_revenue_monthly ORDER BY month")

    vc_yaml = paths.assumptions_dir / "vc_case.yaml"
    raw = {}
    actuals_end_month = None
    if vc_yaml.exists():
        raw = yaml.safe_load(vc_yaml.read_text())
        val = raw.get("model_period", {}).get("actuals_end_month")
        if val:
            actuals_end_month = str(val)

    pricing = raw.get("pricing", {})
    seg_pricing = pricing.get("avg_mrr_per_uc", {})

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
        "invoiced_monthly": invoiced_monthly,
        "quarters": q_rows,
        "year_end_milestones": milestones,
        "delivery_capacity": capacity,
        "cash_monthly": cash,
        "cogs_monthly": cogs_monthly,
        "gross_margin_monthly": gm_monthly,
        "headcount_monthly": headcount_monthly,
        "use_of_funds": use_of_funds,
        "attio_funnel": funnel,
        "key_assumptions": {
            "workshop_fee": pricing.get("workshop_fee_per_new_enterprise_client", 20000),
            "deployment_fee_per_uc": pricing.get("deployment_fee_per_use_case", 40000),
            "deployment_duration_months": pricing.get("deployment_duration_months", 3),
            "fde_billable_day_rate": pricing.get("fde_billable_day_rate", 1150),
            "avg_token_cost_per_uc": pricing.get("avg_token_cost_per_uc_month", 200),
            "segment_pricing": seg_pricing,
            "seed_raise": raw.get("fundraising", {}).get("seed_net_proceeds", 2500000),
        },
        "business_model_phases": [
            {
                "id": "current",
                "name": "Modèle actuel",
                "period": "H1 2026",
                "status": "active",
                "revenue_model": "Service pur — workshops, déploiement custom, FDE facturé",
                "pricing": "Workshop 20k€ + deploy 40k€/UC + FDE 1 150€/j",
                "margin_profile": "~40% (service-heavy)",
                "key_metric": "Revenue de service générée",
            },
            {
                "id": "transition",
                "name": "Modèle transitoire",
                "period": "Sept 2026 → Q3 2027",
                "status": "next",
                "revenue_model": "Abonnement per-UC + service FDE séparé",
                "pricing": f"ETI {seg_pricing.get('ETI', 2000)}€ / GC {seg_pricing.get('GC', 5250)}€ / TGC {seg_pricing.get('TGC', 16250)}€ par UC/mois",
                "margin_profile": "60-75% (mix platform + service)",
                "key_metric": "ARR plateforme + accounts actifs",
            },
            {
                "id": "target",
                "name": "Modèle cible",
                "period": "Q3 2027+",
                "status": "planned",
                "revenue_model": "Abonnement léger + crédits prépayés (usage-based)",
                "pricing": "1 crédit = X tokens, marge ~80%+ sur la couche plateforme",
                "margin_profile": "80%+ (SaaS pure)",
                "key_metric": "Net Revenue Retention > 130%",
            },
        ],
        "unit_economics": [
            {"phase": "Discover", "timing": "3 semaines", "driver": "Workshop cadrage", "assumption": "20k€ / nouveau client"},
            {"phase": "Deploy", "timing": "3 mois", "driver": "Déploiement 0→1", "assumption": "40k€ / use case"},
            {"phase": "Run", "timing": "Post go-live", "driver": "Abonnement plateforme", "assumption": f"ETI {seg_pricing.get('ETI', 2000)}€ – TGC {seg_pricing.get('TGC', 16250)}€ /UC/mois"},
            {"phase": "Expand", "timing": "En continu", "driver": "Expansion UC + upsell segment", "assumption": "Net expansion ~130% NRR cible"},
        ],
        "trajectory": [
            {"year": 2026, "theme": "Deployment proof", "text": "Traction existante 184k€ H1, premier client GC signé, 2 UC en déploiement, levée seed 2.5M€."},
            {"year": 2027, "theme": "Platform transition", "text": "12 comptes activés, 26 UC live, bascule vers l'abonnement récurrent. ARR 1.6M€."},
            {"year": 2028, "theme": "Use case expansion", "text": "30 comptes, 84 UC live, ARR 4.8M€. Levier FDE + self-serve progressif."},
        ],
    }
    save_json(paths.model_outputs_json, dashboard)
    paths.dashboard_data_js.write_text("window.DASHBOARD_DATA = " + json.dumps(dashboard, ensure_ascii=False, indent=2, default=_json_default) + ";\n", encoding="utf-8")
    con.close()
