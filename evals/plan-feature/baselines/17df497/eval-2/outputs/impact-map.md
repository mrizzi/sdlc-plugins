# Repository Impact Map — TC-9002: Improve Search Experience

## Ambiguity Analysis

The feature description for TC-9002 is vague in several areas. The following assumptions
and clarifications were derived from repository analysis and reasonable inference:

- **"Search should be faster"**: Interpreted as adding database-level full-text search
  indexes (PostgreSQL `tsvector`/GIN indexes) to replace or augment the current query-based
  search approach in the `SearchService`. The current `modules/search/` module performs
  full-text search across entities but lacks explicit indexing infrastructure.
- **"Results should be more relevant"**: Interpreted as implementing PostgreSQL full-text
  search ranking (`ts_rank`) to order results by relevance score rather than returning
  unranked or arbitrarily ordered results.
- **"Add filters"**: Interpreted as extending the search endpoint (`GET /api/v2/search`)
  to accept filter parameters for entity type, date range, and severity (for advisories).
  The existing `common/src/db/query.rs` provides shared filtering and pagination helpers
  that should be reused.
- **"Should be fast enough"** (non-functional): Interpreted as a requirement to ensure
  search queries complete within acceptable response times, validated by integration tests
  with performance assertions or at minimum by ensuring indexed queries are used.

---

## Impact Map

```
trustify-backend:
  changes:
    - Add PostgreSQL full-text search indexes (GIN) on searchable entity columns via new database migration
    - Refactor SearchService to use PostgreSQL tsvector/tsquery full-text search with ts_rank relevance scoring
    - Add filter parameters (entity type, date range, severity) to GET /api/v2/search endpoint
    - Extend search endpoint response to include relevance score and total count metadata
    - Update integration tests for search endpoint covering filters, relevance ordering, and performance
```
