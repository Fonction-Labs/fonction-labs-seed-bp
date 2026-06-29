from __future__ import annotations
import json
from pathlib import Path

import duckdb
import yaml

from fonction_bp.config import Paths
from fonction_bp.utils import _json_default, fmt_eur, fmt_pct, save_json


def _build_headcount_by_function(raw: dict, months: list[str]) -> list[dict]:
    from datetime import date
    hc = raw.get("headcount", {})
    founders = hc.get("founder_count", 3)
    hires = hc.get("hires", [])

    # Map function labels to short keys.
    fn_map = {
        "Product & Engineering": "product_engineering",
        "Forward-Deployed Engineering": "fde",
        "Sales & GTM": "sales_gtm",
        "Ops": "ops",
    }

    # current_roles: cold callers (Sales & GTM) + sales freelance (Sales & GTM)
    current_roles = hc.get("current_roles", {})
    cold_callers_start = date.fromisoformat(str(current_roles.get("cold_callers", {}).get("start_month", "2099-01-01"))[:10])
    cold_callers_end   = date.fromisoformat(str(current_roles.get("cold_callers", {}).get("end_month",   "2099-01-01"))[:10])
    cold_callers_count = int(current_roles.get("cold_callers", {}).get("count", 0))
    sales_fl_start = date.fromisoformat(str(current_roles.get("sales_freelance", {}).get("start_month", "2099-01-01"))[:10])
    sales_fl_end   = date.fromisoformat(str(current_roles.get("sales_freelance", {}).get("end_month",   "2099-01-01"))[:10])

    rows = []
    for month_val in months:
        if isinstance(month_val, date):
            m = month_val
            month_str = month_val.isoformat()
        else:
            month_str = str(month_val)[:10]
            m = date.fromisoformat(month_str)
        counts = {k: 0 for k in fn_map.values()}
        # CDI/freelance hires
        for hire in hires:
            start = date.fromisoformat(str(hire["start_month"])[:10])
            if m >= start:
                fn = fn_map.get(hire.get("function", ""), None)
                if fn:
                    counts[fn] += 1
        # current_roles: cold callers
        if cold_callers_start <= m <= cold_callers_end:
            counts["sales_gtm"] += cold_callers_count
        # current_roles: sales freelance
        if sales_fl_start <= m <= sales_fl_end:
            counts["sales_gtm"] += 1
        rows.append({
            "month": month_str,
            "founders": founders,
            **counts,
        })
    return rows


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
    f_raise = raw.get("fundraising", {}).get("seed_net_proceeds", 2500000)
    jan_jun_invoiced = con.execute("SELECT COALESCE(SUM(invoiced_revenue), 0) FROM invoiced_revenue_monthly WHERE month BETWEEN DATE '2026-01-01' AND DATE '2026-06-01'").fetchone()[0]

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
        "headcount_by_function_monthly": _build_headcount_by_function(raw, [r["month"] for r in headcount_monthly]),
        "use_of_funds": use_of_funds,
        "attio_funnel": funnel,
        "backlog_contracted": [
            {"month": str(m), "backlog_revenue": float(v)}
            for m, v in raw.get("backlog_contracted", {}).items()
        ],
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
                "pricing": f"Workshop {pricing.get('workshop_fee_per_new_enterprise_client', 20000)//1000}k€ + deploy {pricing.get('deployment_fee_per_use_case', 40000)//1000}k€/UC + FDE {pricing.get('fde_billable_day_rate', 1150)}€/j",
                "margin_profile": f"~{int(annual[0].get('gross_margin', 0.5) * 100)}% (service-heavy)" if annual else "~50%",
                "key_metric": "Revenue de service générée",
            },
            {
                "id": "transition",
                "name": "Modèle transitoire",
                "period": "Sept 2026 → Q3 2027",
                "status": "next",
                "revenue_model": "Abonnement per-UC + service FDE séparé",
                "pricing": f"ETI {seg_pricing.get('ETI', 2000)}€ / GC {seg_pricing.get('GC', 5250)}€ / TGC {seg_pricing.get('TGC', 16250)}€ par UC/mois",
                "margin_profile": f"~{int(annual[1].get('gross_margin', 0.55) * 100)}% (mix platform + service)" if len(annual) > 1 else "55-65%",
                "key_metric": "ARR plateforme + accounts actifs",
            },
            {
                "id": "target",
                "name": "Modèle cible",
                "period": "2028+",
                "status": "planned",
                "revenue_model": "Plateforme dominante + service FDE allégé (utilization réduite)",
                "pricing": f"Plateforme {seg_pricing.get('ETI', 2000)}–{seg_pricing.get('TGC', 16250)}€/UC/mois + FDE on-demand",
                "margin_profile": f"~{int(annual[2].get('gross_margin', 0.75) * 100)}% (SaaS-grade)" if len(annual) > 2 else "75%+",
                "key_metric": "Net Revenue Retention > 130%",
            },
        ],
        "unit_economics": [
            {"phase": "Discover", "timing": "3 semaines", "driver": "Workshop cadrage", "assumption": f"{pricing.get('workshop_fee_per_new_enterprise_client', 20000)//1000}k€ / nouveau client"},
            {"phase": "Deploy", "timing": f"{pricing.get('deployment_duration_months', 3)} mois", "driver": "Déploiement 0→1", "assumption": f"{pricing.get('deployment_fee_per_use_case', 40000)//1000}k€ / use case"},
            {"phase": "Run", "timing": "Post go-live", "driver": "Abonnement plateforme", "assumption": f"ETI {seg_pricing.get('ETI', 2000)}€ – TGC {seg_pricing.get('TGC', 16250)}€ /UC/mois"},
            {"phase": "Expand", "timing": "En continu", "driver": "Expansion UC + upsell segment", "assumption": "Net expansion ~130% NRR cible"},
        ],
        "trajectory": [
            {"year": 2026, "theme": "Deployment proof", "text": f"Traction {int(jan_jun_invoiced/1000)}k€ facturés H1, premier client GC signé, {milestones[0]['live_use_cases']} UC en déploiement, levée seed {f_raise/1e6:.1f}M€."},
            {"year": 2027, "theme": "Platform transition", "text": f"{milestones[1]['enterprise_accounts']} comptes activés, {milestones[1]['live_use_cases']} UC live, bascule vers l'abonnement récurrent. ARR {milestones[1]['ending_arr']/1e6:.1f}M€."},
            {"year": 2028, "theme": "Use case expansion", "text": f"{milestones[2]['enterprise_accounts']} comptes, {milestones[2]['live_use_cases']} UC live, ARR {milestones[2]['ending_arr']/1e6:.1f}M€. Levier FDE + self-serve progressif."},
        ],
    }
    save_json(paths.model_outputs_json, dashboard)
    paths.dashboard_data_js.write_text("window.DASHBOARD_DATA = " + json.dumps(dashboard, ensure_ascii=False, indent=2, default=_json_default) + ";\n", encoding="utf-8")
    con.close()
