# Repository Impact Map — TC-9002: Improve Search Experience

## Ambiguity Notes

The feature description contains several ambiguous requirements that were interpreted
as follows for planning purposes. These interpretations should be validated with the
product owner before implementation begins.

| Requirement | Ambiguity | Planning Interpretation |
|---|---|---|
| "Search should be faster" | No latency target specified | Add database indexing for full-text search columns and optimize query execution in SearchService |
| "Results should be more relevant" | No definition of relevance | Implement weighted full-text search ranking using PostgreSQL `ts_rank` with field-level weighting (e.g., title > description) |
| "Add filters" | "Some kind of filtering capability" — no specific filters listed | Add filters for entity type, date range, and severity/license based on existing entity fields |
| "Should be fast enough" (NFR) | No quantifiable performance target | Target sub-500ms p95 response time for typical search queries; add query performance logging to enable measurement |

---

## Impact Map

```
trustify-backend:
  changes:
    - Add full-text search indexes (GIN) on searchable columns in SBOM, Advisory, and Package entities via a new database migration
    - Refactor SearchService to use PostgreSQL full-text search with ts_rank weighted ranking instead of basic pattern matching
    - Add filtering parameters (entity type, date range, severity, license) to the search endpoint query interface
    - Extend the GET /api/v2/search endpoint to accept filter query parameters and return relevance-scored results
    - Add query performance logging to SearchService for latency measurement
    - Update common/src/db/query.rs with shared full-text search query builder helpers
    - Add and update integration tests for search performance, relevance ranking, and filtering
```
