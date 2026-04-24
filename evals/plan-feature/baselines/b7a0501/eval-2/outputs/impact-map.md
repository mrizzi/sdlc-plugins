# Repository Impact Map — TC-9002: Improve Search Experience

## trustify-backend

### changes:
- Add database indexes on commonly searched columns (sbom name/version, advisory title/severity, package name/license) to improve full-text search query performance
- Add a new database migration for search-related indexes and a `tsvector` column for PostgreSQL full-text search
- Extend `SearchService` in `modules/search/src/service/mod.rs` to use PostgreSQL full-text search (`tsvector`/`tsquery`) for relevance-ranked results instead of naive pattern matching
- Add filter parameters (entity type, severity, date range, license) to the `GET /api/v2/search` endpoint in `modules/search/src/endpoints/mod.rs`
- Extend query builder helpers in `common/src/db/query.rs` to support full-text search ranking and new filter predicates
- Add search result ranking/scoring to `SearchService` so results are ordered by relevance
- Add integration tests for new search filters, full-text search ranking, and performance in `tests/api/search.rs`
- Add caching for search results using existing `tower-http` caching middleware configuration
