# Repository Impact Map — TC-9002: Improve Search Experience

## trustify-backend

### Changes

- Add database indexes on commonly searched columns (SBOM name, advisory title/severity, package name/license) to improve full-text search query performance
- Refactor `SearchService` in `modules/search/src/service/mod.rs` to implement relevance-based ranking (e.g., weighted scoring across entity fields) instead of returning unranked results
- Add filtering parameters (entity type, severity, date range, license) to the search endpoint `GET /api/v2/search` in `modules/search/src/endpoints/mod.rs`
- Extend `common/src/db/query.rs` with shared filter-parsing helpers for the new search filter parameters, reusing the existing filtering and pagination infrastructure
- Add a database migration to create full-text search indexes (e.g., PostgreSQL `tsvector`/GIN indexes) on searchable entity columns
- Add integration tests for the new search filters, relevance ranking, and performance expectations in `tests/api/search.rs`
- Update the `PaginatedResults` response wrapper or the search response type to include relevance score metadata alongside search results
