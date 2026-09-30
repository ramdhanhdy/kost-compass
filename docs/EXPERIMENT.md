# Bounded live experiment

## What was actually run

- Three source scouts audited **six additional domains** beyond the existing Rukita search.
- Eighteen sample listing/card records were audited locally. These are **not eighteen unique buildings** and are not a complete inventory.
- Parent checks re-fetched Infokost/SewaKost list/detail pages, corroborated Mamikos/Pinhome sample fields against saved detail captures, and checked Cove/Papikost cached evidence without new restricted retrieval.
- Six source-derived records from **Mamikos and Pinhome** were used in a local calculation/classification experiment. Raw records, descriptions and captures were not published.

## Deterministic calculation result

The sample destination was the public Telkom STO Kebayoran location. The budget check used **Rp2,400,000/month base rent**. A **3 km straight-line radius was an explicit demonstration setting**, not a user-confirmed maximum commute.

- Four records had explicit ordinary monthly rent at or below the cap.
- Two had first-month promotional prices, so ongoing-rent budget status remained unknown.
- Three Mamikos records had valid published property-map points and were within the demonstration radius by Haversine.
- Three Pinhome records had malformed coordinate tokens; tokens were preserved, distances remained null and proximity required review.
- No walking route/time, bill-inclusive affordability, physical room condition or actual booking availability was established by this experiment.

## Jev result

Pinned request model: `jev-1.13-free`.
Endpoint: `https://opencode.ai/zen/v1/systemone`.

- Six final listing requests produced **18 typed semantic answers**: advertised availability, electricity inclusion and bathroom type.
- All six final responses passed the application's response-schema validation.
- **Five answers required review** because the relevant field was unknown. A confident “unknown” still requires review; a probability is not a verified housing fact.
- The six final responses each reported cost `"0"`; their reported total was `0`.
- Three earlier exploratory requests also reported `"0"`. They tested a more conservative coordinate-quality flag; no numeric token was repaired. The final batch used the correct published-property enum.
- No API key was needed in these calls. Authentication requirements and free availability may change; this is not a permanent provider guarantee.
- There was **no paid-model fallback**, no changes to Hermes' default model and no OpenCode CLI installation.

This is a **live integration smoke test**, not an accuracy benchmark. The inputs were short captured field summaries, not complete scraped page bodies. No held-out gold set, calibrated error rates or model-vs-rule superiority was established. Research-agent costs are not covered by the Jev endpoint's reported cost.

## What remains

Permission-cleared source adapters, broader collection, room/building deduplication, verified geocoding/routes, human-labelled evaluation and a user-facing report/interface remain on the [roadmap](ROADMAP.md). The repository does not claim to be a deployed production crawler or an automated housing decision-maker.
