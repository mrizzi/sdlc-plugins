# Impact Map — TC-9002: Improve search experience

## Scope Decision

**"Better UI" (Non-MVP)** is explicitly excluded from this plan. This requirement cannot be planned without design mockups, a frontend repository, and UX specifications. No frontend repository is in scope.

## Ambiguities Identified

1. **AMBIGUITY: "Search should be faster" — no performance baseline or target defined.** The feature says search is "currently too slow" and should be "fast enough," but provides no latency measurements, SLA targets, or percentile goals (e.g., p95 < 200ms). **ASSUMPTION pending clarification**: We will target improving query performance by adding database indexes on commonly searched columns and optimizing the existing query logic in `SearchService`. Success will be measured by observable improvement in response times, but a specific SLA should be agreed upon with stakeholders.

2. **AMBIGUITY: "Results should be more relevant" — no definition of relevance.** The feature does not specify what "relevant" means — whether it involves ranking by recency, severity, match quality, or some domain-specific scoring. **ASSUMPTION pending clarification**: We will implement PostgreSQL full-text search ranking (ts_rank) to order results by text match quality, and allow sorting by additional fields (e.g., severity for advisories, date for SBOMs). Stakeholders should validate that this matches their expectation of "relevance."

3. **AMBIGUITY: "Add filters — some kind of filtering capability" — no filter fields specified.** The feature does not define which fields should be filterable, what filter operators are needed (exact match, range, multi-select), or which entity types need filters on the search endpoint. **ASSUMPTION pending clarification**: We will add filters for entity type (SBOM, advisory, package), severity (for advisories), and date range. These represent the most common filtering dimensions based on the existing data model. Additional filters should be specified by product.

4. **AMBIGUITY: "Don't break existing functionality" — no regression test baseline.** Non-functional requirements state not to break existing functionality, but there is no specification of what constitutes "existing functionality" beyond the current search endpoint. **ASSUMPTION pending clarification**: We will preserve backward compatibility of the `GET /api/v2/search` endpoint — existing query parameters will continue to work, and new parameters (filters, sort) will be additive.

5. **AMBIGUITY: Scope of "search" is undefined.** It is unclear whether "search" refers only to the dedicated `GET /api/v2/search` endpoint or also includes the list endpoints (`GET /api/v2/sbom`, `GET /api/v2/advisory`, `GET /api/v2/package`) which also support query-based filtering. **ASSUMPTION pending clarification**: The primary focus is the `GET /api/v2/search` endpoint in `modules/search/`, but shared query improvements in `common/src/db/query.rs` will benefit all list endpoints.

## Impact

trustify-backend:
  changes:
    - Add database migration for full-text search indexes (GIN indexes on searchable text columns in sbom, advisory, and package tables) — new migration directory under `migration/src/`
    - Enhance `modules/search/src/service/mod.rs` (SearchService) to use PostgreSQL full-text search with ts_rank ranking for relevance-based ordering
    - Add filter parameters (entity type, severity, date range) to `modules/search/src/endpoints/mod.rs` search endpoint
    - Extend `common/src/db/query.rs` with shared filter/sort helpers that support the new filter types
    - Update `modules/search/src/endpoints/mod.rs` to accept and validate new query parameters for filtering and sorting
    - Add integration tests in `tests/api/search.rs` covering: filtered search, relevance ranking, performance with indexes, backward compatibility of existing search queries
    - Update entity definitions if needed to support full-text search vector columns (`entity/src/sbom.rs`, `entity/src/advisory.rs`, `entity/src/package.rs`)
