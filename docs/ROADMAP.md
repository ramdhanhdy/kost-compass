# Delivery roadmap

## 1. Repository and foundation
- Public portfolio repository; no credentials, phone numbers, contact-person details or raw page dumps in Git.
- Python package, reproducible CLI, tests, CI and architecture notes.
- Exact monthly budget arithmetic and labeled straight-line distance calculations.

## 2. Evidence-first source discovery
Three independent scouts investigate six candidate websites beyond Rukita.
A source passes discovery only when actual listing/detail data or public result scrolling is observed. A landing page or sitemap alone does not pass.
Record actual URLs, access method, sample listing evidence, robots/terms observations, available fields and blockers. Parent independently verifies the scout reports.
Technical accessibility does not grant scraping permission. Blocked or restricted sources remain documented but are not automatically collected.

## 3. Collection and geospatial enrichment
- Implement a connector only after its source is verified and policy checked.
- Keep source URLs, observed timestamps, original price periods and extraction evidence.
- Reject fabricated prices and exact coordinates. Unknown vacancy, bills or location stay unknown.
- Deduplicate without merging distinct rooms in one building.
- Compare only explicit monthly rents to the chosen cap; annual upfront rents are not monthly offers.
- Distinguish published property coordinates, address geocodes and area-level estimates.
- Do not label straight-line distances as walking/driving routes.

## 4. TypeSafe Jev classification
- Endpoint: `https://opencode.ai/zen/v1/systemone`.
- Free model: `jev-1.13-free`; no automatic paid fallback.
- Questions are narrow typed judgments: availability, included electricity, bathroom arrangement and source inconsistencies.
- Budget/radius buckets are computed in Python. The model does not calculate currency, distance, date differences or totals.
- Strict response validation, explicit unknown options, confidence-based review and retained evidence.
- Evaluate on actual newly collected listings; publish mistakes and review rates, not only successes.

## 5. Portfolio-quality release
- A runnable real-data example, clearly scoped source coverage and freshness.
- Architecture, limitations, data-use policy and reproducible tests.
- Read back the remote commit and CI result before claiming success.

Rukita is already researched. Rebuilding a Rukita-only classifier is deliberately not the next research task.
