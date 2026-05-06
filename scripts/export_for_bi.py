#!/usr/bin/env python3
"""Export aggregate CSVs for Tableau / Power BI from a cleaned toy-sales CSV.

Usage:
  python scripts/export_for_bi.py path/to/cleaned_sales.csv analytics_stack/exports

Expected columns (after your notebook cleaning): at minimum
  Product, Date, Region, Units Sold, Unit Cost, Unit Price
plus Revenue, Profit, Year, Month, Quarter if already engineered; otherwise this script computes them.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


def _ensure_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "Revenue" not in out.columns:
        out["Revenue"] = out["Units Sold"] * out["Unit Price"]
    if "Profit" not in out.columns:
        out["Profit"] = out["Revenue"] - out["Units Sold"] * out["Unit Cost"]
    if "Date" in out.columns and "Year" not in out.columns:
        dt = pd.to_datetime(out["Date"], errors="coerce")
        out["Year"] = dt.dt.year
        out["Month"] = dt.dt.month
        out["Quarter"] = dt.dt.quarter
    return out


def main() -> None:
    p = argparse.ArgumentParser(description="Export BI-ready CSVs for toy sales.")
    p.add_argument("input_csv", type=Path, help="Cleaned row-level CSV from the notebook pipeline")
    p.add_argument("out_dir", type=Path, nargs="?", default=Path("analytics_stack/exports"))
    args = p.parse_args()

    if not args.input_csv.is_file():
        print(f"Missing input: {args.input_csv}", file=sys.stderr)
        sys.exit(1)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(args.input_csv)
    required = {"Product", "Region", "Units Sold", "Unit Cost", "Unit Price"}
    miss = required - set(df.columns)
    if miss:
        print(f"Input CSV missing columns: {miss}", file=sys.stderr)
        sys.exit(1)

    df = _ensure_features(df)
    if "Year" not in df.columns or "Month" not in df.columns:
        print("After feature prep, 'Year' and 'Month' are required (add a Date column or pre-compute Year/Month).", file=sys.stderr)
        sys.exit(1)

    grain = args.out_dir / "sales_grain.csv"
    df.to_csv(grain, index=False)

    g = df.groupby(["Year", "Month", "Region"], as_index=False).agg(
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum"),
        Units_Sold=("Units Sold", "sum"),
    )
    month_path = args.out_dir / "month_region_kpis.csv"
    g.to_csv(month_path, index=False)

    pr = (
        df.groupby("Product", as_index=False)
        .agg(Revenue=("Revenue", "sum"), Profit=("Profit", "sum"), Units_Sold=("Units Sold", "sum"))
        .sort_values("Profit", ascending=False)
    )
    pr["margin_pct"] = (pr["Profit"] / pr["Revenue"]).where(pr["Revenue"] != 0)
    pr_path = args.out_dir / "product_rankings.csv"
    pr.to_csv(pr_path, index=False)

    for path in (grain, month_path, pr_path):
        print("Wrote:", path)


if __name__ == "__main__":
    main()
