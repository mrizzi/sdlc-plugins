# Repository Impact Map — TC-9002: Improve Search Experience

## Ambiguity Analysis

The feature description for TC-9002 is notably vague across all requirements. The following
assumptions and clarifications were derived from repository analysis and reasonable inference:

- **"Search should be faster"**: The current `SearchService` in `modules/search/src/service/mod.rs`
  performs full-text search across entities but there is no evidence of database-level full-text
  search indexing infrastructure. Interpreted as adding PostgreSQL full-text search indexes
  (GIN indexes on `tsvector` columns) to the `sbom`, `advisory`, and `package` entity tables
  so that search queries hit indexed data rather than performing sequential scans.

- **"Results should be more relevant"**: Interpreted as implementing PostgreSQL full-text
  search ranking using `ts_rank` to order results by relevance score. The current search
  likely returns results in an arbitrary or insertion-time order. Ranked results will surface
  the most relevant matches first.

- **"Add filters"**: Interpreted as extending the `GET /api/v2/search` endpoint with optional
  query parameters for filtering by entity type (sbom, advisory, package), date range
  (created/modified date), and severity (for advisories). The existing shared query builder
  helpers in `common/src/db/query.rs` already provide filtering and pagination patterns that
  should be reused and extended.

- **"Should be fast enough"** (non-functional): Interpreted as ensuring indexed queries are
  used for search and validating via integration tests that search latency remains within
  acceptable bounds after the changes.

- **"Don't break existing functionality"** (non-functional): The search endpoint
  `GET /api/v2/search` must remain backward-compatible or, if the response shape changes,
  the change must be clearly documented. Existing callers should not break.

---

## Impact Map

```
trustify-backend:
  changes:
    - Add PostgreSQL full-text search indexes (GIN on tsvector columns) for sbom, advisory, and package tables via a new database migration
    - Refactor SearchService to use PostgreSQL tsvector/tsquery full-text search with ts_rank relevance scoring
    - Add filter parameters (entity_type, date_from, date_to, severity) to GET /api/v2/search endpoint
    - Define a SearchResultItem response model with entity_type, relevance_score, snippet, and metadata fields
    - Update and expand search integration tests to cover full-text search, filters, relevance ordering, and response format
```
