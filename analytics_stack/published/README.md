# Published artifacts (open locally or on GitHub)

| File | What it is |
|------|------------|
| `dashboard.html` | **Interactive** Plotly dashboard — double-click or drag into a browser (or view raw on GitHub). |
| `*.csv` | Same numbers the dashboard uses — **Get Data → Text/CSV** in **Power BI** or **Tableau**. |
| `wireframe_dashboard.svg` | Vector wireframe (open in browser; drop into Figma / slides as reference). |

## Regenerate

```bash
python tools/build_published_deliverables.py
```

Committed outputs are checked in so the portfolio is **self-contained** (no extra steps for recruiters).
