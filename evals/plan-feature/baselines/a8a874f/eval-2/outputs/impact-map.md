# Impact Map: TC-9002 — Improve Search Experience

## Feature Summary

Improve the platform's search functionality to be faster and return more relevant results, and add filtering capabilities to the search endpoint.

## Workflow Mode

**direct-to-main** — Single repository, scoped backend changes, no cross-repo coordination needed.

## Ambiguities Identified

The feature description (TC-9002) is underspecified in several critical areas. The following ambiguities were identified and must be resolved with the product owner. Until then, assumptions are documented inline in each task.

| # | Ambiguity | What is unclear | Assumption pending clarification |
|---|---|---|---|
| 1 | **Performance target** | "Search should be faster" and "should be fast enough" provide no measurable target. No current baseline latency is given, no target latency or percentile (p50, p95, p99) is defined. | Assume target is p95 < 200ms for typical queries. Add database indexes and optimize the query path. Revisit after profiling. |
| 2 | **Relevance ranking criteria** | "Results should be more relevant" has no definition of relevance. It is unclear whether relevance means text-match scoring, recency weighting, severity-based boosting, or a combination. No user research or examples of "irrelevant" results are provided. | Assume PostgreSQL full-text search ranking (`ts_rank`) is sufficient for MVP. Weight title/name matches higher than description matches. |
| 3 | **Filter fields and types** | "Add filters — some kind of filtering capability" does not specify which entity fields should be filterable, what filter operators are needed (exact match, range, contains, multi-select), or whether filters combine with AND or OR semantics. | Assume filters for entity type (SBOM, advisory, package), severity (for advisories), and date range (created/modified). Use AND semantics between different filter fields. Reuse the existing query builder pattern from `common/src/db/query.rs`. |
| 4 | **Search scope** | It is unclear whether "search" means the unified search endpoint (`/api/v2/search`) only, or also the per-entity list endpoints (`/api/v2/sbom`, `/api/v2/advisory`, `/api/v2/package`). | Assume the primary target is the unified search endpoint in `modules/search/`. Per-entity list endpoints are not in scope for this feature. |
| 5 | **"Better UI" requirement** | Marked as non-MVP. No design mockups, wireframes, or frontend repository are available. | **Excluded from scope entirely.** Cannot be planned without design assets and a frontend repository. This requirement should be revisited as a separate feature once designs are available. |

## Scope

### In Scope (MVP)

1. **Search performance optimization** — Database indexing and query optimization for the search module
2. **Search relevance improvement** — Full-text search ranking with weighted fields
3. **Search filtering** — Add filter parameters to the search endpoint (entity type, severity, date range)
4. **Search integration tests** — Update and expand the existing search test suite

### Out of Scope

- **Better UI** — No frontend repository or design mockups available; cannot be planned (non-MVP requirement)
- **Per-entity list endpoint changes** — Assumed out of scope per Ambiguity #4
- **Ingestion pipeline changes** — Search improvements target the read path only

## Task Breakdown

| Task | Summary | Repository | Dependencies |
|---|---|---|---|
| Task 1 | Add database migration for full-text search indexes | trustify-backend | None |
| Task 2 | Implement search relevance ranking in SearchService | trustify-backend | Task 1 |
| Task 3 | Add filter parameters to the search endpoint | trustify-backend | Task 1 |
| Task 4 | Add integration tests for search improvements | trustify-backend | Tasks 2, 3 |

## Repositories Affected

- **trustify-backend** — All tasks target this repository
