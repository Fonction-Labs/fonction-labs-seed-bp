from __future__ import annotations
import duckdb

from fonction_bp.config import Paths
from fonction_bp.utils import create_table_from_dicts, load_yaml, month_range, month_start


def _monthly_dict_to_rows(mapping: dict, value_col: str) -> list[dict]:
    rows = []
    for month, value in (mapping or {}).items():
        rows.append({"month": str(month), value_col: float(value or 0)})
    return rows


def run(paths: Paths, scenario: str = "vc_case") -> None:
    assumptions = load_yaml(paths.assumptions_dir / f"{scenario}.yaml")
    con = duckdb.connect(str(paths.duckdb_path))

    months = [{"month": m.isoformat(), "year": m.year, "quarter": ((m.month - 1)//3)+1, "month_num": m.month} for m in month_range(assumptions["model_period"]["start_month"], assumptions["model_period"]["end_month"])]
    create_table_from_dicts(con, "months", months, [("month", "DATE"), ("year", "INTEGER"), ("quarter", "INTEGER"), ("month_num", "INTEGER")])

    # Scalar assumptions table for auditability.
    scalar_rows = []
    for section, values in assumptions.items():
        if isinstance(values, dict):
            for key, value in values.items():
                if not isinstance(value, (dict, list)):
                    scalar_rows.append({"section": section, "key": key, "value": str(value)})
    create_table_from_dicts(con, "assumptions_scalar", scalar_rows, [("section", "VARCHAR"), ("key", "VARCHAR"), ("value", "VARCHAR")])

    pricing = assumptions["pricing"]
    pricing_rows = [{"key": k, "value": float(v)} for k, v in pricing.items() if isinstance(v, (int, float))]
    create_table_from_dicts(con, "pricing", pricing_rows, [("key", "VARCHAR"), ("value", "DOUBLE")])

    baseline_rows = _monthly_dict_to_rows(assumptions["service_forecast_baseline"]["monthly_eur"], "custom_service_baseline")
    create_table_from_dicts(con, "service_baseline_raw", baseline_rows, [("month", "DATE"), ("custom_service_baseline", "DOUBLE")])
    con.execute("CREATE TABLE service_baseline AS SELECT month, custom_service_baseline FROM service_baseline_raw")

    fde_support_rows = _monthly_dict_to_rows(assumptions["fde_support_revenue"]["monthly_eur"], "fde_support_revenue")
    create_table_from_dicts(con, "fde_support_revenue_raw", fde_support_rows, [("month", "DATE"), ("fde_support_revenue", "DOUBLE")])
    con.execute("CREATE TABLE fde_support_revenue AS SELECT month, fde_support_revenue FROM fde_support_revenue_raw")

    # Enterprise cohort plan.
    cohort_rows = []
    for month, values in assumptions["enterprise_cohort_plan"]["monthly"].items():
        cohort_rows.append({
            "month": str(month),
            "new_enterprise_accounts": int(values.get("new_enterprise_accounts", 0) or 0),
            "initial_use_case_starts": int(values.get("initial_use_case_starts", 0) or 0),
            "expansion_use_case_starts": int(values.get("expansion_use_case_starts", 0) or 0),
        })
    create_table_from_dicts(con, "cohort_plan_raw", cohort_rows, [("month", "DATE"), ("new_enterprise_accounts", "INTEGER"), ("initial_use_case_starts", "INTEGER"), ("expansion_use_case_starts", "INTEGER")])
    con.execute("""
        CREATE TABLE cohort_plan AS
        SELECT month, new_enterprise_accounts, initial_use_case_starts, expansion_use_case_starts,
               initial_use_case_starts + expansion_use_case_starts AS use_case_starts
        FROM cohort_plan_raw
    """)

    # FDE capacity by year.
    cap_rows = []
    for year, cap in assumptions["fde_capacity"]["use_cases_per_fde"].items():
        cap_rows.append({"year": int(year), "use_cases_per_fde": float(cap)})
    create_table_from_dicts(con, "fde_capacity_assumptions", cap_rows, [("year", "INTEGER"), ("use_cases_per_fde", "DOUBLE")])

    # Gross margin by year.
    gm_rows = []
    for stream, mapping in assumptions["gross_margin"].items():
        for year, margin in mapping.items():
            gm_rows.append({"stream": stream, "year": int(year), "gross_margin": float(margin)})
    create_table_from_dicts(con, "gross_margin_assumptions", gm_rows, [("stream", "VARCHAR"), ("year", "INTEGER"), ("gross_margin", "DOUBLE")])

    # Use of funds.
    uof_rows = []
    for row in assumptions["use_of_funds"]:
        uof_rows.append({"category": row["category"], "amount": float(row["amount"]), "purpose": row["purpose"]})
    create_table_from_dicts(con, "use_of_funds", uof_rows, [("category", "VARCHAR"), ("amount", "DOUBLE"), ("purpose", "VARCHAR")])

    con.close()
