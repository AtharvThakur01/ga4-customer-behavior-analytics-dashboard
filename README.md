# GA4 Customer Behavior Analytics Dashboard

I built this project as a customer analytics dashboard inspired by Google Analytics 4 concepts. It monitors user behavior, engagement metrics, event tracking, conversion performance, and stakeholder-ready digital product insights.

## What I Built

- Developed an interactive customer behavior dashboard with channel and audience segment filters.
- Implemented KPI tracking for users, engagement, checkout completion, purchases, revenue, and conversion rate.
- Built GA4-style event analysis for `page_view`, `user_engagement`, `add_to_cart`, `begin_checkout`, and `purchase`.
- Added a Python reporting workflow that validates GA4-style event exports and generates conversion reporting outputs.
- Created Excel-ready and stakeholder-ready reports for analytics review, dashboard QA, and digital product optimization.
- Documented the measurement plan, conversion tracking approach, Looker Studio reporting brief, and QA checklist.

## Recruiter Evidence

| Resume Claim | Where It Is Demonstrated |
| --- | --- |
| GA4-inspired customer analytics dashboard | `index.html`, `src/app.js`, `src/styles.css` |
| User behavior and engagement metrics | Dashboard KPIs and funnel sections |
| Event analysis and conversion-focused reporting | `data/sample-ga4-events.csv`, `scripts/build_report.py` |
| Data validation and plausibility checks | `validate()` logic in `scripts/build_report.py` |
| Excel reporting workflow | `reports/ga4-channel-conversion-summary.xlsx` and `reports/ga4-channel-conversion-summary.csv` |
| Stakeholder insights and visual reports | `reports/stakeholder-insights.md` and `reports/stakeholder-visual-report.html` |
| Looker Studio and measurement planning | `docs/looker-studio-brief.md`, `docs/measurement-plan.md` |

## Run The Dashboard

Open `index.html` in a browser.

## Rebuild Reports

```bash
python scripts/build_report.py
```

The script generates:

- `reports/ga4-channel-conversion-summary.csv`
- `reports/ga4-channel-conversion-summary.xlsx`
- `reports/stakeholder-insights.md`
- `reports/stakeholder-visual-report.html`

## Project Structure

```text
.
├── data/
│   └── sample-ga4-events.csv
├── docs/
│   ├── looker-studio-brief.md
│   └── measurement-plan.md
├── reports/
│   ├── ga4-channel-conversion-summary.csv
│   ├── ga4-channel-conversion-summary.xlsx
│   ├── stakeholder-insights.md
│   └── stakeholder-visual-report.html
├── scripts/
│   └── build_report.py
├── src/
│   ├── app.js
│   └── styles.css
└── index.html
```

## Skills Demonstrated

Google Analytics 4 concepts, GA4 event tracking, conversion tracking, Looker Studio reporting, Python, Excel reporting, dashboards, data validation, customer behavior analytics, KPI tracking, stakeholder insights, digital product optimization, data visualization.

## Business Scenario

An ecommerce product team needs a weekly analytics view that connects acquisition quality, customer behavior, event instrumentation, checkout behavior, and revenue outcomes. This project demonstrates how I would turn GA4-style event data into dashboards, reports, and stakeholder recommendations.
