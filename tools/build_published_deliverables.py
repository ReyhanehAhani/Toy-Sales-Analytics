#!/usr/bin/env python3
"""Regenerate committed portfolio artifacts (CSV + interactive HTML + wireframe SVG).

Run from repo root:
  python tools/build_published_deliverables.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)
REGIONS = ["A", "B", "C"]
PRODUCTS = [f"Toy SKU {i:02d}" for i in range(1, 31)]


def synthetic_sales(n_rows: int = 2000) -> pd.DataFrame:
    start = pd.Timestamp("2022-01-01")
    rows = []
    for i in range(n_rows):
        day = start + pd.Timedelta(days=int(i % 640))
        rows.append(
            {
                "Product": str(RNG.choice(PRODUCTS)),
                "Date": day.strftime("%Y-%m-%d"),
                "Region": str(RNG.choice(REGIONS)),
                "Units Sold": int(RNG.integers(8, 220)),
                "Unit Cost": round(float(RNG.uniform(3.5, 14.0)), 2),
                "Unit Price": round(float(RNG.uniform(9.0, 42.0)), 2),
            }
        )
    df = pd.DataFrame(rows)
    df["Revenue"] = df["Units Sold"] * df["Unit Price"]
    df["Profit"] = df["Revenue"] - df["Units Sold"] * df["Unit Cost"]
    dt = pd.to_datetime(df["Date"])
    df["Year"] = dt.dt.year.astype(int)
    df["Month"] = dt.dt.month.astype(int)
    df["Quarter"] = dt.dt.quarter.astype(int)
    return df


def write_dashboard_html(out: Path, month_kpis: pd.DataFrame, product_rank: pd.DataFrame) -> None:
    payload = {
        "months": month_kpis.groupby(["Year", "Month"], sort=False)["Revenue"]
        .sum()
        .reset_index()
        .assign(label=lambda d: d["Year"].astype(str) + "-" + d["Month"].astype(str).str.zfill(2))
        .to_dict("records"),
        "by_region_month": month_kpis.to_dict("records"),
        "products": product_rank.head(12).to_dict("records"),
        "kpis": {
            "revenue": float(month_kpis["Revenue"].sum()),
            "profit": float(month_kpis["Profit"].sum()),
            "skus": int(product_rank.shape[0]),
        },
    }
    json_blob = json.dumps(payload)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Toy Sales — published dashboard</title>
  <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
  <style>
    :root {{ --bg:#f5f9fc; --card:#fff; --accent:#2b7fd4; --text:#1d1d1f; --muted:#6e6e73; }}
    body {{ font-family: system-ui, sans-serif; margin:0; background:var(--bg); color:var(--text); }}
    header {{ padding:1.25rem 1.5rem; background:var(--card); border-bottom:1px solid #e2e8f0; }}
    h1 {{ margin:0; font-size:1.25rem; }}
    .sub {{ color:var(--muted); font-size:0.9rem; margin-top:0.35rem; }}
    main {{ padding:1rem 1.25rem 2rem; max-width:1200px; margin:0 auto; }}
    .kpis {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); gap:12px; margin-bottom:16px; }}
    .kpi {{ background:var(--card); border-radius:14px; padding:14px 16px; border:1px solid #e2e8f0; }}
    .kpi label {{ display:block; font-size:0.72rem; text-transform:uppercase; letter-spacing:0.06em; color:var(--muted); }}
    .kpi strong {{ font-size:1.35rem; }}
    .grid2 {{ display:grid; grid-template-columns:1fr; gap:14px; }}
    @media(min-width:900px){{ .grid2 {{ grid-template-columns:1.1fr 0.9fr; }} }}
    .panel {{ background:var(--card); border-radius:14px; padding:8px; border:1px solid #e2e8f0; min-height:320px; }}
    footer {{ font-size:0.8rem; color:var(--muted); padding:0 1.25rem 2rem; max-width:1200px; margin:0 auto; }}
    a {{ color:var(--accent); }}
  </style>
</head>
<body>
  <header>
    <h1>Toy sales analytics — live dashboard</h1>
    <div class="sub">Built from the same aggregates as <code>month_region_kpis.csv</code> / <code>product_rankings.csv</code> — import those files into Power BI or Tableau for the same story.</div>
  </header>
  <main>
    <div class="kpis" id="kpiRow"></div>
    <div class="grid2">
      <div class="panel" id="lineChart"></div>
      <div class="panel" id="barChart"></div>
    </div>
  </main>
  <footer>
    Open this file locally or via GitHub Pages. CSV twins live in this folder for BI tools.
  </footer>
  <script>
    const DATA = {json_blob};

    const fmt = (n) => new Intl.NumberFormat(undefined, {{ style: 'currency', currency: 'USD', maximumFractionDigits: 0 }}).format(n);
    document.getElementById('kpiRow').innerHTML = `
      <div class="kpi"><label>Total revenue</label><strong>${{fmt(DATA.kpis.revenue)}}</strong></div>
      <div class="kpi"><label>Total profit</label><strong>${{fmt(DATA.kpis.profit)}}</strong></div>
      <div class="kpi"><label>Active SKUs</label><strong>${{DATA.kpis.skus}}</strong></div>
    `;

    const t = DATA.months;
    Plotly.newPlot('lineChart', [{{
      x: t.map(d => d.label),
      y: t.map(d => d.Revenue),
      type: 'scatter',
      mode: 'lines+markers',
      line: {{ color: '#2b7fd4', width: 3 }},
      name: 'Revenue'
    }}], {{
      margin: {{ t: 20, r: 20, b: 48, l: 56 }},
      title: 'Revenue by month',
      paper_bgcolor: 'rgba(0,0,0,0)',
      plot_bgcolor: '#fbfcfe',
      font: {{ family: 'system-ui, sans-serif' }}
    }}, {{ responsive: true }});

    const p = DATA.products;
    Plotly.newPlot('barChart', [{{
      y: p.map(r => r.Product).reverse(),
      x: p.map(r => r.Profit).reverse(),
      type: 'bar',
      orientation: 'h',
      marker: {{ color: '#2b7fd4' }}
    }}], {{
      margin: {{ t: 20, r: 20, b: 40, l: 120 }},
      title: 'Top products by profit',
      paper_bgcolor: 'rgba(0,0,0,0)',
      plot_bgcolor: '#fbfcfe'
    }}, {{ responsive: true }});
  </script>
</body>
</html>
"""
    out.write_text(html, encoding="utf-8")


def write_wireframe_svg(path: Path) -> None:
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="920" height="420" viewBox="0 0 920 420">
  <rect width="100%" height="100%" fill="#f5f9fc"/>
  <text x="24" y="36" font-size="20" font-family="system-ui,sans-serif" fill="#1d1d1f" font-weight="600">Toy sales dashboard — wireframe</text>
  <text x="24" y="58" font-size="13" font-family="system-ui,sans-serif" fill="#6e6e73">Figma / handoff spec (vector). KPI strip + trend + SKU pareto.</text>
  <rect x="20" y="80" width="200" height="72" rx="12" fill="#ffffff" stroke="#e2e8f0"/>
  <rect x="236" y="80" width="200" height="72" rx="12" fill="#ffffff" stroke="#e2e8f0"/>
  <rect x="452" y="80" width="200" height="72" rx="12" fill="#ffffff" stroke="#e2e8f0"/>
  <rect x="20" y="170" width="560" height="220" rx="14" fill="#ffffff" stroke="#e2e8f0"/>
  <rect x="600" y="170" width="300" height="220" rx="14" fill="#ffffff" stroke="#e2e8f0"/>
  <text x="36" y="118" font-size="12" fill="#6e6e73" font-family="system-ui,sans-serif">KPI: Revenue</text>
  <text x="252" y="118" font-size="12" fill="#6e6e73" font-family="system-ui,sans-serif">KPI: Profit</text>
  <text x="468" y="118" font-size="12" fill="#6e6e73" font-family="system-ui,sans-serif">KPI: Top region</text>
  <text x="40" y="200" font-size="13" fill="#2b7fd4" font-family="system-ui,sans-serif" font-weight="600">Main: Revenue trend</text>
  <text x="620" y="200" font-size="13" fill="#2b7fd4" font-family="system-ui,sans-serif" font-weight="600">Pareto: SKU profit</text>
  <line x1="48" y1="340" x2="520" y2="280" stroke="#2b7fd4" stroke-width="3" stroke-linecap="round"/>
  <rect x="640" y="230" width="28" height="120" rx="4" fill="#2b7fd4" opacity="0.85"/>
  <rect x="690" y="260" width="28" height="90" rx="4" fill="#2b7fd4" opacity="0.65"/>
  <rect x="740" y="290" width="28" height="60" rx="4" fill="#2b7fd4" opacity="0.45"/>
</svg>"""
    path.write_text(svg, encoding="utf-8")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    pub = root / "analytics_stack" / "published"
    pub.mkdir(parents=True, exist_ok=True)

    df = synthetic_sales(2000)
    df.to_csv(pub / "sales_grain_demo.csv", index=False)

    g = df.groupby(["Year", "Month", "Region"], as_index=False).agg(
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum"),
        Units_Sold=("Units Sold", "sum"),
    )
    g.to_csv(pub / "month_region_kpis.csv", index=False)

    pr = (
        df.groupby("Product", as_index=False)
        .agg(Revenue=("Revenue", "sum"), Profit=("Profit", "sum"), Units_Sold=("Units Sold", "sum"))
        .sort_values("Profit", ascending=False)
    )
    pr["margin_pct"] = (pr["Profit"] / pr["Revenue"]).where(pr["Revenue"] != 0)
    pr.to_csv(pub / "product_rankings.csv", index=False)

    write_dashboard_html(pub / "dashboard.html", g, pr)
    write_wireframe_svg(pub / "wireframe_dashboard.svg")

    print("Wrote deliverables to", pub)


if __name__ == "__main__":
    main()
