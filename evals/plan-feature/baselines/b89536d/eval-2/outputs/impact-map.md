# Repository Impact Map — TC-9002: Improve Search Experience

## trustify-backend

changes:
  - Add PostgreSQL full-text search indexing (tsvector/GIN index) to searchable entities (sbom, advisory, package) to improve search performance
  - Implement search result ranking using ts_rank or ts_rank_cd in SearchService for relevance scoring
  - Add filter parameters (entity type, severity, date range, license) to the GET /api/v2/search endpoint
  - Extend common query builder helpers to support full-text search filtering and ranking
  - Add database migration for GIN indexes on searchable columns
  - Update integration tests in tests/api/search.rs to cover performance, relevance, and filtering

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. Each change is additive and backward-compatible:
- The GIN index migration can land independently (adding an index does not break existing queries).
- Search ranking is an enhancement to existing result ordering — existing consumers still receive valid results.
- Filter parameters are optional query parameters on an existing endpoint — omitting them preserves current behavior.
- No cross-repository dependencies exist (single backend repo).

All tasks target branch `main`.
