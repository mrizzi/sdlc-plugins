# Repository Impact Map -- TC-9002: Improve search experience

## Ambiguities and Assumptions

The feature description for TC-9002 is underspecified in several critical areas. The following ambiguities were identified, along with the assumptions made for planning purposes. These assumptions should be validated with the product owner before implementation begins.

### Ambiguities Flagged

1. **No performance targets for "faster" search.** The requirement states "search should be faster" and "currently too slow" but provides no quantitative baseline or target. No current latency measurements (p50, p95, p99) are given, and no target SLA is defined (e.g., "search must return results within 200ms at p95"). **Assumption:** We will add PostgreSQL full-text search indexing (GIN indexes) on searchable text columns and optimize the existing `SearchService` query path. Performance improvements will be measured via integration test timing but without a defined threshold.

2. **No definition of "more relevant" results.** The requirement states "results should be more relevant" but does not define relevance criteria, ranking factors, or provide examples of queries that currently return poor results. **Assumption:** We will implement PostgreSQL `ts_rank` scoring based on full-text search vectors and return results ordered by relevance score. This is a standard approach but may not match the product owner's unstated expectations.

3. **"Add filters" is completely undefined.** No specification of which fields should be filterable, what filter operators to support (exact match, range, contains), whether filters should be combinable (AND/OR), or what the API shape should be (query parameters vs. request body). **Assumption:** We will add filtering by entity type (SBOM, advisory, package) and by common fields: severity (for advisories), license (for packages), and date range. Filters will be implemented as query parameters following the existing pattern in `common/src/db/query.rs`.

4. **"Better UI" cannot be planned.** This requirement targets the user interface, but the target repository (`trustify-backend`) is a Rust backend service with no frontend code. Planning this requirement requires: (a) design mockups or Figma files specifying the desired UI, and (b) access to a frontend repository. **This requirement is deferred and cannot be included in this plan.**

5. **No specification of searchable entity scope.** The repository contains three entity types (SBOMs, advisories, packages) but the feature does not specify whether "search" means improving the existing cross-entity search endpoint (`GET /api/v2/search`), adding search within individual entity list endpoints, or both. **Assumption:** We will improve the existing cross-entity search endpoint and ensure individual list endpoints can leverage the same filtering infrastructure.

6. **"Should be fast enough" is not a measurable NFR.** No quantitative performance threshold is given. **Assumption:** We will ensure search queries use appropriate indexes and measure response times in integration tests. No specific latency SLA will be enforced without further input.

7. **"Don't break existing functionality" lacks specificity.** **Assumption:** All existing API endpoints must continue to return the same response shapes. New query parameters will be optional, and the existing search behavior without filters will be preserved.

### Out of Scope

- **"Better UI" requirement** -- cannot be planned without design mockups and a frontend repository. This should be planned as a separate feature once designs are available.

---

## Impact Map

```
trustify-backend:
  changes:
    - Add GIN indexes on searchable text columns for SBOMs, advisories, and packages to improve full-text search performance
    - Implement relevance-based ranking (ts_rank) in SearchService to return results ordered by relevance score
    - Add filter parameters to the search endpoint for entity type, severity, license, and date range
    - Extend the shared query builder in common/src/db/query.rs to support full-text search filtering and ranking
    - Add database migration for GIN indexes and tsvector columns
    - Update search integration tests to cover filtering, ranking, and performance
```

---

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. Each change can be merged independently without leaving `main` in a broken state:
- The database migration (GIN indexes) is additive -- it does not break existing queries.
- Filter parameters are optional query parameters -- existing clients are unaffected.
- Relevance ranking changes the default sort order of search results but does not break the API contract (the response shape remains `PaginatedResults<T>`).
- No cross-repository dependencies exist (all changes are within `trustify-backend`).
- No breaking API changes -- all modifications are backward-compatible additions.
