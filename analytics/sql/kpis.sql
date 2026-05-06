-- DuckDB analytics on published month/region KPIs (CSV).
-- Run via: python analytics/run_sql_kpis.py

CREATE OR REPLACE VIEW month_region AS
SELECT * FROM read_csv_auto('{{PUBLISHED}}/month_region_kpis.csv');

CREATE OR REPLACE VIEW product_rank AS
SELECT * FROM read_csv_auto('{{PUBLISHED}}/product_rankings.csv');

-- KPI 1: Total revenue & profit
SELECT
  ROUND(SUM(Revenue), 2) AS total_revenue,
  ROUND(SUM(Profit), 2) AS total_profit,
  ROUND(SUM(Profit) / NULLIF(SUM(Revenue), 0), 4) AS portfolio_margin
FROM month_region;

-- KPI 2: Best region by cumulative profit
SELECT Region,
       ROUND(SUM(Revenue), 2) AS revenue,
       ROUND(SUM(Profit), 2) AS profit
FROM month_region
GROUP BY 1
ORDER BY profit DESC;

-- KPI 3: Year-over-year revenue (same calendar months, summed)
WITH ym AS (
  SELECT Year, Month, SUM(Revenue) AS rev
  FROM month_region
  GROUP BY Year, Month
)
SELECT b.Year AS y2,
       a.Year AS y1,
       ROUND(SUM(b.rev), 2) AS revenue_new_year,
       ROUND(SUM(a.rev), 2) AS revenue_prev_year,
       ROUND(100.0 * (SUM(b.rev) - SUM(a.rev)) / NULLIF(SUM(a.rev), 0), 2) AS yoy_pct
FROM ym a
JOIN ym b ON a.Month = b.Month AND b.Year = a.Year + 1
GROUP BY b.Year, a.Year
ORDER BY y2;

-- KPI 4: Top 5 product margin sanity (spot negative margins)
SELECT Product,
       ROUND(margin_pct, 4) AS margin_pct,
       ROUND(Revenue, 2) AS revenue
FROM product_rank
ORDER BY margin_pct ASC
LIMIT 5;
