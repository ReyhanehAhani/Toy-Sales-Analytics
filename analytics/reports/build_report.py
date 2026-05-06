#!/usr/bin/env python3
"""Build a simple static HTML report (case study + SQL summary + links)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MD = ROOT / "analytics" / "reports" / "case_study.md"
SQL_TXT = ROOT / "analytics" / "reports" / "sql_kpi_summary.txt"
OUT = ROOT / "analytics" / "reports" / "ANALYST_REPORT.html"
DOCS_OUT = ROOT / "docs" / "report.html"


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def md_to_html(md: str) -> str:
    """Tiny markdown: #, ##, paragraphs, `code`."""
    out: list[str] = []
    for block in md.split("\n\n"):
        b = block.strip()
        if not b:
            continue
        if b.startswith("# "):
            out.append(f"<h1>{esc(b[2:])}</h1>")
        elif b.startswith("## "):
            out.append(f"<h2>{esc(b[3:])}</h2>")
        else:
            lines = []
            for line in b.split("\n"):
                if line.startswith("- "):
                    lines.append(f"<li>{esc(line[2:])}</li>")
                else:
                    lines.append(f"<p>{esc(line)}</p>")
            if any("<li>" in x for x in lines):
                out.append("<ul>" + "".join(x for x in lines if "<li>" in x) + "</ul>")
            else:
                out.append("".join(lines))
    return "\n".join(out)


def main() -> None:
    md = MD.read_text(encoding="utf-8")
    sql_block = ""
    if SQL_TXT.exists():
        sql_block = f"<h2>SQL output snapshot</h2><pre>{esc(SQL_TXT.read_text(encoding='utf-8'))}</pre>"
    body = md_to_html(md) + sql_block
    html = f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Toy Sales — Analyst report</title>
<style>
body {{ font-family: system-ui, sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 1rem; line-height: 1.55; color: #1d1d1f; }}
pre {{ background: #f5f9fc; padding: 1rem; overflow: auto; border-radius: 8px; border: 1px solid #e2e8f0; font-size: 0.85rem; }}
a {{ color: #2b7fd4; }}
h1, h2 {{ letter-spacing: -0.02em; }}
</style></head><body>
<p><a href="index.html">← Data lab hub</a> · <a href="dashboard.html">Interactive dashboard</a></p>
{body}
</body></html>"""
    OUT.write_text(html, encoding="utf-8")
    DOCS_OUT.parent.mkdir(parents=True, exist_ok=True)
    DOCS_OUT.write_text(html, encoding="utf-8")
    print("Wrote", OUT, "and", DOCS_OUT)


if __name__ == "__main__":
    main()
