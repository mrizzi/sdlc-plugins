# Impact Map: TC-9002 — Improve Search Experience

## Feature Summary

Enhance the search functionality in trustify-backend to improve performance (faster queries), relevance (ranked results), and usability (filtering). The feature scope covers backend search infrastructure only.

## Ambiguities Identified

The feature description contains several vague or underspecified requirements that require clarification before implementation can be fully scoped. The following ambiguities have been identified:

1. **"Search should be faster" / "Currently too slow"** — No baseline performance metrics are provided (current p95 latency, query volume) and no target performance thresholds are defined (e.g., "search should return results in under 200ms"). **Assumption pending clarification:** We assume adding PostgreSQL GIN indexes on key text columns and using full-text search primitives (tsvector/tsquery) will provide adequate improvement. Performance benchmarks should be established before and after implementation.

2. **"Results should be more relevant"** — No definition of relevance criteria, no ranking algorithm preference, and no examples of "irrelevant" results to diagnose the root cause. **Assumption pending clarification:** We assume PostgreSQL ts_rank-based ordering using tsvector/tsquery will improve relevance. The ranking weights across entity types (SBOM, advisory, package) are unspecified; we assume equal weighting initially.

3. **"Add filters" / "Some kind of filtering capability"** — No specification of which fields should be filterable, what filter types to support (exact match, range, multi-select, free-text), or how filters combine (AND vs OR). **Assumption pending clarification:** We assume filters for entity type, severity (advisories), and date range, using AND combination semantics, leveraging existing query helpers in `common/src/db/query.rs`.

4. **"Should be fast enough"** — Non-functional requirement with no quantitative target. No SLA, no p95/p99 latency budget, no concurrent-user target. **Assumption pending clarification:** We assume the existing PostgreSQL infrastructure is sufficient and that index-based optimization meets the implicit performance expectation.

5. **"Better UI" (Non-MVP)** — This requirement is explicitly marked as non-MVP. Additionally, no frontend repository is available in the project configuration, no design mockups or wireframes are provided, and no UI specifications exist. **This requirement is excluded from the implementation plan.** It cannot be planned without a frontend repository and design artifacts.

## Scope

### In Scope (MVP)
- Database migration to add full-text search indexes
- Enhanced SearchService with PostgreSQL full-text search ranking (tsvector/tsquery)
- Filter query parameters on the search endpoint (entity type, severity, date range)
- Integration tests for all new search functionality

### Out of Scope
- "Better UI" — non-MVP, no frontend repo or design mockups available
- Frontend changes of any kind (no frontend repository configured)
- Changes to ingestor or ingestion pipelines
- Cross-service search (scope limited to existing SearchService)

## Architecture

### Affected Components
- `migration/` — New migration for GIN indexes on searchable columns
- `modules/search/src/service/mod.rs` — SearchService enhanced with tsvector/tsquery ranking
- `modules/search/src/endpoints/mod.rs` — Search endpoint extended with filter parameters
- `common/src/db/query.rs` — Potential extension for full-text search query helpers
- `tests/api/search.rs` — Integration tests for new search functionality

### Data Flow
```
Client request (with optional filters)
  -> GET /api/v2/search?q=...&type=...&severity=...&from=...&to=...
  -> Search endpoint (parse filter params)
  -> SearchService (build tsvector/tsquery, apply filters, rank results)
  -> PostgreSQL (GIN index-accelerated full-text search)
  -> PaginatedResults<SearchResult> (ordered by ts_rank)
```

## Task Breakdown

| # | Task | Repository | Dependencies |
|---|------|-----------|--------------|
| 1 | Add database migration for full-text search indexes | trustify-backend | None |
| 2 | Enhance SearchService with full-text search ranking | trustify-backend | Task 1 |
| 3 | Add filter query parameters to search endpoint | trustify-backend | Task 2 |
| 4 | Add integration tests for enhanced search | trustify-backend | Task 3 |

## Workflow Mode

direct-to-main — single repository, no atomicity constraints. All tasks target `main` branch.

## Propagated Fields

- **Priority:** Normal (propagated from TC-9002 to all tasks)
- **Fix Versions:** RHTPA 1.6.0 (propagated from TC-9002 to all tasks)
