# Tableau — Toy Sales

## Data connection

1. In the notebook, export `exports/month_region_kpis.csv` and `exports/product_rankings.csv` (see `analytics_stack/README.md`).
2. **Connect → Text file →** choose the CSV.
3. If you use both files, relate on `Region` / `Month` / `Year` where applicable, or use **blending** for simple demos.

## Recommended sheets

- **Revenue trend:** `Month` on columns, `SUM(Revenue)` line; `Region` on color or filter.
- **Regional KPIs:** bar chart `Region` vs `SUM(Profit)`.
- **Pareto:** `Product` sorted by `SUM(Profit)`, dual axis cumulative %.

## Dashboard

- Use the same layout as `../figma/dashboard_wireframe.md`.
- **Actions:** filter across sheets by `Region` and `Year`.

## Resume

- *Built **Tableau** dashboards on notebook-validated aggregates; matched EDA narratives used in Jupyter.*
