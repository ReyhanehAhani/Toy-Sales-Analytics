#!/usr/bin/env python3
"""Data-quality checks on analytics_stack/published CSVs (fail fast for CI)."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PUB = ROOT / "analytics_stack" / "published"


def check_month_region(df: pd.DataFrame) -> list[str]:
    errs: list[str] = []
    need = {"Year", "Month", "Region", "Revenue", "Profit", "Units_Sold"}
    if need - set(df.columns):
        errs.append(f"month_region_kpis missing columns: {need - set(df.columns)}")
        return errs
    if df["Year"].dtype != "int64" and not pd.api.types.is_integer_dtype(df["Year"]):
        errs.append("Year should be integer")
    if not df["Month"].between(1, 12).all():
        errs.append("Month out of 1..12")
    if not df["Region"].isin(["A", "B", "C"]).all():
        errs.append("Region outside {A,B,C}")
    if df["Revenue"].isna().any() or (df["Revenue"] < 0).any():
        errs.append("Revenue null or negative")
    if df["Units_Sold"].isna().any() or (df["Units_Sold"] <= 0).any():
        errs.append("Units_Sold invalid")
    return errs


def check_products(df: pd.DataFrame) -> list[str]:
    errs: list[str] = []
    need = {"Product", "Revenue", "Profit", "Units_Sold", "margin_pct"}
    if need - set(df.columns):
        errs.append(f"product_rankings missing columns: {need - set(df.columns)}")
        return errs
    if df["margin_pct"].isna().any():
        errs.append("margin_pct has nulls")
    if not df["margin_pct"].between(-1.0, 1.0).fillna(False).all():
        bad = df.loc[~df["margin_pct"].between(-1.0, 1.0), "margin_pct"]
        if len(bad):
            errs.append(f"margin_pct out of [-1,1]: {bad.iloc[:3].tolist()}")
    return errs


def check_grain(df: pd.DataFrame) -> list[str]:
    errs: list[str] = []
    need = {"Product", "Date", "Region", "Units Sold", "Unit Cost", "Unit Price", "Revenue", "Profit"}
    miss = need - set(df.columns)
    if miss:
        errs.append(f"sales_grain_demo missing: {miss}")
    return errs


def main() -> int:
    all_err: list[str] = []
    mr = pd.read_csv(PUB / "month_region_kpis.csv")
    all_err += check_month_region(mr)
    pr = pd.read_csv(PUB / "product_rankings.csv")
    all_err += check_products(pr)
    sg = pd.read_csv(PUB / "sales_grain_demo.csv")
    all_err += check_grain(sg)
    if all_err:
        print("DATA QUALITY FAILED:", file=sys.stderr)
        for e in all_err:
            print(" -", e, file=sys.stderr)
        return 1
    print("OK: toy sales published CSVs passed checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
