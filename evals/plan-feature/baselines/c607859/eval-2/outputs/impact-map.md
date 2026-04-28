# Repository Impact Map — TC-9002: Improve Search Experience

## Feature Ambiguity Notes

The feature description TC-9002 is underspecified in several areas. The following
assumptions were made to produce a concrete plan. These should be validated with
the product owner before implementation begins:

1. **"Search should be faster"** — Interpreted as: add database-level full-text search
   indexes and optimize the `SearchService` query path. The current implementation
   likely performs unindexed or naive text matching. Specific latency targets are
   not defined in the feature; a reasonable target would be sub-200ms p95 for
   typical queries.

2. **"Results should be more relevant"** — Interpreted as: implement ranked
   full-text search using PostgreSQL `ts_rank` / `ts_vector` capabilities rather
   than simple `LIKE`/`ILIKE` matching. The feature does not define a relevance
   metric; relevance will be measured by whether results matching more query terms
   rank higher.

3. **"Add filters"** — Interpreted as: add query-parameter-based filtering to the
   `GET /api/v2/search` endpoint, allowing users to filter by entity type
   (SBOM, advisory, package), severity (for advisories), and date range. The
   feature does not specify which filters; these were inferred from the existing
   entity model fields.

4. **"Better UI"** — Marked as non-MVP in the feature. Excluded from this plan
   (also: no frontend repository is in scope).

5. **Non-functional requirements** — "Should be fast enough" and "Don't break
   existing functionality" are not measurable as stated. Translated to: maintain
   backward compatibility on the existing `GET /api/v2/search` endpoint (no
   breaking changes to response shape), and add integration tests verifying
   performance characteristics.

---

## Impact Map

```
trustify-backend:
  changes:
    - Add PostgreSQL full-text search indexes via a new database migration for sbom, advisory, and package tables
    - Extend SearchService to use ts_vector/ts_rank for ranked full-text search instead of naive text matching
    - Add filter parameters (entity type, severity, date range) to the GET /api/v2/search endpoint
    - Extend the search endpoint request handling to parse and apply filter query parameters
    - Update PaginatedResults or search response to include relevance score metadata
    - Add integration tests for search relevance ranking, filtering, and performance
```
