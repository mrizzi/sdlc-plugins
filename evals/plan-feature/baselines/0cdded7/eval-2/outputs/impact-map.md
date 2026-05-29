# Repository Impact Map — TC-9002: Improve Search Experience

## Ambiguities Identified

The feature description contains several ambiguities that were resolved with reasonable defaults during planning. These should be confirmed with stakeholders:

1. **"Search should be faster"** — No performance target specified. Resolved: add database indexing for full-text search columns and implement query result caching via tower-http middleware. Target: p95 latency under 200ms for typical queries.
2. **"Results should be more relevant"** — No relevance criteria defined. Resolved: implement weighted full-text search ranking (title matches weighted higher than description matches) and support multi-entity search with per-entity relevance scoring.
3. **"Add filters"** — No filter types specified. Resolved: add filtering by entity type (SBOM, advisory, package), severity (for advisories), and date range. These align with existing entity model fields.
4. **"Should be fast enough"** — No latency SLA. Resolved: use the 200ms p95 target above; add database indexes to support filter queries without sequential scans.

## Impact Map

```
trustify-backend:
  changes:
    - Add full-text search indexes on searchable columns in SBOM, advisory, and package entities (database migration)
    - Extend SearchService to support weighted ranking and multi-entity relevance scoring
    - Add filter parameters (entity type, severity, date range) to the search endpoint query interface
    - Extend GET /api/v2/search to accept filter query parameters and return ranked results
    - Add caching layer for search results using tower-http cache middleware
    - Update search integration tests to cover filtering, ranking, and performance expectations
```

## Workflow Mode

**Selected mode: `direct-to-main`**

**Rationale:** No atomicity indicators are present. Each change can be delivered incrementally without leaving `main` in a broken state:
- The migration adds indexes which are additive and non-breaking
- Filter parameters are additive (existing queries without filters continue to work)
- Relevance ranking improves existing results without breaking the response shape
- Caching is transparent middleware that does not change the API contract
- No cross-repository dependencies exist (single repository)

All tasks target the `trustify-backend` repository and changes are backward-compatible, so each PR can be merged independently.
