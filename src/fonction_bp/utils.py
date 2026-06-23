from __future__ import annotations
import calendar
import csv
import datetime as dt
import json
from decimal import Decimal
import re
import zipfile
from pathlib import Path
from typing import Any, Iterable

import yaml

MONTH_FMT = "%Y-%m-%d"


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _json_default(obj):
    if isinstance(obj, (dt.date, dt.datetime)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=_json_default)


def month_start(value: str | dt.date | dt.datetime) -> dt.date:
    if isinstance(value, dt.datetime):
        return dt.date(value.year, value.month, 1)
    if isinstance(value, dt.date):
        return dt.date(value.year, value.month, 1)
    return dt.datetime.strptime(str(value), MONTH_FMT).date().replace(day=1)


def month_range(start: str | dt.date, end: str | dt.date) -> list[dt.date]:
    cur = month_start(start)
    end_date = month_start(end)
    out: list[dt.date] = []
    while cur <= end_date:
        out.append(cur)
        cur = add_months(cur, 1)
    return out


def add_months(value: dt.date, months: int) -> dt.date:
    month = value.month - 1 + months
    year = value.year + month // 12
    month = month % 12 + 1
    return dt.date(year, month, 1)


def parse_fr_amount(value: str | None) -> float:
    if value is None:
        return 0.0
    s = str(value).strip().replace("\u202f", "").replace(" ", "").replace(",", ".")
    if not s:
        return 0.0
    try:
        return float(s)
    except ValueError:
        return 0.0


def parse_qonto_datetime(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    value = value.strip()
    if not value:
        return None
    for fmt in ("%d-%m-%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            return dt.datetime.strptime(value, fmt)
        except ValueError:
            pass
    return None


def read_qonto_rows(zip_path: Path) -> list[dict[str, str]]:
    with zipfile.ZipFile(zip_path) as zf:
        names = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        if not names:
            raise FileNotFoundError(f"No CSV found in {zip_path}")
        text = zf.read(names[0]).decode("utf-8-sig")
    return list(csv.DictReader(text.splitlines(), delimiter=";"))


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def normalize_text(value: str | None) -> str:
    return (value or "").upper()


def fmt_eur(value: float) -> str:
    if abs(value) >= 1_000_000:
        return f"{value/1_000_000:.1f}M€".replace(".0", "")
    if abs(value) >= 1_000:
        return f"{value/1_000:.0f}k€"
    return f"{value:.0f}€"


def fmt_pct(value: float) -> str:
    return f"{value*100:.0f}%"


def year_quarter(value: dt.date) -> str:
    return f"Q{((value.month - 1)//3) + 1} {str(value.year)[-2:]}"


def annualize_mrr(mrr: float) -> float:
    return mrr * 12


def create_table_from_dicts(con, table_name: str, rows: list[dict[str, Any]], columns: list[tuple[str, str]] | None = None) -> None:
    """Create a DuckDB table from a list of dictionaries without pandas."""
    con.execute(f"DROP TABLE IF EXISTS {table_name}")
    if not rows and columns is None:
        raise ValueError(f"No rows or schema provided for {table_name}")
    if columns is None:
        first = rows[0]
        columns = []
        for key, value in first.items():
            if isinstance(value, int):
                typ = "INTEGER"
            elif isinstance(value, float):
                typ = "DOUBLE"
            else:
                typ = "VARCHAR"
            columns.append((key, typ))
    col_sql = ", ".join(f"{name} {typ}" for name, typ in columns)
    con.execute(f"CREATE TABLE {table_name} ({col_sql})")
    if rows:
        names = [c[0] for c in columns]
        placeholders = ", ".join(["?"] * len(names))
        con.executemany(f"INSERT INTO {table_name} ({', '.join(names)}) VALUES ({placeholders})", [[row.get(name) for name in names] for row in rows])
