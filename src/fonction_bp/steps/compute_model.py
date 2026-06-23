from __future__ import annotations
import duckdb

from fonction_bp.config import Paths
from fonction_bp.utils import create_table_from_dicts, load_yaml


def run(paths: Paths, scenario: str = "vc_case") -> None:
    assumptions = load_yaml(paths.assumptions_dir / f"{scenario}.yaml")
    con = duckdb.connect(str(paths.duckdb_path))
    p = assumptions["pricing"]
    f = assumptions["fundraising"]
    s = assumptions["service_continuity"]
    h = assumptions["headcount"]
    o = assumptions["opex"]

    # Cohort / use-case model.
    deploy_lag = int(p["deployment_duration_months"])
    con.execute(f"""
        CREATE OR REPLACE TABLE enterprise_cohorts AS
        SELECT
            m.month,
            COALESCE(cp.new_enterprise_accounts, 0) AS new_enterprise_accounts,
            COALESCE(cp.initial_use_case_starts, 0) AS initial_use_case_starts,
            COALESCE(cp.expansion_use_case_starts, 0) AS expansion_use_case_starts,
            COALESCE(cp.use_case_starts, 0) AS use_case_starts,
            SUM(COALESCE(cp.new_enterprise_accounts, 0)) OVER (ORDER BY m.month) AS enterprise_accounts_end,
            SUM(COALESCE(cp.use_case_starts, 0)) OVER (ORDER BY m.month) AS cumulative_use_case_starts
        FROM months m
        LEFT JOIN cohort_plan cp USING(month)
        ORDER BY m.month
    """)

    # Live use cases = use case starts after deployment lag.
    con.execute(f"""
        CREATE OR REPLACE TABLE live_use_cases AS
        SELECT
            m.month,
            COALESCE(SUM(cp.use_case_starts), 0) AS live_use_cases
        FROM months m
        LEFT JOIN cohort_plan cp
          ON cp.month <= m.month - INTERVAL {deploy_lag} MONTH
        GROUP BY 1
        ORDER BY 1
    """)

    # Deployment revenue is recognized linearly over deployment duration.
    con.execute(f"""
        CREATE OR REPLACE TABLE deployment_revenue AS
        SELECT
            m.month,
            COALESCE(SUM(cp.use_case_starts * {float(p['deployment_fee_per_use_case'])} / {deploy_lag}), 0) AS deployment_revenue
        FROM months m
        LEFT JOIN cohort_plan cp
          ON m.month >= cp.month AND m.month < cp.month + INTERVAL {deploy_lag} MONTH
        GROUP BY 1
        ORDER BY 1
    """)

    # Wassym service continuity is internal detail, folded into services & deployment revenue.
    wassym_monthly_revenue = float(s["wassym_days_per_month"]) * float(s["wassym_revenue_day_rate"])
    wassym_monthly_cost = float(s["wassym_days_per_month"]) * float(s["wassym_cost_day_rate"])
    con.execute(f"""
        CREATE OR REPLACE TABLE service_continuity AS
        SELECT
            month,
            CASE WHEN month BETWEEN DATE '{s['start_month']}' AND DATE '{s['end_month']}' THEN {wassym_monthly_revenue} ELSE 0 END AS service_continuity_revenue,
            CASE WHEN month BETWEEN DATE '{s['start_month']}' AND DATE '{s['end_month']}' THEN {wassym_monthly_cost} ELSE 0 END AS service_continuity_cogs
        FROM months
    """)

    con.execute(f"""
        CREATE OR REPLACE TABLE revenue_monthly AS
        SELECT
            m.month,
            m.year,
            COALESCE(ar.commercial_revenue_actual, 0) AS actual_commercial_revenue,
            COALESCE(sb.custom_service_baseline, 0) AS custom_service_baseline,
            COALESCE(fsr.fde_support_revenue, 0) AS fde_support_revenue,
            COALESCE(ec.new_enterprise_accounts, 0) * {float(p['workshop_fee_per_new_enterprise_client'])} AS workshop_revenue,
            COALESCE(dr.deployment_revenue, 0) AS deployment_revenue,
            COALESCE(sc.service_continuity_revenue, 0) AS service_continuity_revenue,
            CASE
              WHEN m.month <= DATE '{assumptions['model_period']['actuals_end_month']}'
                THEN COALESCE(ar.commercial_revenue_actual, 0)
              ELSE COALESCE(sb.custom_service_baseline, 0) + COALESCE(fsr.fde_support_revenue, 0) +
                   COALESCE(ec.new_enterprise_accounts, 0) * {float(p['workshop_fee_per_new_enterprise_client'])} +
                   COALESCE(dr.deployment_revenue, 0) + COALESCE(sc.service_continuity_revenue, 0)
            END AS services_deployment_revenue,
            COALESCE(luc.live_use_cases, 0) * {float(p['subscription_mrr_per_live_use_case'])} AS platform_subscription_revenue,
            0.0 AS usage_success_revenue,
            COALESCE(luc.live_use_cases, 0) * {float(p['subscription_mrr_per_live_use_case'])} * 12 AS ending_arr,
            COALESCE(luc.live_use_cases, 0) AS live_use_cases,
            COALESCE(ec.enterprise_accounts_end, 0) AS enterprise_accounts_end,
            COALESCE(ec.use_case_starts, 0) AS use_case_starts
        FROM months m
        LEFT JOIN actual_revenue_monthly ar USING(month)
        LEFT JOIN service_baseline sb USING(month)
        LEFT JOIN fde_support_revenue fsr USING(month)
        LEFT JOIN enterprise_cohorts ec USING(month)
        LEFT JOIN deployment_revenue dr USING(month)
        LEFT JOIN service_continuity sc USING(month)
        LEFT JOIN live_use_cases luc USING(month)
        ORDER BY m.month
    """)

    con.execute("""
        CREATE OR REPLACE TABLE revenue_monthly AS
        SELECT *,
            services_deployment_revenue + platform_subscription_revenue + usage_success_revenue AS total_revenue
        FROM revenue_monthly
    """)

    con.execute("""
        CREATE OR REPLACE TABLE cogs_monthly AS
        SELECT
            r.month,
            r.year,
            r.services_deployment_revenue * (1 - gm_s.gross_margin) + sc.service_continuity_cogs AS services_deployment_cogs,
            r.platform_subscription_revenue * (1 - gm_p.gross_margin) AS platform_subscription_cogs,
            (r.services_deployment_revenue * (1 - gm_s.gross_margin) + sc.service_continuity_cogs + r.platform_subscription_revenue * (1 - gm_p.gross_margin)) AS total_cogs
        FROM revenue_monthly r
        LEFT JOIN gross_margin_assumptions gm_s ON gm_s.stream = 'services_deployment' AND gm_s.year = r.year
        LEFT JOIN gross_margin_assumptions gm_p ON gm_p.stream = 'platform_subscription' AND gm_p.year = r.year
        LEFT JOIN service_continuity sc USING(month)
    """)

    # Delivery capacity / FDE leverage.
    con.execute("""
        CREATE OR REPLACE TABLE fde_headcount_plan AS
        SELECT month, year,
               CASE WHEN month < DATE '2026-09-01' THEN 0
                    WHEN month < DATE '2027-01-01' THEN 1
                    WHEN month < DATE '2027-05-01' THEN 2
                    WHEN month < DATE '2027-09-01' THEN 3
                    WHEN month < DATE '2028-02-01' THEN 4
                    WHEN month < DATE '2028-06-01' THEN 5
                    WHEN month < DATE '2028-09-01' THEN 6
                    ELSE 7 END AS fde_headcount
        FROM months
    """)
    con.execute("""
        CREATE OR REPLACE TABLE delivery_capacity AS
        SELECT
            m.month,
            m.year,
            fde.fde_headcount,
            cap.use_cases_per_fde,
            fde.fde_headcount * cap.use_cases_per_fde AS fde_capacity_active_use_cases,
            COALESCE(SUM(cp.use_case_starts), 0) AS active_deployments,
            CASE WHEN fde.fde_headcount * cap.use_cases_per_fde = 0 THEN NULL
                 ELSE COALESCE(SUM(cp.use_case_starts), 0) / (fde.fde_headcount * cap.use_cases_per_fde) END AS capacity_utilization
        FROM months m
        LEFT JOIN fde_headcount_plan fde USING(month)
        LEFT JOIN fde_capacity_assumptions cap ON cap.year = m.year
        LEFT JOIN cohort_plan cp ON cp.month <= m.month AND cp.month > m.month - INTERVAL 3 MONTH
        GROUP BY 1,2,3,4,5
        ORDER BY 1
    """)

    # Headcount and opex.
    hire_rows = []
    for hire in h["hires"]:
        hire_rows.append({
            "role": hire["role"],
            "function": hire["function"],
            "start_month": str(hire["start_month"]),
            "monthly_loaded_cost": float(hire["monthly_loaded_cost"]),
        })
    create_table_from_dicts(con, "hires", hire_rows, [("role", "VARCHAR"), ("function", "VARCHAR"), ("start_month", "DATE"), ("monthly_loaded_cost", "DOUBLE")])
    catchup_rows = [{"month": str(month), "amount": float(amount)} for month, amount in h["founder_catchup_payments"].items()]
    create_table_from_dicts(con, "founder_catchup", catchup_rows, [("month", "DATE"), ("amount", "DOUBLE")])

    con.execute(f"""
        CREATE OR REPLACE TABLE headcount_monthly AS
        SELECT
            m.month,
            m.year,
            {int(h['founder_count'])} AS founder_count,
            CASE WHEN m.year = 2027 THEN {float(h['founder_salary_monthly_loaded_2027'])}
                 WHEN m.year >= 2028 THEN {float(h['founder_salary_monthly_loaded_2028'])}
                 ELSE 0 END * {int(h['founder_count'])} AS founder_salary_cost,
            COALESCE(fc.amount, 0) AS founder_catchup_cost,
            CASE WHEN m.month >= DATE '2026-07-01' THEN {float(h['current_roles']['cold_caller_monthly_total_placeholder'])} ELSE 0 END AS cold_callers_cost,
            CASE WHEN m.month >= DATE '2026-07-01' THEN {float(h['current_roles']['sales_full_time_monthly_loaded_placeholder'])} ELSE 0 END AS existing_sales_cost,
            COALESCE(SUM(CASE WHEN CAST(hi.start_month AS DATE) <= m.month THEN hi.monthly_loaded_cost ELSE 0 END), 0) AS new_hires_cost,
            COALESCE(COUNT(CASE WHEN CAST(hi.start_month AS DATE) <= m.month THEN 1 END), 0) AS new_hires_count
        FROM months m
        LEFT JOIN hires hi ON CAST(hi.start_month AS DATE) <= m.month
        LEFT JOIN founder_catchup fc USING(month)
        GROUP BY 1,2,3,4,5,6,7
        ORDER BY 1
    """)
    con.execute("""
        CREATE OR REPLACE TABLE headcount_monthly AS
        SELECT *,
            founder_salary_cost + founder_catchup_cost + cold_callers_cost + existing_sales_cost + new_hires_cost AS total_payroll_cost,
            founder_count + new_hires_count + CASE WHEN cold_callers_cost > 0 THEN 2 ELSE 0 END + CASE WHEN existing_sales_cost > 0 THEN 1 ELSE 0 END AS total_headcount_equivalent
        FROM headcount_monthly
    """)

    # Opex. Use base yearly monthly values + dated extras.
    security_rows = [{"month": str(month), "amount": float(amount)} for month, amount in o["enterprise_security_legal"].items()]
    tooling_rows = [{"month": str(month), "amount": float(amount)} for month, amount in o["product_infra_ai_tooling"].items()]
    create_table_from_dicts(con, "security_legal_spend", security_rows, [("month", "DATE"), ("amount", "DOUBLE")])
    create_table_from_dicts(con, "tooling_spend", tooling_rows, [("month", "DATE"), ("amount", "DOUBLE")])
    con.execute(f"""
        CREATE OR REPLACE TABLE opex_monthly AS
        SELECT
            m.month,
            m.year,
            CASE WHEN m.month BETWEEN DATE '2026-07-01' AND DATE '2026-12-01' THEN {float(o['monthly_base_2026_h2'])}
                 WHEN m.year = 2027 THEN {float(o['monthly_base_2027'])}
                 WHEN m.year = 2028 THEN {float(o['monthly_base_2028'])}
                 ELSE 0 END AS base_opex,
            COALESCE(sl.amount, 0) AS enterprise_security_legal,
            COALESCE(ts.amount, 0) AS product_infra_ai_tooling
        FROM months m
        LEFT JOIN security_legal_spend sl USING(month)
        LEFT JOIN tooling_spend ts USING(month)
    """)
    con.execute("""
        CREATE OR REPLACE TABLE opex_monthly AS
        SELECT *, base_opex + enterprise_security_legal + product_infra_ai_tooling AS total_opex
        FROM opex_monthly
    """)

    # Cash runway. Starts July 2026 with actual Qonto cash. Prior months set NULL for cash balance in VC outputs.
    con.execute(f"""
        CREATE OR REPLACE TABLE cash_monthly_base AS
        SELECT
            m.month,
            m.year,
            r.total_revenue,
            c.total_cogs,
            h.total_payroll_cost,
            o.total_opex,
            CASE WHEN m.month = DATE '{f['seed_close_month']}' THEN {float(f['seed_net_proceeds'])} ELSE 0 END AS seed_proceeds,
            r.total_revenue - c.total_cogs - h.total_payroll_cost - o.total_opex AS operating_cashflow
        FROM months m
        LEFT JOIN revenue_monthly r USING(month)
        LEFT JOIN cogs_monthly c USING(month)
        LEFT JOIN headcount_monthly h USING(month)
        LEFT JOIN opex_monthly o USING(month)
        WHERE m.month >= DATE '2026-07-01'
        ORDER BY m.month
    """)
    con.execute(f"""
        CREATE OR REPLACE TABLE cash_monthly AS
        SELECT *,
            {float(f['starting_cash_2026_07_01'])} + SUM(operating_cashflow + seed_proceeds) OVER (ORDER BY month ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS ending_cash
        FROM cash_monthly_base
    """)

    # Annual and quarterly summaries.
    con.execute("""
        CREATE OR REPLACE TABLE annual_summary AS
        SELECT
            r.year,
            SUM(r.services_deployment_revenue) AS services_deployment_revenue,
            SUM(r.platform_subscription_revenue) AS platform_subscription_revenue,
            SUM(r.usage_success_revenue) AS usage_success_revenue,
            SUM(r.total_revenue) AS total_revenue,
            SUM(c.total_cogs) AS total_cogs,
            SUM(r.total_revenue - c.total_cogs) AS gross_profit,
            CASE WHEN SUM(r.total_revenue) = 0 THEN NULL ELSE SUM(r.total_revenue - c.total_cogs) / SUM(r.total_revenue) END AS gross_margin,
            MAX(CASE WHEN strftime(r.month, '%m') = '12' THEN r.ending_arr END) AS ending_arr,
            MAX(CASE WHEN strftime(r.month, '%m') = '12' THEN r.enterprise_accounts_end END) AS enterprise_accounts_end,
            MAX(CASE WHEN strftime(r.month, '%m') = '12' THEN r.live_use_cases END) AS live_use_cases,
            CASE WHEN SUM(r.total_revenue) = 0 THEN NULL ELSE SUM(r.platform_subscription_revenue) / SUM(r.total_revenue) END AS recurring_revenue_share
        FROM revenue_monthly r
        LEFT JOIN cogs_monthly c USING(month)
        GROUP BY 1
        ORDER BY 1
    """)

    con.execute("""
        CREATE OR REPLACE TABLE quarterly_summary AS
        SELECT
            year,
            CAST(((EXTRACT(month FROM month) - 1) / 3) AS INTEGER) + 1 AS quarter,
            'Q' || (CAST(((EXTRACT(month FROM month) - 1) / 3) AS INTEGER) + 1) || ' ' || right(CAST(year AS VARCHAR), 2) AS period,
            SUM(total_revenue) AS total_revenue,
            SUM(services_deployment_revenue) AS services_deployment_revenue,
            SUM(platform_subscription_revenue) AS platform_subscription_revenue,
            MAX(month) AS quarter_end_month
        FROM revenue_monthly
        GROUP BY year, quarter
        ORDER BY year, quarter
    """)

    con.execute("""
        CREATE OR REPLACE TABLE year_end_milestones AS
        SELECT
            year,
            CAST(enterprise_accounts_end AS INTEGER) AS enterprise_accounts,
            CAST(live_use_cases AS INTEGER) AS live_use_cases,
            CASE WHEN enterprise_accounts_end = 0 THEN NULL ELSE live_use_cases / enterprise_accounts_end END AS use_cases_per_account,
            ending_arr
        FROM annual_summary
        ORDER BY year
    """)

    # Dashboard KPIs.
    jan_jun_actual = con.execute("SELECT SUM(commercial_revenue_actual) FROM actual_revenue_monthly").fetchone()[0] or 0
    dec_2027 = con.execute("SELECT ending_arr, enterprise_accounts_end, live_use_cases FROM annual_summary WHERE year = 2027").fetchone()
    dec_2028 = con.execute("SELECT ending_arr FROM annual_summary WHERE year = 2028").fetchone()
    runway_cash_2027 = con.execute("SELECT ending_cash FROM cash_monthly WHERE month = DATE '2027-12-01'").fetchone()[0]
    kpis = [
        {"metric": "Actual commercial revenue Jan-Jun 2026", "value": jan_jun_actual, "unit": "EUR"},
        {"metric": "2026E revenue", "value": con.execute("SELECT total_revenue FROM annual_summary WHERE year=2026").fetchone()[0], "unit": "EUR"},
        {"metric": "2027E revenue", "value": con.execute("SELECT total_revenue FROM annual_summary WHERE year=2027").fetchone()[0], "unit": "EUR"},
        {"metric": "Ending ARR Dec-2027", "value": dec_2027[0], "unit": "EUR"},
        {"metric": "Enterprise accounts Dec-2027", "value": dec_2027[1], "unit": "count"},
        {"metric": "Live use cases Dec-2027", "value": dec_2027[2], "unit": "count"},
        {"metric": "Ending cash Dec-2027", "value": runway_cash_2027, "unit": "EUR"},
        {"metric": "Seed raise", "value": float(f['seed_net_proceeds']), "unit": "EUR"},
    ]
    create_table_from_dicts(con, "dashboard_kpis", kpis, [("metric", "VARCHAR"), ("value", "DOUBLE"), ("unit", "VARCHAR")])

    con.close()
