# Pillar 1 — Analytics storytelling (Tableau · Power BI · Figma)

End-to-end path from the **Python notebook** to executive-ready BI assets.

| Layer | Role |
|--------|------|
| **Notebook** (`Toy-Sales-Analytics.ipynb`) | Source of truth: cleaning, features (`Revenue`, `Profit`, calendars). |
| **Exports** | Curated CSVs for BI (no raw duplication—export once after the cleaning cells). |
| **Figma** | Low-fi layout before you invest time in workbook tabs (`figma/`). |
| **Tableau / Power BI** | Dashboards on aggregates (`tableau/`, `powerbi/`). |

## Suggested exports (from your fields)

After your cleaned frame exists in the notebook, materialize at least:

1. `exports/sales_grain.csv` — row-level or `Product × Date × Region` with `Revenue`, `Profit`, `Units Sold`, `Unit Cost`, `Unit Price`.
2. `exports/month_region_kpis.csv` — `Year`, `Month`, `Region`, sum Revenue, sum Profit, sum Units.
3. `exports/product_rankings.csv` — `Product`, total Revenue, total Profit, margin %.

Use `scripts/export_for_bi.py` once you point `CLEAN_CSV` at your saved cleaned file (see script docstring).

## Resume phrasing (examples)

- *Designed dashboard wireframes in **Figma**, then built **Tableau / Power BI** views on Python-derived aggregates aligned with notebook EDA.*
- *Shipped stakeholder-ready time/region/SKU narratives consistent with the Jupyter analysis pipeline.*
