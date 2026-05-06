# Toy Sales — Analyst case study

## Business question

Where do we earn money (region × time), which SKUs drive profit, and are margins structurally sound?

## Data

Published demo grain + KPI tables in `analytics_stack/published/` (regenerable via `tools/build_published_deliverables.py`). Columns follow the notebook: `Product`, `Date`, `Region`, units, cost/price, engineered `Revenue` / `Profit`.

## KPI definitions

- **Revenue** = Units × Unit price  
- **Profit** = Revenue − Units × Unit cost  
- **Portfolio margin** = ΣProfit / ΣRevenue  
- **YoY** = compare summed monthly revenue across consecutive calendar years on aligned months (see `analytics/sql/kpis.sql`)

## Quality gates

Automated checks in `analytics/quality/validate_published.py` (non-nulls, region enum, margin bounds).

## SQL analytics

DuckDB executes the same KPI logic you would ship to a warehouse layer: `analytics/run_sql_kpis.py` materializes `analytics/reports/sql_kpi_summary.txt`.

## Takeaways (demo data)

Open `docs/dashboard.html` after enabling GitHub Pages, or run the Plotly dashboard locally — trend + SKU pareto should match the SQL aggregates.

## Limitations

Demo CSV is synthetic but schema-aligned; swap in cleaned notebook exports for production narratives.
