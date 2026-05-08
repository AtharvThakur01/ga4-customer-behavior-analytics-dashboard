from __future__ import annotations

import csv
import html
import zipfile
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sample-ga4-events.csv"
REPORT_DIR = ROOT / "reports"


def read_rows() -> list[dict[str, str]]:
    with DATA_PATH.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def number(row: dict[str, str], key: str) -> float:
    return float(row[key])


def validate(rows: list[dict[str, str]]) -> None:
    required = {"date", "channel", "segment", "event_name", "users", "event_count", "conversions", "revenue"}
    missing = required - set(rows[0])
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    for row in rows:
        if number(row, "event_count") < 0 or number(row, "users") < 0:
            raise ValueError(f"Negative event values are not allowed for {row['channel']} {row['event_name']}")
        if row["event_name"] == "purchase" and number(row, "conversions") <= 0:
            raise ValueError(f"Purchase rows must include conversions for {row['channel']}")


def purchase_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [row for row in rows if row["event_name"] == "purchase"]


def channel_summary(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    page_views_by_channel = {
        row["channel"]: number(row, "event_count")
        for row in rows
        if row["event_name"] == "page_view"
    }
    summary = []
    for row in purchase_rows(rows):
        users = number(row, "users")
        conversions = number(row, "conversions")
        revenue = number(row, "revenue")
        summary.append(
            {
                "channel": row["channel"],
                "segment": row["segment"],
                "users": str(int(users)),
                "purchases": str(int(conversions)),
                "revenue": f"{revenue:.0f}",
                "conversion_rate": f"{(conversions / users) * 100:.2f}%",
                "revenue_per_user": f"{revenue / users:.2f}",
                "page_view_events": str(int(page_views_by_channel.get(row["channel"], 0))),
                "insight": insight(row),
            }
        )
    return summary


def insight(row: dict[str, str]) -> str:
    conversions = number(row, "conversions")
    users = number(row, "users")
    conversion_rate = conversions / users
    if conversion_rate >= 0.07:
        return "High-converting segment; protect budget and landing-page experience."
    if conversion_rate <= 0.025:
        return "Low conversion efficiency; audit acquisition intent and checkout path."
    return "Monitor performance and compare against weekly channel benchmark."


def write_csv(summary: list[dict[str, str]]) -> None:
    path = REPORT_DIR / "ga4-channel-conversion-summary.csv"
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(summary[0].keys()))
        writer.writeheader()
        writer.writerows(summary)


def write_markdown(summary: list[dict[str, str]]) -> None:
    total_users = sum(int(row["users"]) for row in summary)
    total_purchases = sum(int(row["purchases"]) for row in summary)
    total_revenue = sum(float(row["revenue"]) for row in summary)
    best = max(summary, key=lambda row: float(row["conversion_rate"].rstrip("%")))
    weakest = min(summary, key=lambda row: float(row["conversion_rate"].rstrip("%")))

    lines = [
        "# GA4 Customer Behavior Insight Report",
        "",
        f"Generated on {date.today().isoformat()} from `data/sample-ga4-events.csv`.",
        "",
        "## KPI Summary",
        "",
        f"- Users analyzed: {total_users:,}",
        f"- Purchase conversions: {total_purchases:,}",
        f"- Total revenue: ${total_revenue:,.0f}",
        f"- Blended conversion rate: {(total_purchases / total_users) * 100:.2f}%",
        "",
        "## Stakeholder Insights",
        "",
        f"- **{best['channel']}** is the highest converting channel at **{best['conversion_rate']}**.",
        f"- **{weakest['channel']}** needs optimization because conversion rate is **{weakest['conversion_rate']}**.",
        "- Validate ecommerce event parameters before publishing Looker Studio reports.",
        "- Segment new and returning users separately for conversion-focused analysis.",
        "",
        "## Validation Checks",
        "",
        "- Required GA4 export columns verified.",
        "- Purchase rows checked for positive conversions.",
        "- Event counts and user counts checked for impossible negative values.",
    ]
    (REPORT_DIR / "stakeholder-insights.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_html(summary: list[dict[str, str]]) -> None:
    rows = "\n".join(
        f"<tr><td>{html.escape(row['channel'])}</td><td>{row['purchases']}</td><td>{row['conversion_rate']}</td><td>${float(row['revenue']):,.0f}</td><td>{html.escape(row['insight'])}</td></tr>"
        for row in summary
    )
    document = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>GA4 Stakeholder Insight Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #18212f; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #d9e1ea; padding: 10px; text-align: left; }}
    th {{ background: #f6f8fb; }}
  </style>
</head>
<body>
  <h1>GA4 Customer Behavior Insight Report</h1>
  <p>Automated Python output for event analysis, conversion reporting, and stakeholder communication.</p>
  <table>
    <thead><tr><th>Channel</th><th>Purchases</th><th>Conversion Rate</th><th>Revenue</th><th>Insight</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</body>
</html>
"""
    (REPORT_DIR / "stakeholder-visual-report.html").write_text(document, encoding="utf-8")


def write_xlsx(summary: list[dict[str, str]]) -> None:
    headers = list(summary[0].keys())
    worksheet_rows = [headers, *[[row[key] for key in headers] for row in summary]]
    sheet_data = []
    for row_number, values in enumerate(worksheet_rows, start=1):
        cells = []
        for col_number, value in enumerate(values, start=1):
            cell_ref = f"{column_name(col_number)}{row_number}"
            cells.append(f'<c r="{cell_ref}" t="inlineStr"><is><t>{escape(str(value))}</t></is></c>')
        sheet_data.append(f'<row r="{row_number}">{"".join(cells)}</row>')

    files = {
        "[Content_Types].xml": """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>""",
        "_rels/.rels": """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>""",
        "xl/workbook.xml": """<?xml version="1.0" encoding="UTF-8"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets><sheet name="GA4 Channel Summary" sheetId="1" r:id="rId1"/></sheets>
</workbook>""",
        "xl/_rels/workbook.xml.rels": """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
</Relationships>""",
        "xl/worksheets/sheet1.xml": f"""<?xml version="1.0" encoding="UTF-8"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheetData>{"".join(sheet_data)}</sheetData>
</worksheet>""",
    }

    with zipfile.ZipFile(REPORT_DIR / "ga4-channel-conversion-summary.xlsx", "w", zipfile.ZIP_DEFLATED) as archive:
        for path, content in files.items():
            archive.writestr(path, content)


def column_name(number: int) -> str:
    name = ""
    while number:
        number, remainder = divmod(number - 1, 26)
        name = chr(65 + remainder) + name
    return name


def main() -> None:
    REPORT_DIR.mkdir(exist_ok=True)
    rows = read_rows()
    validate(rows)
    summary = channel_summary(rows)
    write_csv(summary)
    write_markdown(summary)
    write_html(summary)
    write_xlsx(summary)
    print(f"Built {len(summary)} GA4 channel reporting rows in {REPORT_DIR}")


if __name__ == "__main__":
    main()
