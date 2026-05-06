# Power BI — Toy Sales

## Import

1. **Get data → Text/CSV** → `exports/month_region_kpis.csv`.
2. Repeat for `exports/product_rankings.csv` if needed.
3. **Model** view: confirm types (`Month` as date or text consistently, `Region` as text).

## Measures (DAX examples)

```dax
Total Revenue = SUM('month_region_kpis'[Revenue])
Total Profit = SUM('month_region_kpis'[Profit])
Profit Margin = DIVIDE([Total Profit], [Total Revenue], BLANK())
```

Adjust table/column names to match your CSV headers.

## Report pages

1. **Overview:** KPI cards + line chart (revenue by month) + slicers for `Region`, `Year`.
2. **SKU:** table visual with `Product`, revenue, profit, margin.

Match layout to `../figma/dashboard_wireframe.md`.

## Resume

- *Prototyped layouts in **Figma**, delivered **Power BI** reports on Python-exported KPI tables.*
