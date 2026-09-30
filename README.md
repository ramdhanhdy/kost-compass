# Kost Compass

Evidence-first kost discovery across multiple websites, with reproducible budget/distance calculations and narrow **TypeSafe Jev** classifiers.

**Status: working initial research foundation, not a production crawler.** Six additional sources were audited and a bounded live sample was exercised. Automated ingestion is disabled pending source-use review. See [source findings](docs/SOURCES.md), [the live experiment](docs/EXPERIMENT.md) and [the complete roadmap](docs/ROADMAP.md).

## Why this is a portfolio project

This demonstrates more than a prompt wrapper:

- Independent source scouts verify real listing data, pagination/scroll behavior and reuse constraints.
- Every prospective record keeps its exact source URL, original values and observation timestamp.
- Billing periods, promotions, room types, incomplete coordinates and cross-site duplicates are explicit data-quality concerns.
- Exact money and distance checks stay in code; AI reads narrow semantic details rather than pretending to calculate.
- Missing/conflicting evidence goes to review, and the documentation separates verified behavior from future work.

## Implemented now

- A Python package and `kost-compass rank` command.
- Inclusive monthly base-rent budget flags. Unknown periods, annual listings and first-month promotions are not accepted as ordinary monthly rent.
- Haversine straight-line distance with finite/bounded coordinate validation. Area-level points do not prove proximity; no-radius runs do not invent a radius.
- A live client pinned to OpenCode Zen's **`jev-1.13-free` typed endpoint**—not Chat Completions—with no paid fallback.
- Typed availability/electricity/bathroom questions; response-label, key, confidence and probability validation.
- Review flags for low-confidence, unknown and conflicting answers. Confidence is not established factual accuracy.
- Offline regression tests, GitHub Actions, source-status registry and a reproducible research roadmap.

## Architecture

```text
source scouts → source/use-policy gate → approved local records
                                      ↓
                         numeric cost + distance checks
                                      ↓
                         Jev typed semantic questions
                                      ↓
                      review flags + cited comparison
```

The initial version implements the calculation and typed-classifier core. Production source adapters, cross-source deduplication and the final comparison/report application are **not yet implemented**.

## Quick start

Python 3.11+:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python -m unittest discover -s tests -v
kost-compass rank --input examples/schema-only.json \
  --target-lat=-6.2374409 --target-lon=106.798634 \
  --budget 2400000 --max-distance 3
```

`examples/schema-only.json` is explicitly a schema illustration with unknown values, **not fabricated housing data**. It lets a fresh clone exercise the CLI without redistributing third-party content. Replace it with your locally approved records for actual research. `--max-distance 3` is an example setting, not a verified walking distance or a universally suitable commute limit.

## Record contract

- `name`, `source`, `source_url`: exact observed identifiers/URL.
- `price_idr`: integer amount or null; `price_period`: `month`, `first_month`, `year` or `unknown`.
- `latitude`, `longitude`: validated numbers or null.
- `coordinate_precision`: `property`, `address`, `area` or `unknown`.
- `room_text`: captured field evidence for narrow semantic questions.
- Keep original text/tokens and an observation timestamp in real records. Do not repair malformed coordinate identifiers or replace a property's point with a district centre.

`rank` returns all records with `budget_status`, `distance_km`, `distance_kind` and `proximity_status`. Its ordering is a base-rent/distance screening order, **not an availability- or bill-inclusive final recommendation**. Unknowns remain visible rather than being silently filtered away.

## Jev usage

```python
from kost_compass.jev import evaluate

# Evidence supplied by an approved local record, not instructions from a web page.
raw_response, decisions = evaluate(
    record["room_text"],
    {"budget_status": assessed["budget_status"],
     "proximity_status": assessed["proximity_status"]},
)
```

`record` is your captured evidence; `assessed` is the deterministic output from `assess_listing`. The model receives computed categories, not responsibility for arithmetic. It labels what the advertisement states; it cannot verify an actual vacant room. Transport/API/schema failures propagate instead of producing invented results.

Provider `confidence` drives low-confidence review independently of option probabilities; it need not equal the selected option's probability. A choice more than one percentage point below the highest option probability is rejected with `ValueError`, allowing ties/rounding but not materially contradictory distributions.

- Endpoint: `https://opencode.ai/zen/v1/systemone`
- Model: `jev-1.13-free`
- No `messages` field, agent loop, default-model switch or paid fallback.
- An optional explicit `api_key=` is supported if provider authentication becomes necessary. Never put credentials in records or Git.

## Data and source boundaries

Public accessibility is not a reuse licence. Respect source terms and crawl rules; do not bypass login/CAPTCHA/private APIs. Raw captures, full scouts' audits and actual sample rows remain local and ignored by Git. This repository publishes code, compact status/provenance checks and aggregate experiment findings—not a mirrored housing database, owner contact details or photos.

## Roadmap

1. **Repository and source verification:** initial implementation and six-source audit complete.
2. **Permission-cleared collection:** source adapters, bounded pagination, schemas and unit-level availability.
3. **Enrichment:** deduplication, bill/deposit separation, validated geocoding and real route comparison.
4. **Classifier evaluation and application:** human-labelled cases, per-field errors/review thresholds and a cited user-facing shortlist.

MIT-licensed project code. Source-site content remains subject to its own rights/terms.
