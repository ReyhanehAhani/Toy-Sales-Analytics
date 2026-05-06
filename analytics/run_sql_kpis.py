#!/usr/bin/env python3
"""Execute DuckDB KPI queries from analytics/sql/kpis.sql and save summary."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
PUBLISHED = (ROOT / "analytics_stack" / "published").resolve()
OUT = ROOT / "analytics" / "reports" / "sql_kpi_summary.txt"


def load_sql() -> str:
    raw = (ROOT / "analytics" / "sql" / "kpis.sql").read_text(encoding="utf-8")
    return raw.replace("{{PUBLISHED}}", str(PUBLISHED).replace("\\", "/"))


def main() -> int:
    if not (PUBLISHED / "month_region_kpis.csv").exists():
        print("Missing published CSVs. Run: python tools/build_published_deliverables.py", file=sys.stderr)
        return 1
    con = duckdb.connect(database=":memory:")
    sql = load_sql()
    chunks = [c.strip() for c in re.split(r";", sql) if c.strip() and not c.strip().startswith("--")]
    lines: list[str] = []
    for block in chunks:
        if block.upper().startswith("CREATE "):
            con.execute(block)
            continue
        if block.upper().startswith("SELECT"):
            lines.append(block.split("\n")[0][:120] + " …")
            df = con.execute(block).fetchdf()
            lines.append(df.to_string(index=False))
            lines.append("")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
