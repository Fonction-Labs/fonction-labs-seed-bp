from __future__ import annotations
import duckdb
from pathlib import Path

from fonction_bp.config import Paths
from fonction_bp.utils import csv_rows, create_table_from_dicts, load_yaml, month_start, normalize_text, parse_fr_amount, parse_qonto_datetime, read_qonto_rows


def classify_commercial_revenue(row: dict[str, str], assumptions: dict) -> tuple[bool, str]:
    q = assumptions["qonto_classification"]
    counterparty = normalize_text(row.get("Nom de la contrepartie"))
    reference = normalize_text(row.get("Référence")) + " " + normalize_text(row.get("Note"))
    category = row.get("Catégorie de trésorerie") or ""
    category_norm = normalize_text(category)

    if any(term in counterparty for term in q.get("exclude_counterparty_contains", [])):
        return False, "excluded_counterparty"
    if any(term in reference for term in q.get("exclude_reference_contains", [])):
        return False, "excluded_reference"

    category_included = any(normalize_text(term) in category_norm for term in q.get("include_credit_categories", []))
    counterparty_included = any(term in counterparty for term in q.get("include_counterparty_contains", []))
    if category_included or counterparty_included:
        return True, "commercial_revenue"
    return False, "not_commercial"


def run(paths: Paths, scenario: str = "vc_case") -> None:
    assumptions = load_yaml(paths.assumptions_dir / f"{scenario}.yaml")
    paths.ensure_dirs()
    if paths.duckdb_path.exists():
        paths.duckdb_path.unlink()
    con = duckdb.connect(str(paths.duckdb_path))

    qonto_zip = paths.raw_qonto_dir / "qonto_archive.zip"
    rows = read_qonto_rows(qonto_zip)
    tx_rows = []
    for row in rows:
        op_date = parse_qonto_datetime(row.get("Date de l'opération (local)") or row.get("Date de la valeur (local)"))
        if op_date is None:
            continue
        credit_ttc = parse_fr_amount(row.get("Crédit"))
        debit_ttc = parse_fr_amount(row.get("Débit"))
        amount_ht = parse_fr_amount(row.get("Montant total (HT)"))
        is_commercial, classification = classify_commercial_revenue(row, assumptions)
        tx_rows.append({
            "operation_date": op_date.date().isoformat(),
            "month": op_date.date().replace(day=1).isoformat(),
            "counterparty": row.get("Nom de la contrepartie") or "",
            "reference": row.get("Référence") or "",
            "cash_category": row.get("Catégorie de trésorerie") or "",
            "credit_ttc": credit_ttc,
            "debit_ttc": debit_ttc,
            "amount_ht": amount_ht,
            "is_commercial_revenue": 1 if (credit_ttc > 0 and is_commercial) else 0,
            "classification": classification,
        })

    create_table_from_dicts(con, "raw_qonto_transactions", tx_rows)

    con.execute("""
        CREATE TABLE actual_revenue_monthly AS
        SELECT
            CAST(month AS DATE) AS month,
            SUM(CASE WHEN is_commercial_revenue = 1 THEN amount_ht ELSE 0 END) AS commercial_revenue_actual
        FROM raw_qonto_transactions
        WHERE CAST(month AS DATE) BETWEEN DATE '2026-01-01' AND DATE '2026-06-01'
        GROUP BY 1
        ORDER BY 1
    """)

    # Invoiced revenue from Qonto invoices CSV (source of truth for actuals).
    invoices_dir = paths.root / "data" / "raw" / "invoices"
    invoice_files = list(invoices_dir.glob("*.csv")) if invoices_dir.exists() else []
    if invoice_files:
        import csv as csv_mod
        inv_rows = []
        for inv_file in invoice_files:
            with open(inv_file, "r", encoding="utf-8") as f:
                reader = csv_mod.DictReader(f, delimiter=";")
                for row in reader:
                    issue_date = row.get("Issue Date", "")
                    subtotal_raw = row.get("Subtotal", "0")
                    subtotal = float(subtotal_raw.replace(",", ".")) if subtotal_raw else 0.0
                    if issue_date and subtotal > 0:
                        inv_rows.append({
                            "invoice_number": row.get("Number", ""),
                            "issue_date": issue_date,
                            "month": issue_date[:8] + "01",
                            "status": row.get("Status", ""),
                            "client_name": row.get("Client Name", ""),
                            "subtotal_ht": subtotal,
                        })
        if inv_rows:
            create_table_from_dicts(con, "raw_invoices", inv_rows)
            con.execute("""
                CREATE TABLE invoiced_revenue_monthly AS
                SELECT
                    CAST(month AS DATE) AS month,
                    SUM(subtotal_ht) AS invoiced_revenue,
                    SUM(CASE WHEN status = 'paid' THEN subtotal_ht ELSE 0 END) AS collected_revenue,
                    SUM(CASE WHEN status != 'paid' THEN subtotal_ht ELSE 0 END) AS outstanding_revenue,
                    COUNT(*) AS invoice_count
                FROM raw_invoices
                GROUP BY 1
                ORDER BY 1
            """)
        else:
            con.execute("CREATE TABLE invoiced_revenue_monthly (month DATE, invoiced_revenue DOUBLE, collected_revenue DOUBLE, outstanding_revenue DOUBLE, invoice_count INTEGER)")
    else:
        con.execute("CREATE TABLE invoiced_revenue_monthly (month DATE, invoiced_revenue DOUBLE, collected_revenue DOUBLE, outstanding_revenue DOUBLE, invoice_count INTEGER)")

    attio_path = paths.raw_attio_dir / "attio_funnel_extract.csv"
    attio_rows = csv_rows(attio_path)
    create_table_from_dicts(con, "raw_attio_funnel", attio_rows)
    con.execute("""
        CREATE TABLE attio_funnel AS
        SELECT
            stage_or_source,
            CAST(count AS INTEGER) AS count,
            CAST(default_probability AS DOUBLE) AS default_probability,
            CAST(default_deal_value_eur AS DOUBLE) AS default_deal_value_eur,
            CAST(count AS DOUBLE) * CAST(default_probability AS DOUBLE) * CAST(default_deal_value_eur AS DOUBLE) AS weighted_pipeline_eur,
            notes
        FROM raw_attio_funnel
    """)

    con.close()
