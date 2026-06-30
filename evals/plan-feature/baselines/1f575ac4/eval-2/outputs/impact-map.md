# Repository Impact Map — TC-9002: Improve Search Experience

## Workflow Mode: `direct-to-main`

**Rationale:** No atomicity indicators identified. All changes are within a single repository (trustify-backend) and can be delivered incrementally. The search performance improvements, relevance tuning, and filtering capability are independently deployable — merging any single task does not leave `main` in a broken state without the others.

## trustify-backend

### Changes

1. **Add database indexes for search-critical columns** — Add indexes on frequently searched text columns in SBOM, advisory, and package entities to improve full-text search query performance.

2. **Optimize SearchService full-text search queries** — Refactor `modules/search/src/service/mod.rs` to use PostgreSQL full-text search features (tsvector/tsquery) instead of naive LIKE queries, improving both speed and relevance ranking.

3. **Add search result relevance scoring** — Implement `ts_rank` or `ts_rank_cd`-based relevance scoring in `SearchService` so results are ordered by relevance rather than insertion order.

4. **Add filtering parameters to search endpoint** — Extend `GET /api/v2/search` to accept query parameters for filtering by entity type (sbom, advisory, package), date range, and severity, using the shared query builder helpers in `common/src/db/query.rs`.

5. **Add integration tests for improved search** — Add comprehensive integration tests in `tests/api/search.rs` covering performance expectations, relevance ordering, and filter parameter combinations.

## Ambiguities Identified in Feature TC-9002

The feature description contains several ambiguities that were resolved with conservative, concrete assumptions:

| Ambiguity | Resolution |
|---|---|
| "Search should be faster" — no target latency specified | Focus on database-level optimization (indexes + full-text search) which provides measurable improvement. Specific latency targets should be defined by the team. |
| "Results should be more relevant" — no relevance criteria defined | Implement PostgreSQL full-text search ranking (ts_rank) as a standard relevance mechanism. |
| "Add filters" — "some kind of filtering capability" is unspecified | Add filters for entity type, date range, and severity — these are the natural filterable dimensions present in the existing data model. |
| "Better UI" — marked non-MVP | Excluded from this plan per the feature's own MVP classification. Backend-only changes. |
| "Should be fast enough" — no performance threshold | No specific SLA can be enforced without a target. Tests will verify that search returns results and that indexes are used. |
| "Don't break existing functionality" — vague NFR | Ensure backward compatibility by keeping the existing search endpoint contract intact (new filter parameters are optional). |
