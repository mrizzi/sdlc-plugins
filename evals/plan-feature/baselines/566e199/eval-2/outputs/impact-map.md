# Repository Impact Map — TC-9002: Improve Search Experience

## Ambiguities Identified

The feature description for TC-9002 is vague and underspecified across multiple dimensions. The following ambiguities are flagged for clarification before implementation proceeds:

1. **"Search should be faster" — no performance baseline or target defined.** The description states search is "currently too slow" and should be "fast enough," but provides no current latency measurements, no target SLA (e.g., p95 < 200ms), and no dataset size context. Without a baseline, there is no way to verify the improvement objectively. **Assumption (pending clarification):** We assume the primary performance bottleneck is the lack of database-level full-text search indexes. Adding PostgreSQL GIN indexes on tsvector columns for searchable entities and refactoring the query path in `SearchService` to use `ts_rank`-based ranking should address the speed concern. A reasonable target is p95 < 500ms for typical queries against the current dataset.

2. **"Results should be more relevant" — no definition of relevance.** The description does not specify what "relevant" means: whether results should be ranked by text match quality, by recency, by severity/risk score, or by some other criterion. It also does not clarify whether the current implementation uses full-text search, simple LIKE queries, or another approach. **Assumption (pending clarification):** We assume relevance means PostgreSQL full-text search ranking (`ts_rank`) should be used to order results by text match quality, replacing any existing naive string matching in the `SearchService` (`modules/search/src/service/mod.rs`).

3. **"Add filters — some kind of filtering capability" — filter dimensions not specified.** The description says "some kind of filtering capability" but does not specify which fields should be filterable, what filter types are needed (exact match, range, multi-select), or which entity types support filtering. **Assumption (pending clarification):** Based on the entity models visible in the repository — `AdvisorySummary` (includes severity field in `modules/fundamental/src/advisory/model/summary.rs`), `PackageSummary` (includes license field in `modules/fundamental/src/package/model/summary.rs`) — we assume filters should cover entity type (sbom, advisory, package), advisory severity, and package license, applied as optional query parameters on the existing `GET /api/v2/search` endpoint.

4. **No specification of which entities are searchable.** The feature says "search" generically but does not state whether it covers SBOMs, advisories, packages, or all three. **Assumption (pending clarification):** Based on the repository structure showing `modules/search/` with a `SearchService` described as "full-text search across entities," we assume the improvements apply to all three entity types (SBOMs, advisories, packages).

5. **Non-functional requirements are unmeasurable.** "Should be fast enough" and "don't break existing functionality" are not testable as written. **Assumption (pending clarification):** We interpret "don't break existing functionality" as requiring backward-compatible API changes (existing clients using the current `GET /api/v2/search` interface should not break) and "fast enough" as addressed by the indexing improvements in ambiguity #1.

## Out of Scope

- **"Better UI" (non-MVP):** This requirement is explicitly marked as non-MVP in the feature description. Additionally, the target repository (`trustify-backend`) is a Rust backend service with no frontend code. No frontend repository is available in the Repository Registry, and no Figma design mockups have been provided. This requirement is excluded from the implementation plan entirely.

## Workflow Mode

**Selected mode: `direct-to-main`**

**Rationale:** No atomicity indicators are present. All planned changes are within a single repository (`trustify-backend`) and can be delivered incrementally:
- The database migration adding full-text search indexes can land independently — it adds new columns and indexes without removing or modifying existing ones.
- The search relevance improvements are backward-compatible changes to the existing `GET /api/v2/search` endpoint — the response shape (`PaginatedResults`) remains unchanged.
- The filter additions extend the existing query parameters without breaking current clients — all new parameters are optional.
- Integration tests can be added independently after the feature code is in place.

Each task's PR can be merged to `main` independently without leaving the codebase in a broken state.

## Impact Map

```
trustify-backend:
  changes:
    - Add PostgreSQL full-text search indexes via database migration (tsvector columns and GIN indexes on sbom, advisory, and package tables)
    - Refactor SearchService to use ts_rank-based full-text search ranking for improved result relevance
    - Add query parameter filters to GET /api/v2/search endpoint (entity type, severity, license)
    - Add comprehensive integration tests for search relevance ranking, filters, and backward compatibility
```
