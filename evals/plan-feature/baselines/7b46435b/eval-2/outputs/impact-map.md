# Impact Map: TC-9002 -- Improve search experience

## Feature
Improve the search experience in the trustify-backend platform. Users have reported that search is slow and returns irrelevant results. The feature aims to make search faster, improve result relevance, and add filtering capabilities.

## Ambiguities

The following ambiguities were identified in the feature description and must be clarified with the product owner before implementation begins. Tasks below include assumptions that should be validated.

1. **"Search should be faster" -- no performance targets specified.** The requirement states search is "currently too slow" but provides no measurable performance targets (e.g., p95 latency < 200ms, throughput targets, dataset size expectations). Without concrete targets, it is impossible to verify whether the performance improvement is sufficient.
   - **Assumption pending clarification:** Performance improvement will be achieved via PostgreSQL full-text search indexes (GIN indexes on searchable text columns). Success will be measured by observable query plan improvement and reduced response times under load, but no specific SLA is defined.

2. **"Results should be more relevant" -- no relevance criteria defined.** The requirement does not specify what "relevant" means: no ranking algorithm, scoring factors, weighting preferences, or definition of relevance relative to user intent. "Users complain about irrelevant results" does not explain which results are irrelevant or what results should appear instead.
   - **Assumption pending clarification:** Relevance will be implemented using PostgreSQL full-text search ranking (ts_rank) to score results by text-match quality. Results will be ordered by descending relevance score. This is a standard approach but may not match specific user expectations without further requirements.

3. **"Add filters" -- no filter specification.** The requirement says "some kind of filtering capability" but does not specify which fields should be filterable, what filter types are needed (exact match, range, multi-select), which entities support filtering, or how filters interact with each other (AND vs OR logic).
   - **Assumption pending clarification:** Filters will include entity type (sbom, advisory, package) and a text query refinement parameter, leveraging existing query builder helpers in `common/src/db/query.rs`. Additional filter fields can be added once requirements are clarified.

4. **Non-functional requirement "Should be fast enough" -- no concrete latency target.** This repeats the performance ambiguity without adding specificity. No p50/p95/p99 latency targets, no concurrent user expectations, no dataset size benchmarks.
   - **Assumption pending clarification:** The indexing and query optimization changes will provide measurable improvement. Specific latency SLAs should be defined by the product owner.

5. **Non-functional requirement "Don't break existing functionality" -- no regression scope defined.** All changes should avoid breaking existing functionality, but no specific regression test suite or backwards-compatibility contract is referenced.
   - **Assumption pending clarification:** Existing search endpoint behavior (response shape, query parameters) will be preserved. New parameters are additive. Existing integration tests in `tests/api/search.rs` must continue to pass.

## Excluded Requirements

| Requirement | Is MVP? | Reason for Exclusion |
|---|---|---|
| Better UI -- "Make it look nicer" | No | Cannot be planned: no design mockups are available, no Figma URL was provided, and no frontend repository is listed in the Repository Registry. UI improvements require visual specifications and a frontend codebase to target. This requirement should be re-planned once design mockups are provided and a frontend repository is registered. |

## Repositories Affected

| Repository | Role |
|---|---|
| trustify-backend | Primary -- all search performance, relevance, and filtering changes land here. This is the Rust backend service that manages SBOMs, advisories, packages, and exposes the REST API including the search endpoint at `GET /api/v2/search`. |

## Specific Changes Needed

### Migration Layer
- Create a new database migration to add PostgreSQL GIN indexes on text columns used by the search service (SBOM names, advisory titles, package names)
- Register the new migration in `migration/src/lib.rs`

### Service Layer
- Modify `SearchService` in `modules/search/src/service/mod.rs` to use PostgreSQL full-text search with `tsvector`/`tsquery` and `ts_rank` for relevance scoring
- Add relevance score to search result items and order by descending score
- Add support for entity type filtering and query refinement parameters

### Endpoint Layer
- Modify `GET /api/v2/search` handler in `modules/search/src/endpoints/mod.rs` to accept optional filter query parameters (entity type, query refinement)
- Ensure response shape is backwards-compatible (new fields are additive)

### Integration Tests
- Extend `tests/api/search.rs` with test cases for: filtered search by entity type, relevance ordering, search with indexes, empty results, backwards compatibility of existing behavior

## Workflow Mode Decision

**Mode**: Direct-to-main

**Rationale**: This feature is a single-repository change improving an existing endpoint. All changes land in trustify-backend. There are no coordinated schema migrations that require atomicity across tasks -- the migration adds indexes (non-breaking, additive), the service changes are additive, and the endpoint changes preserve backwards compatibility. No cross-repository dependencies exist. Each task's PR can be merged independently without leaving main in a broken state.
