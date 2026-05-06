#!/usr/bin/env python3
"""Populate docs/ for GitHub Pages from published dashboard + report."""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def main() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    dash = ROOT / "analytics_stack" / "published" / "dashboard.html"
    wire = ROOT / "analytics_stack" / "published" / "wireframe_dashboard.svg"
    if dash.exists():
        shutil.copy(dash, DOCS / "dashboard.html")
    if wire.exists():
        shutil.copy(wire, DOCS / "wireframe_dashboard.svg")
    hub = f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Toy Sales — Data lab</title>
<style>
body {{ font-family: system-ui, sans-serif; max-width: 640px; margin: 3rem auto; padding: 0 1rem; color: #1d1d1f; }}
a {{ display: block; margin: 0.75rem 0; color: #2b7fd4; font-weight: 600; }}
p {{ color: #6e6e73; }}
</style></head><body>
<h1>Toy Sales Analytics</h1>
<p>Interactive dashboard + analyst report (GitHub Pages)</p>
<a href="dashboard.html">Interactive dashboard (Plotly)</a>
<a href="report.html">Analyst report (HTML)</a>
<a href="wireframe_dashboard.svg">Wireframe SVG</a>
</body></html>"""
    (DOCS / "index.html").write_text(hub, encoding="utf-8")
    print("docs/ ready for GitHub Pages → Settings → Pages → /docs on main")


if __name__ == "__main__":
    main()
