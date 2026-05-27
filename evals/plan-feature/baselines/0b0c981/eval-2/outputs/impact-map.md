# Repository Impact Map — TC-9002: Improve Search Experience

## Ambiguities Identified

The feature description (TC-9002) is intentionally vague and contains several ambiguities that must be resolved before implementation can proceed with full confidence. The following are flagged for clarification:

1. **"Search should be faster" — no performance baseline or target defined.** The description says search is "currently too slow" and should be "fast enough," but provides no current latency measurements, no target latency (e.g., p95 < 200ms), and no dataset size context. **Assumption (pending clarification):** We assume the goal is to add database indexing for full-text search columns and optimize the existing query path in `SearchService`. A reasonable target is p95 < 500ms for typical queries against the current dataset.

2. **"Results should be more relevant" — no definition of relevance.** The description does not specify what "relevant" means: whether results should be ranked by recency, by text match quality, by severity/risk score, or by some other criterion. It also does not specify whether the current search uses full-text search, simple LIKE queries, or something else. **Assumption (pending clarification):** We assume relevance means PostgreSQL full-text search ranking (`ts_rank`) should be used to order results by match quality, replacing any existing naive string matching.

3. **"Add filters" — filter dimensions not specified.** The description says "some kind of filtering capability" without specifying which fields should be filterable, what filter types are needed (exact match, range, multi-select), or which entity types support filtering. **Assumption (pending clarification):** We assume filters should cover the primary entity types visible in the search results — SBOMs (by name), advisories (by severity), and packages (by license) — using query parameter-based filtering on the existing `GET /api/v2/search` endpoint.

4. **No specification of which entities are searched.** The feature says "search" generically but does not state whether this covers SBOMs, advisories, packages, or all three. **Assumption (pending clarification):** Based on the repository structure showing `modules/search/` with a `SearchService` described as "full-text search across entities," we assume the improvement applies to all searchable entity types (SBOMs, advisories, packages).

5. **Non-functional requirements are vague.** "Should be fast enough" and "don't break existing functionality" are not measurable. **Assumption (pending clarification):** We interpret "don't break existing functionality" as requiring backward-compatible API changes (existing clients should not break) and "fast enough" as covered by ambiguity #1 above.

## Out of Scope

- **"Better UI" (non-MVP):** This requirement is explicitly marked as non-MVP in the feature description. Additionally, the target repository (`trustify-backend`) is a backend service — there is no frontend repository available to plan UI changes against, and no design mockups or Figma links have been provided. This requirement is excluded from the implementation plan entirely.

## Workflow Mode

**Selected mode: `direct-to-main`**

**Rationale:** No atomicity indicators are present. The planned changes are all within a single repository (`trustify-backend`) and can be delivered incrementally:
- The database migration adding search indexes can land independently (it adds indexes, does not remove or rename columns).
- The search relevance improvements are backward-compatible changes to the existing search endpoint.
- The filter additions extend the existing query parameters without breaking current clients.

Each task's PR can be merged to `main` independently without leaving the codebase in a broken state.

## Impact Map

```
trustify-backend:
  changes:
    - Add PostgreSQL full-text search indexes via database migration for SBOM, advisory, and package entities
    - Implement full-text search ranking in SearchService using ts_rank to improve result relevance
    - Add query parameter filters to GET /api/v2/search endpoint for severity, license, and entity type
    - Add integration tests for search performance, relevance ranking, and filter functionality
```
