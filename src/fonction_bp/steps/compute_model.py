from __future__ import annotations
import calendar
import datetime as dt
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
    fde_f = assumptions["fde_formula"]
    fde_b = assumptions["fde_billable"]

    deploy_lag = int(p["deployment_duration_months"])

    # Cohort / use-case model with segment.
    con.execute(f"""
        CREATE OR REPLACE TABLE enterprise_cohorts AS
        SELECT
            m.month,
            COALESCE(cp.segment, 'ETI') AS segment,
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

    # Live use cases by segment = UC starts after deployment lag, grouped by segment.
    con.execute(f"""
        CREATE OR REPLACE TABLE live_use_cases_by_segment AS
        SELECT
            m.month,
            cp.segment,
            COALESCE(SUM(cp.use_case_starts), 0) AS live_use_cases
        FROM months m
        LEFT JOIN cohort_plan cp
          ON cp.month <= m.month - INTERVAL {deploy_lag} MONTH
        WHERE cp.segment IS NOT NULL
        GROUP BY 1, 2
        ORDER BY 1, 2
    """)

    # Total live use cases per month (all segments).
    con.execute(f"""
        CREATE OR REPLACE TABLE live_use_cases AS
        SELECT
            month,
            SUM(live_use_cases) AS live_use_cases
        FROM live_use_cases_by_segment
        GROUP BY 1
        ORDER BY 1
    """)

    # Platform subscription revenue by segment (pricing × live UC).
    con.execute("""
        CREATE OR REPLACE TABLE platform_revenue_by_segment AS
        SELECT
            l.month,
            l.segment,
            l.live_use_cases,
            sp.avg_mrr_per_uc,
            l.live_use_cases * sp.avg_mrr_per_uc AS segment_platform_revenue
        FROM live_use_cases_by_segment l
        JOIN segment_pricing sp ON sp.segment = l.segment
    """)

    con.execute("""
        CREATE OR REPLACE TABLE platform_revenue_monthly AS
        SELECT
            month,
            SUM(segment_platform_revenue) AS platform_subscription_revenue,
            SUM(live_use_cases * avg_mrr_per_uc * 12) AS ending_arr
        FROM platform_revenue_by_segment
        GROUP BY 1
        ORDER BY 1
    """)

    # Deployment revenue recognized linearly over deployment duration.
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

    # Wassym service continuity.
    wassym_monthly_revenue = float(s["freelance_bpce_days_per_month"]) * float(s["freelance_bpce_revenue_day_rate"])
    wassym_monthly_cost = float(s["freelance_bpce_days_per_month"]) * float(s["freelance_bpce_cost_day_rate"])
    con.execute(f"""
        CREATE OR REPLACE TABLE service_continuity AS
        SELECT
            month,
            CASE WHEN month BETWEEN DATE '{s['start_month']}' AND DATE '{s['end_month']}' THEN {wassym_monthly_revenue} ELSE 0 END AS service_continuity_revenue,
            CASE WHEN month BETWEEN DATE '{s['start_month']}' AND DATE '{s['end_month']}' THEN {wassym_monthly_cost} ELSE 0 END AS service_continuity_cogs
        FROM months
    """)

    # FDE billable service revenue — formula-driven, replaces hardcoded service_forecast_baseline.
    # Revenue = uc_in_run × fde_per_uc_in_run × day_rate × days_per_month × utilization_rate
    # UC in deployment already generates deployment_revenue (40k/UC over 3 months) — not here.
    fde_day_rate = float(p['fde_billable_day_rate'])
    fde_days_per_month = float(fde_b['days_billable_per_month'])
    util_rates = {str(k): v for k, v in fde_b['utilization_rate'].items()}
    con.execute(f"""
        CREATE OR REPLACE TABLE fde_service_revenue AS
        SELECT
            m.month,
            COALESCE(luc.live_use_cases, 0) AS uc_in_run,
            COALESCE(luc.live_use_cases, 0) * {float(fde_f['fde_per_uc_in_run'])}
                * {fde_day_rate} * {fde_days_per_month}
                * CASE
                    WHEN m.month BETWEEN DATE '2026-07-01' AND DATE '2026-12-01' THEN {float(util_rates['2026_h2'])}
                    WHEN m.month BETWEEN DATE '2027-01-01' AND DATE '2027-06-01' THEN {float(util_rates['2027_h1'])}
                    WHEN m.month BETWEEN DATE '2027-07-01' AND DATE '2027-12-01' THEN {float(util_rates['2027_h2'])}
                    ELSE {float(util_rates['2028'])}
                  END AS fde_service_revenue
        FROM months m
        LEFT JOIN live_use_cases luc USING(month)
    """)

    # Revenue monthly — combines all streams.
    # Actuals source: invoiced revenue (facturé), not collected (encaissé).
    # For the current month: split into actual portion (invoiced so far) + forecast residual.
    today = dt.date.today()
    current_month_start = today.replace(day=1)
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    fraction_elapsed = today.day / days_in_month
    fraction_remaining = 1.0 - fraction_elapsed
    current_month_iso = current_month_start.isoformat()
    actuals_end = str(assumptions['model_period']['actuals_end_month'])

    con.execute(f"""
        CREATE OR REPLACE TABLE revenue_monthly AS
        SELECT
            m.month,
            m.year,
            COALESCE(inv.invoiced_revenue, 0) AS invoiced_revenue_actual,
            COALESCE(ar.commercial_revenue_actual, 0) AS collected_revenue_actual,
            COALESCE(fsr.fde_service_revenue, 0) AS fde_service_revenue,
            COALESCE(ec.new_enterprise_accounts, 0) * {float(p['workshop_fee_per_new_enterprise_client'])} AS workshop_revenue,
            COALESCE(dr.deployment_revenue, 0) AS deployment_revenue,
            COALESCE(sc.service_continuity_revenue, 0) AS service_continuity_revenue,
            -- actual_services: invoiced for past/current months; 0 for future
            CASE
              WHEN m.month <= DATE '{current_month_iso}' THEN COALESCE(inv.invoiced_revenue, 0)
              ELSE 0
            END AS actual_services_revenue,
            -- forecast_services: 0 for past; residual fraction for current; full for future
            CASE
              WHEN m.month < DATE '{current_month_iso}' THEN 0
              WHEN m.month = DATE '{current_month_iso}'
                THEN GREATEST(0,
                       (COALESCE(fsr.fde_service_revenue, 0) +
                        COALESCE(ec.new_enterprise_accounts, 0) * {float(p['workshop_fee_per_new_enterprise_client'])} +
                        COALESCE(dr.deployment_revenue, 0) + COALESCE(sc.service_continuity_revenue, 0))
                       * {fraction_remaining})
              ELSE COALESCE(fsr.fde_service_revenue, 0) +
                   COALESCE(ec.new_enterprise_accounts, 0) * {float(p['workshop_fee_per_new_enterprise_client'])} +
                   COALESCE(dr.deployment_revenue, 0) + COALESCE(sc.service_continuity_revenue, 0)
            END AS forecast_services_revenue,
            COALESCE(pr.platform_subscription_revenue, 0) AS platform_subscription_revenue,
            0.0 AS usage_success_revenue,
            COALESCE(pr.ending_arr, 0) AS ending_arr,
            COALESCE(luc.live_use_cases, 0) AS live_use_cases,
            COALESCE(ec.enterprise_accounts_end, 0) AS enterprise_accounts_end,
            COALESCE(ec.use_case_starts, 0) AS use_case_starts
        FROM months m
        LEFT JOIN invoiced_revenue_monthly inv USING(month)
        LEFT JOIN actual_revenue_monthly ar USING(month)
        LEFT JOIN fde_service_revenue fsr USING(month)
        LEFT JOIN enterprise_cohorts ec USING(month)
        LEFT JOIN deployment_revenue dr USING(month)
        LEFT JOIN service_continuity sc USING(month)
        LEFT JOIN platform_revenue_monthly pr USING(month)
        LEFT JOIN live_use_cases luc USING(month)
        ORDER BY m.month
    """)

    con.execute("""
        CREATE OR REPLACE TABLE revenue_monthly AS
        SELECT *,
            actual_services_revenue + forecast_services_revenue AS services_deployment_revenue,
            actual_services_revenue + forecast_services_revenue + platform_subscription_revenue + usage_success_revenue AS total_revenue
        FROM revenue_monthly
    """)

    # FDE headcount — formula-based.
    fde_per_deploying = float(fde_f["fde_per_uc_deploying"])
    fde_per_run = float(fde_f["fde_per_uc_in_run"])
    con.execute(f"""
        CREATE OR REPLACE TABLE fde_headcount_plan AS
        SELECT
            m.month,
            m.year,
            COALESCE(deploying.uc_deploying, 0) AS uc_in_deployment,
            COALESCE(luc.live_use_cases, 0) AS uc_in_run,
            CEIL(COALESCE(deploying.uc_deploying, 0) * {fde_per_deploying} + COALESCE(luc.live_use_cases, 0) * {fde_per_run}) AS fde_headcount
        FROM months m
        LEFT JOIN (
            SELECT m2.month, COALESCE(SUM(cp.use_case_starts), 0) AS uc_deploying
            FROM months m2
            LEFT JOIN cohort_plan cp
              ON cp.month <= m2.month AND cp.month > m2.month - INTERVAL {deploy_lag} MONTH
            GROUP BY 1
        ) deploying USING(month)
        LEFT JOIN live_use_cases luc USING(month)
    """)

    # Hires table (needed by both COGS and headcount).
    hire_rows = []
    for hire in h["hires"]:
        hire_rows.append({
            "role": hire["role"],
            "function": hire["function"],
            "start_month": str(hire["start_month"]),
            "monthly_loaded_cost": float(hire["monthly_loaded_cost"]),
        })
    create_table_from_dicts(con, "hires", hire_rows, [("role", "VARCHAR"), ("function", "VARCHAR"), ("start_month", "DATE"), ("monthly_loaded_cost", "DOUBLE")])

    # Freelance missions — COGS ponctuels de sous-traitance delivery.
    freelance_missions = assumptions.get("freelance_missions", {}).get("missions", [])
    fl_rows = []
    for mission in freelance_missions:
        total_cost = float(mission["tjm"]) * int(mission["days"])
        start = str(mission["start_month"])
        end = str(mission["end_month"])
        fl_rows.append({
            "name": mission["name"],
            "client": mission["client"],
            "start_month": start,
            "end_month": end,
            "total_cost": total_cost,
        })
    if fl_rows:
        create_table_from_dicts(con, "freelance_missions", fl_rows, [("name", "VARCHAR"), ("client", "VARCHAR"), ("start_month", "DATE"), ("end_month", "DATE"), ("total_cost", "DOUBLE")])
        con.execute("""
            CREATE OR REPLACE TABLE freelance_cogs_monthly AS
            SELECT
                m.month,
                COALESCE(SUM(
                    fm.total_cost / (DATEDIFF('month', fm.start_month, fm.end_month) + 1)
                ), 0) AS freelance_cost
            FROM months m
            LEFT JOIN freelance_missions fm
              ON m.month >= fm.start_month AND m.month <= fm.end_month
            GROUP BY 1
        """)
    else:
        con.execute("CREATE TABLE freelance_cogs_monthly AS SELECT month, 0.0 AS freelance_cost FROM months")

    # COGS bottom-up.
    # FDE cost = actual hire cost of Forward-Deployed Engineering staff (not formula × flat rate).
    # This avoids double-counting with payroll — FDE hires are EXCLUDED from payroll below.
    avg_token_cost = float(p["avg_token_cost_per_uc_month"])
    infra_cloud = o["infra_cloud_monthly"]
    con.execute(f"""
        CREATE OR REPLACE TABLE fde_actual_cost AS
        SELECT
            m.month,
            COALESCE(SUM(CASE WHEN hi.function = 'Forward-Deployed Engineering'
                              AND CAST(hi.start_month AS DATE) <= m.month
                         THEN hi.monthly_loaded_cost ELSE 0 END), 0) AS fde_cost
        FROM months m
        LEFT JOIN hires hi ON CAST(hi.start_month AS DATE) <= m.month
        GROUP BY 1
    """)
    con.execute(f"""
        CREATE OR REPLACE TABLE cogs_monthly AS
        SELECT
            m.month,
            m.year,
            COALESCE(fac.fde_cost, 0) AS fde_cost,
            COALESCE(fl.freelance_cost, 0) AS freelance_cost,
            COALESCE(luc.live_use_cases, 0) * {avg_token_cost} AS token_cost,
            CASE
              WHEN m.month BETWEEN DATE '2026-07-01' AND DATE '2026-12-01' THEN {float(infra_cloud['2026_h2'])}
              WHEN m.month BETWEEN DATE '2027-01-01' AND DATE '2027-06-01' THEN {float(infra_cloud['2027_h1'])}
              WHEN m.month BETWEEN DATE '2027-07-01' AND DATE '2027-12-01' THEN {float(infra_cloud['2027_h2'])}
              WHEN m.month BETWEEN DATE '2028-01-01' AND DATE '2028-06-01' THEN {float(infra_cloud['2028_h1'])}
              WHEN m.month >= DATE '2028-07-01' THEN {float(infra_cloud['2028_h2'])}
              ELSE 0
            END AS infra_cloud_cost,
            COALESCE(sc.service_continuity_cogs, 0) AS service_continuity_cogs
        FROM months m
        LEFT JOIN fde_actual_cost fac USING(month)
        LEFT JOIN freelance_cogs_monthly fl USING(month)
        LEFT JOIN live_use_cases luc USING(month)
        LEFT JOIN service_continuity sc USING(month)
    """)
    con.execute("""
        CREATE OR REPLACE TABLE cogs_monthly AS
        SELECT *,
            fde_cost + freelance_cost + token_cost + infra_cloud_cost + service_continuity_cogs AS total_cogs
        FROM cogs_monthly
    """)

    # Delivery capacity (legacy view — kept for Excel compat).
    con.execute("""
        CREATE OR REPLACE TABLE delivery_capacity AS
        SELECT
            m.month,
            m.year,
            fde.fde_headcount,
            cap.use_cases_per_fde,
            fde.fde_headcount * cap.use_cases_per_fde AS fde_capacity_active_use_cases,
            fde.uc_in_deployment AS active_deployments,
            CASE WHEN fde.fde_headcount = 0 THEN NULL
                 ELSE (fde.uc_in_deployment + fde.uc_in_run) / fde.fde_headcount END AS capacity_utilization
        FROM months m
        LEFT JOIN fde_headcount_plan fde USING(month)
        LEFT JOIN fde_capacity_assumptions cap ON cap.year = m.year
        ORDER BY 1
    """)

    # Headcount and opex.
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
            CASE WHEN m.month BETWEEN DATE '{h['current_roles']['cold_callers']['start_month']}' AND DATE '{h['current_roles']['cold_callers']['end_month']}'
                 THEN {float(h['current_roles']['cold_callers']['monthly_total_cost'])} ELSE 0 END AS cold_callers_cost,
            CASE WHEN m.month BETWEEN DATE '{h['current_roles']['sales_freelance']['start_month']}' AND DATE '{h['current_roles']['sales_freelance']['end_month']}'
                 THEN {float(h['current_roles']['sales_freelance']['monthly_loaded_cost'])} ELSE 0 END AS existing_sales_cost,
            COALESCE(SUM(CASE WHEN CAST(hi.start_month AS DATE) <= m.month
                              AND hi.function != 'Forward-Deployed Engineering'
                         THEN hi.monthly_loaded_cost ELSE 0 END), 0) AS new_hires_cost,
            COALESCE(COUNT(CASE WHEN CAST(hi.start_month AS DATE) <= m.month
                               AND hi.function != 'Forward-Deployed Engineering'
                          THEN 1 END), 0) AS new_hires_count
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

    # Opex — decomposed.
    ai_tooling_cost = float(o["ai_tooling_cost_per_person_month"])
    marketing = {str(k): v for k, v in o["marketing_incremental"].items()}
    saas = {str(k): v for k, v in o["saas_misc_monthly"].items()}
    security_rows = [{"month": str(month), "amount": float(amount)} for month, amount in o["enterprise_security_legal"].items()]
    create_table_from_dicts(con, "security_legal_spend", security_rows, [("month", "DATE"), ("amount", "DOUBLE")])

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
            CASE WHEN m.year = 2027 THEN {float(marketing['monthly_2027'])}
                 WHEN m.year = 2028 THEN {float(marketing['monthly_2028'])}
                 ELSE 0 END AS marketing_incremental,
            -- AI dev tooling: count tech headcount (Product & Engineering + FDE) × cost
            (SELECT COUNT(*) FROM hires hi
             WHERE hi.function IN ('Product & Engineering', 'Forward-Deployed Engineering')
             AND CAST(hi.start_month AS DATE) <= m.month) * {ai_tooling_cost} AS ai_dev_tooling,
            CASE WHEN m.month BETWEEN DATE '2026-07-01' AND DATE '2026-12-01' THEN {float(saas['2026_h2'])}
                 WHEN m.year = 2027 THEN {float(saas['2027'])}
                 WHEN m.year = 2028 THEN {float(saas['2028'])}
                 ELSE 0 END AS saas_misc
        FROM months m
        LEFT JOIN security_legal_spend sl USING(month)
    """)
    con.execute("""
        CREATE OR REPLACE TABLE opex_monthly AS
        SELECT *,
            base_opex + enterprise_security_legal + marketing_incremental + ai_dev_tooling + saas_misc AS total_opex
        FROM opex_monthly
    """)

    # Cash runway.
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
    jan_jun_invoiced = con.execute("SELECT SUM(invoiced_revenue) FROM invoiced_revenue_monthly WHERE month BETWEEN DATE '2026-01-01' AND DATE '2026-06-01'").fetchone()[0] or 0
    dec_2027 = con.execute("SELECT ending_arr, enterprise_accounts_end, live_use_cases FROM annual_summary WHERE year = 2027").fetchone()
    runway_cash_2027 = con.execute("SELECT ending_cash FROM cash_monthly WHERE month = DATE '2027-12-01'").fetchone()[0]
    kpis = [
        {"metric": "Invoiced revenue H1 2026", "value": jan_jun_invoiced, "unit": "EUR"},
        {"metric": "2026E revenue", "value": con.execute("SELECT total_revenue FROM annual_summary WHERE year=2026").fetchone()[0], "unit": "EUR"},
        {"metric": "2027E revenue", "value": con.execute("SELECT total_revenue FROM annual_summary WHERE year=2027").fetchone()[0], "unit": "EUR"},
        {"metric": "2028E revenue", "value": con.execute("SELECT total_revenue FROM annual_summary WHERE year=2028").fetchone()[0], "unit": "EUR"},
        {"metric": "Ending ARR Dec-2027", "value": dec_2027[0], "unit": "EUR"},
        {"metric": "Enterprise accounts Dec-2027", "value": dec_2027[1], "unit": "count"},
        {"metric": "Live use cases Dec-2027", "value": dec_2027[2], "unit": "count"},
        {"metric": "Gross margin 2027", "value": con.execute("SELECT gross_margin FROM annual_summary WHERE year=2027").fetchone()[0], "unit": "pct"},
        {"metric": "Ending cash Dec-2027", "value": runway_cash_2027, "unit": "EUR"},
        {"metric": "Seed raise", "value": float(f['seed_net_proceeds']), "unit": "EUR"},
    ]
    create_table_from_dicts(con, "dashboard_kpis", kpis, [("metric", "VARCHAR"), ("value", "DOUBLE"), ("unit", "VARCHAR")])

    con.close()
