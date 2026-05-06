# Toy sales — dashboard wireframe (Figma)

Duplicate this structure in **Figma** (frames + sticky notes for metrics). Goal: one screen an exec can read in under 60 seconds.

## Frame: Executive overview

| Zone | Content |
|------|---------|
| Top KPI strip (4 cards) | Total revenue, total profit, MoM revenue Δ%, top region (A/B/C). |
| Main chart | Line: revenue by month (filter: all regions / single region). |
| Secondary | Bar or pareto: top 10 products by profit. |
| Sidebar filters | Region, year, quarter, product category if you split products. |

## Frame: Drill-down

- Table: `Product`, `Units Sold`, `Revenue`, `Profit`, margin % — sortable.
- Optional heatmap: `Month × Region` for units or profit (matches your notebook story).

## Components to create in Figma

- Auto-layout rows for KPI cards (16–24 px padding, 8 pt grid).
- Named layers: `Filter_Region`, `Chart_RevenueTrend`, `Table_SKU`.
- Export a **PNG** for README or portfolio if you like; link the **Figma file** in the main repo README.

This file is the spec; the live deck lives in your Figma account.
