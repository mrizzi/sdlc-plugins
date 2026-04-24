# Repository Impact Map — TC-9002: Improve Search Experience

## Ambiguities Identified

The feature description TC-9002 contains several ambiguities that were resolved with reasonable defaults for planning purposes. In a real engagement, these would be clarified with the product owner before proceeding.

1. **"Search should be faster"** — No specific latency targets given. Interpreted as: add database indexing for full-text search columns and implement query-level caching to reduce repeated query overhead.
2. **"Results should be more relevant"** — No ranking criteria specified. Interpreted as: implement weighted full-text search scoring (e.g., PostgreSQL `ts_rank`) with boosting for title/name fields over description fields.
3. **"Add filters"** — No filter types specified. Interpreted as: add filtering by entity type (SBOM, advisory, package), severity (for advisories), and date range, since these are the primary domain dimensions visible in the existing entity models.
4. **"Should be fast enough"** — No NFR targets. Interpreted as: search queries should respond within 500ms at p95 under normal load; add response time logging to enable measurement.
5. **"Don't break existing functionality"** — Interpreted as: existing `GET /api/v2/search` endpoint contract must remain backward-compatible; new parameters are additive.

## Impact Map

```
trustify-backend:
  changes:
    - Add PostgreSQL full-text search indexes on searchable columns (sbom name, advisory title/description, package name)
    - Create a new database migration for full-text search indexes and tsvector columns
    - Extend SearchService to support weighted full-text ranking using ts_rank
    - Add filter parameters to the search endpoint (entity_type, severity, date_range)
    - Extend the shared query builder in common/src/db/query.rs to support full-text search filtering
    - Add query-result caching to the search endpoint using tower-http caching middleware
    - Update search endpoint to return relevance scores in results
    - Add integration tests for new search filters, ranking, and performance baseline
    - Update search endpoint to return paginated results with filter metadata
```
