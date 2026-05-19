# Repository Impact Map -- TC-9002: Improve Search Experience

## Feature Summary

TC-9002 requests improvements to the search experience: faster performance, more relevant results, and the addition of filtering capabilities. A fourth requirement ("Better UI") is excluded from this plan -- see Excluded Requirements below.

## Ambiguities and Open Questions

The feature description is notably vague across every requirement. The following ambiguities must be resolved before implementation begins. Each is flagged with a severity level.

### Critical Ambiguities (block implementation)

| # | Ambiguity | What is missing | Impact on planning |
|---|---|---|---|
| A1 | "Search should be faster" -- no quantitative target | Current p50/p95 latency is unknown; target latency is unspecified. Without a measurable goal, there is no way to verify the requirement is met. | Task 1 assumes a goal of adding database indexing and query optimization. **Pending clarification:** acceptable latency target (e.g., p95 < 200ms). |
| A2 | "Results should be more relevant" -- no definition of relevance | No ranking criteria, no weighting specification, no examples of "irrelevant" results. Does "relevant" mean full-text ranking, field boosting, or something else? | Task 2 assumes PostgreSQL full-text search with ts_rank as a starting point. **Pending clarification:** what makes a result "relevant" vs. "irrelevant" from a user perspective. |
| A3 | "Add filters" -- which filters? | No specification of which fields should be filterable, which entities support filtering, or whether filters combine with AND/OR logic. | Task 3 assumes filters on commonly useful fields per entity (severity for advisories, license for packages). **Pending clarification:** exact filter fields and combination logic. |
| A4 | Searchable entity scope undefined | The current search module (`modules/search/`) provides full-text search "across entities," but the feature does not specify which entities (SBOMs, advisories, packages) are in scope. | All tasks assume all three entity types are in scope. **Pending clarification:** which entities are included. |

### Non-Critical Ambiguities (can proceed with assumptions)

| # | Ambiguity | Assumption |
|---|---|---|
| A5 | "Should be fast enough" -- no NFR target | Assumed: search queries should complete within 500ms at p95 under normal load. This is a placeholder; real SLA must be confirmed. |
| A6 | "Don't break existing functionality" -- no regression scope | Assumed: existing integration tests in `tests/api/search.rs` define the regression boundary. No new regression test matrix is specified. |
| A7 | Full-text vs. structured search | Assumed: the existing `SearchService` uses basic SQL LIKE/ILIKE matching. Improvement means adding PostgreSQL full-text search (tsvector/tsquery) for ranking, while preserving structured field-based queries. |

## Excluded Requirements

| Requirement | Reason for exclusion |
|---|---|
| "Better UI" (non-MVP) | No frontend repository is available in the project configuration. No Figma mockups or design specifications exist. UI improvements cannot be planned without a frontend codebase and visual designs. This requirement should be revisited when a frontend repository is onboarded and design mockups are provided. |

## Repository: trustify-backend

### Impacted Modules

| Module | Path | Impact | Reason |
|---|---|---|---|
| search | `modules/search/` | **Major** | Core module for this feature: service logic, endpoint, query optimization |
| common/db | `common/src/db/` | **Moderate** | Query builder helpers need new filter and full-text search support |
| entity | `entity/src/` | **Moderate** | Entity definitions may need tsvector columns or index annotations |
| migration | `migration/src/` | **Major** | New migration for full-text search indexes and tsvector columns |
| fundamental/advisory | `modules/fundamental/src/advisory/` | **Minor** | Advisory-specific filter parameters (e.g., severity) |
| fundamental/package | `modules/fundamental/src/package/` | **Minor** | Package-specific filter parameters (e.g., license) |
| fundamental/sbom | `modules/fundamental/src/sbom/` | **Minor** | SBOM-specific filter parameters (if applicable) |
| server | `server/src/main.rs` | **None** | No changes expected -- search routes already mounted |
| tests | `tests/api/search.rs` | **Moderate** | Updated and new integration tests for search improvements |

### Impacted Files

| File | Change type | Reason |
|---|---|---|
| `modules/search/src/service/mod.rs` | Modify | Rewrite search queries to use full-text search; add filter support; add relevance ranking |
| `modules/search/src/endpoints/mod.rs` | Modify | Accept new query parameters (filters, sort-by-relevance) |
| `common/src/db/query.rs` | Modify | Add full-text search query builder helpers; add filter combinators |
| `entity/src/sbom.rs` | Modify | Add tsvector column annotation (if using stored tsvector approach) |
| `entity/src/advisory.rs` | Modify | Add tsvector column annotation |
| `entity/src/package.rs` | Modify | Add tsvector column annotation |
| `migration/src/` (new migration) | Create | Migration for GIN indexes on tsvector columns |
| `tests/api/search.rs` | Modify | New tests for filters, relevance ranking, performance |

### Key Reuse Candidates

| Symbol / File | Relevance |
|---|---|
| `common/src/db/query.rs` -- shared query builder helpers | Filtering and pagination patterns already exist here; extend rather than duplicate |
| `common/src/model/paginated.rs` -- `PaginatedResults<T>` | Search results already use this; continue using for filtered/ranked results |
| `common/src/error.rs` -- `AppError` | Error handling pattern for new filter validation errors |
| `modules/fundamental/src/advisory/service/advisory.rs` -- `AdvisoryService::search` | Existing search method to understand current search pattern |

## Workflow Mode

**Recommended: direct-to-main**

Rationale: The three tasks (performance/indexing, relevance ranking, filters) can be delivered incrementally. Each task produces a self-contained improvement that does not require the others to be deployed simultaneously. There are no breaking API changes -- the search endpoint gains optional parameters while maintaining backward compatibility. The migration in Task 1 adds indexes and columns without altering existing schema.

## Task Breakdown

| Task | Title | Dependencies | Key files |
|---|---|---|---|
| 1 | Add full-text search indexes and tsvector migration | None | `migration/`, `entity/src/`, `common/src/db/query.rs` |
| 2 | Implement relevance-ranked search using full-text search | Task 1 | `modules/search/src/service/mod.rs`, `modules/search/src/endpoints/mod.rs` |
| 3 | Add search filter parameters | Task 2 | `modules/search/src/endpoints/mod.rs`, `modules/search/src/service/mod.rs`, `common/src/db/query.rs` |
