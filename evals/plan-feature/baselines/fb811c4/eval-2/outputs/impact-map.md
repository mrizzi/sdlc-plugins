# Impact Map — TC-9002: Improve Search Experience

## Workflow Mode

Single-repo feature, no atomicity constraints. **Mode: direct-to-main.**

## Scope Exclusion

The "Better UI" requirement is marked non-MVP. No design mockups or specifications have been provided, and there is no frontend repository in scope. This requirement is **excluded from the plan** and should be addressed in a separate feature once designs are available.

## Repository Impact

```
trustify-backend:
  changes:
    - Add database indexes on commonly searched columns to improve query performance (migration/)
    - Optimize SearchService full-text search implementation with query caching and result ranking (modules/search/src/service/mod.rs)
    - Add filtering parameters (entity type, severity, date range) to the search endpoint (modules/search/src/endpoints/mod.rs)
    - Extend common query helpers with new filter types (common/src/db/query.rs)
    - Add integration tests for search performance, relevance, and new filters (tests/api/search.rs)
```

## Ambiguities Identified

1. **"Search should be faster" — no performance target defined.** The feature says search is "currently too slow" and should be "fast enough" but provides no concrete latency targets (e.g., p95 < 200ms, p99 < 500ms). **Clarification needed:** What are the acceptable response time thresholds? What is the current baseline? How many records are typical in customer deployments?

2. **"Results should be more relevant" — no relevance criteria specified.** The feature states users complain about "irrelevant results" but does not define what relevance means in this context. **Clarification needed:** Should results be ranked by recency, text match quality, severity, or a combination? Are there specific search scenarios (e.g., searching by CVE ID, package name, advisory title) that are broken today? Should exact matches rank higher than partial matches?

3. **"Add filters" — filter types and behavior are unspecified.** The requirement says "some kind of filtering capability" without enumerating which fields should be filterable, whether filters are AND/OR, or whether they apply pre- or post-search. **Clarification needed:** Which entity attributes should be filterable (e.g., severity, date range, entity type, license, package ecosystem)? Should filters be combinable? Should filtering happen server-side within the search query or as post-query refinement?

4. **"Don't break existing functionality" — no regression test baseline.** The non-functional requirement to preserve existing behavior implies backward compatibility but does not specify whether the search API contract (request/response schema) must remain identical or if additive changes are acceptable. **Clarification needed:** Is adding new optional query parameters considered a breaking change? Must the default (unfiltered, unranked) behavior produce identical results to today's implementation?

5. **Search scope is undefined.** The feature says "full-text search across entities" but does not clarify which entities (SBOMs, advisories, packages, or all three) are in scope for improvement, or whether cross-entity search should return unified or segregated results. **Clarification needed:** Should improvements apply uniformly to all searchable entities, or are specific entity types the priority?

## Tasks

| # | Slug | Summary | Dependencies |
|---|---|---|---|
| 1 | search-index-migration | Add database indexes for search performance | None |
| 2 | search-relevance-ranking | Implement relevance-based result ranking in SearchService | Task 1 |
| 3 | search-filters | Add filtering capabilities to the search endpoint | Task 1 |
| 4 | search-caching | Add query result caching for repeated searches | Task 2 |
| 5 | search-integration-tests | Comprehensive integration tests for search improvements | Tasks 2, 3, 4 |
