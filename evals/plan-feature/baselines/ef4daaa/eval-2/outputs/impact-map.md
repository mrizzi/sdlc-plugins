# Repository Impact Map — TC-9002: Improve Search Experience

## Ambiguities Identified

The feature description TC-9002 contains several ambiguities that were resolved with reasonable defaults for planning purposes. These should be confirmed with the product owner before implementation begins:

1. **"Search should be faster"** — No specific latency targets provided. No baseline measurements referenced. Resolved by planning database-level indexing and query optimization as the most likely bottleneck in a PostgreSQL-backed full-text search.

2. **"Results should be more relevant"** — No definition of "relevant" or ranking criteria. Resolved by planning PostgreSQL full-text search ranking improvements (ts_rank, ts_rank_cd) and result ordering by relevance score, which is the standard approach for improving relevance in PostgreSQL-backed search.

3. **"Add filters"** — No specification of which filters, what entity types are filterable, or what filter UI/UX is expected. Resolved by planning filters for the most common searchable entity attributes: entity type (SBOM, advisory, package), severity (for advisories), and date range. These align with the existing entity model fields visible in the repository structure.

4. **"Should be fast enough"** (NFR) — No quantitative performance target. This is not actionable without a specific SLA. Resolved by focusing on measurable improvements (indexing, query optimization) rather than targeting a specific latency number.

5. **Scope of "search"** — Unclear whether this refers only to the existing `GET /api/v2/search` endpoint or also to the individual entity list endpoints (`/api/v2/sbom`, `/api/v2/advisory`, `/api/v2/package`). Resolved by focusing on the dedicated search module (`modules/search/`) as the primary target, with shared query infrastructure in `common/` benefiting all list endpoints.

---

## Impact Map

```
trustify-backend:
  changes:
    - Add PostgreSQL full-text search indexes (GIN) on searchable entity columns via a new database migration
    - Enhance SearchService to use PostgreSQL ts_rank for relevance-based result ordering
    - Add filter parameters (entity type, severity, date range) to the search endpoint query interface
    - Update search endpoint to accept and validate filter query parameters
    - Extend shared query builder helpers to support full-text search filtering and ranking
    - Add integration tests for search performance improvements, relevance ordering, and filter combinations
```
