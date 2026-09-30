# Source reconnaissance

Three independent scouts checked six additional websites on **30 September 2026**. They checked actual listing pages, pagination or scrolling, structured data, crawl directives and reuse terms—not just homepages or search-engine snippets.

**Technical access is not permission to automate or republish. All unattended ingestion is disabled in this initial version.** Full captures and source-derived sample rows remain local; this repository publishes code, a compact source registry and methodological findings, not a copied housing database.

## Mamikos
- [Verified Kebayoran Baru results](https://mamikos.com/kost/kost-kebayoran-baru-jakarta-murah)
- Actual room records were present in public Vue state and card attributes. In the tested browser, results remained visually skeletal, so this is **data hydration verified**, not a claim that every result card rendered correctly.
- Scrolling and a page 1 → page 2 transition were verified; record titles and displayed result range changed.
- Public room details provided prices, availability labels and property map points.
- Separate first-month promotions from recurring rent; separate room types from buildings.
- Terms route was blocked by a security checkpoint. Scheduled collection and public data redistribution remain unapproved.

## Pinhome
- [Verified Kebayoran Baru kost catalogue](https://www.pinhome.id/kost/kec-kebayoran-baru-1274)
- Visible rental cards, public detail links, pagination and scrolling were verified. Do not confuse this route with kost-building sales.
- Monthly and annual offerings coexist; minimum commitments and advertised availability require separate fields.
- The three sampled room pages had malformed JSON-LD coordinate tokens. Original tokens were preserved; no silently repaired points or advertisement-based distance guesses enter the ranking.
- Terms describe limited personal/noncommercial information use and protected intellectual property. Public mirroring or ongoing aggregation needs review/permission.

## Infokost
- [Verified South Jakarta results](https://infokost.id/kost/jakarta-selatan)
- Public server-rendered lists and room details were extractable. Parent verification re-fetched the list and one sample detail with successful HTTP responses.
- Observed anchors include related/recommended rooms; link counts are not primary-result counts or a verified full inventory total.
- Sampled properties overlap the existing Rukita inventory. Cross-domain duplication must not inflate the housing count.
- Crawl directives permit the inspected paths but do not establish data-reuse rights; no ongoing collector is enabled.

## SewaKost
- [Verified South Jakarta results](https://www.sewakost.com/kost/jakarta/jakarta-selatan/)
- Independent-owner listings, direct public details and server-rendered pagination were verified. Parent verification re-fetched the list and one sample detail.
- The published 10-second crawl delay was respected during parent verification. Restricted sort/print/private routes were not used.
- Some price fields omit the billing period and a sample map point was outside the advertised Jakarta area. These are review cases, not inputs to optimistic budget or travel claims.
- Dedicated reuse terms were not located; scheduled collection/republication remain unresolved.

## Papikost
- [Public website](https://papikost.com/)
- Actual priced rental cards were observed, but the tested Jakarta search route had zero results. Do not describe a generic SEO page as a working Jakarta adapter.
- [Terms](https://papikost.com/syarat-ketentuan) restrict manual/automated monitoring and copying without written authorization.
- Further retrieval was stopped after the restriction was identified. **No automatic ingestion.**

## Cove
- [Public website](https://cove.id/)
- A public directory contained real room-detail links; sampled public detail payloads included monthly-price rows, coordinates and availability.
- A browser scroll attempt did not change position; successful scrolling or infinite loading was **not** verified. The directory/details are the data evidence.
- [Terms](https://cove.id/terms-conditions) restrict copying and redistribution; request permission or a licensed feed before an ongoing adapter/public dataset.
- **No automatic ingestion.**

## Next source gate

1. Confirm permitted collection/use for each enabled adapter.
2. Collect bounded batches with exact source URLs, timestamps and billing-period evidence.
3. Deduplicate buildings **and** room types; keep source links.
4. Calculate straight-line distance only from valid property/address points; keep area proxies and malformed coordinates out of hard proximity decisions.
5. Apply Jev to narrow semantic questions after numeric checks, with review on missing/conflicting evidence.

Machine-readable status: [`source-registry.json`](../research/sources/source-registry.json).
