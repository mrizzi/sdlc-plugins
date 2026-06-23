# Repository Impact Map — TC-9002: Improve search experience

## Ambiguities and Assumptions

The feature description TC-9002 contains several ambiguities that must be resolved before implementation can proceed with full confidence. The following assumptions have been made to produce a viable plan; they should be validated with the product owner.

### Flagged Ambiguities

1. **"Search should be faster"** — No performance baseline or target metrics are defined. What is "too slow"? What response time is acceptable? **Assumption:** Optimize the existing search query path with database indexing and query restructuring. Measure improvement relative to current performance but no specific SLA is defined.

2. **"Results should be more relevant"** — No definition of relevance is provided. Relevance could mean full-text search ranking, recency weighting, field-specific boosting, or typo tolerance. **Assumption:** Implement PostgreSQL full-text search with `tsvector`/`tsquery` to replace naive `LIKE`/`ILIKE` matching, which will provide built-in ranking via `ts_rank`.

3. **"Add filters"** — No specification of which filters, which entities are filterable, or what filter UI is expected. **Assumption:** Add server-side filtering parameters to the search endpoint for common entity attributes (entity type, severity for advisories, date ranges). Leverage the existing `query.rs` filter builder pattern.

4. **"Better UI"** — **Excluded from scope.** The target repository is a backend service (trustify-backend). No frontend repository is in the Repository Registry. UI improvements cannot be planned without a frontend repo and design mockups.

5. **"Should be fast enough"** — Vague non-functional requirement with no measurable threshold. **Assumption:** Performance improvements from indexing and query optimization will be validated via integration tests that assert query completion within reasonable bounds, but no specific latency SLA is imposed.

6. **"Don't break existing functionality"** — Standard backward compatibility constraint. **Assumption:** Existing search API contract (`GET /api/v2/search`) will be preserved; new filter parameters will be additive (optional query params).

### Excluded from Scope

- **"Better UI"** requirement — no frontend repository available, no design mockups provided
- Any client-side search behavior changes — backend-only scope

---

## Impact Map

```
trustify-backend:
  changes:
    - Add database migration to create GIN indexes on tsvector columns for full-text search on SBOMs, advisories, and packages
    - Refactor SearchService to use PostgreSQL full-text search (tsvector/tsquery) with ts_rank for relevance ranking
    - Add filtering parameters to GET /api/v2/search endpoint (entity type, severity, date range)
    - Update search endpoint handler to accept and apply filter query parameters using existing query builder helpers
    - Add integration tests for full-text search relevance ranking and filter combinations
    - Update README.md to document new search filter parameters and full-text search behavior
```

---

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. Each task can be merged independently without leaving `main` in a broken state:
- The database migration adds indexes — this is additive and does not break existing queries
- The SearchService refactor improves query execution but maintains the same API contract
- Filter parameters are additive (optional query params) and do not break existing callers
- Tests and documentation are independently mergeable

No coordinated schema migrations, breaking API changes, cross-cutting refactors, or tightly coupled components were identified.
