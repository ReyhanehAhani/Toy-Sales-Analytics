# Toy Sales Analytics

This project analyzes 21 months of sales and inventory data from a Mexican toy company to uncover key insights about revenue, inventory management, and seasonal trends. It combines data cleaning, exploratory data analysis (EDA), and visualization techniques to support strategic business decisions.

## Objectives

- Understand sales trends over time and across regions
- Evaluate product performance and profitability
- Identify seasonality and monthly patterns
- Support inventory and marketing optimization

## Dataset

The dataset includes 8126 records with the following fields:
- `Product` – Toy name
- `Date` – Sale date
- `Region` – Sales region (A/B/C)
- `Units Sold` – Number of units sold
- `Unit Cost` – Cost per unit
- `Unit Price` – Selling price per unit

## Technologies Used

- **Python 3**
- **Pandas** – data manipulation
- **Matplotlib & Seaborn** – visualizations
- **NumPy** – numeric computation
- **Jupyter Notebook** – analysis environment

## Analysis Pipeline

### 1. Data Cleaning
- Converted date format
- Removed duplicates and missing values
- Checked for outliers

### 2. Feature Engineering
- Computed `Revenue` = `Units Sold` × `Unit Price`
- Computed `Profit` = `Revenue` – (`Units Sold` × `Unit Cost`)
- Extracted `Year`, `Month`, and `Quarter` from date

### 3. Exploratory Data Analysis (EDA)
- Revenue and profit trends by month and region
- Top and bottom-performing products
- Regional sales comparison
- Seasonal and monthly pattern identification
- Profit margin distribution

### 4. Business Insights
- Region C consistently performs best across metrics
- Profits peak during holidays and end-of-year months
- Some low-selling items show high profit margins
- Recommendation: reallocate marketing focus and optimize inventory for top SKUs

## Sample Visualizations

- Revenue by Month (line chart)
- Product-wise Profit Distribution (bar chart)
- Monthly Units Sold Heatmap
- Region-wise Quarterly Performance (box plot)

## Key Takeaways

- Inventory optimization can reduce overhead during low-demand months.
- Region C should be prioritized for new product launches.
- Top 10 profitable products generate over 40% of total profit.

## Files

- `Toy-Sales-Analytics.ipynb`: Main analysis notebook
- `Toy-Sales-Analytics-report.pdf`: Summarized business report with key visuals and conclusions
- `analytics_stack/`: **Portfolio track — Tableau, Power BI, Figma** (exports + playbooks)
- `analytics_stack/published/`: **Ready-to-view** `dashboard.html`, `wireframe_dashboard.svg`, and CSV twins for BI tools (regenerate via `tools/build_published_deliverables.py`)
- `scripts/export_for_bi.py`: Pandas helper to emit BI-ready CSVs after you save a cleaned table from the notebook

---

## Portfolio stack — Pillar 1 (storytelling)

- **Figma:** layout spec in `analytics_stack/figma/dashboard_wireframe.md` (build the deck in Figma, link it in your CV).
- **Tableau / Power BI:** step-by-step in `analytics_stack/tableau/` and `analytics_stack/powerbi/`.
- **CSV bridge:** run `python scripts/export_for_bi.py <cleaned.csv> analytics_stack/exports` (`pip install -r analytics_stack/requirements-analytics.txt`).

---

