# Repository Impact Map — TC-9002: Improve search experience

## Inherited Fields

- **Priority**: Normal (inherited from TC-9002, propagated to all tasks)
- **fixVersions**: RHTPA 1.6.0 (inherited from TC-9002, propagated to all tasks per fixVersion scope default "both")

## Workflow Mode

**direct-to-main** — No atomicity indicators identified. Each search improvement (filtering, relevance, performance) can be merged independently without leaving `main` in a broken state. There are no coordinated schema migrations, breaking API changes, or cross-cutting refactors that require all changes to land together.

## Ambiguities

The following ambiguities were identified in the TC-9002 feature description. These are flagged for clarification with the feature owner before or during implementation:

1. **"Search should be faster" — no performance target defined.** The feature states search is "currently too slow" but provides no baseline metrics (current latency) or target metrics (acceptable latency, e.g., p95 < 200ms). **Assumption (pending clarification):** optimization will focus on adding database indexes for full-text search columns and optimizing query patterns in SearchService, with performance validated by before/after measurement rather than a fixed threshold.

2. **"Results should be more relevant" — no definition of relevance.** The feature does not define what "relevant" means — no ranking criteria, scoring algorithm, or examples of good vs. bad results are provided. **Assumption (pending clarification):** relevance will be improved by implementing PostgreSQL full-text search ranking (`ts_rank` or equivalent) to order results by match quality, rather than the current unranked ordering.

3. **"Add filters — some kind of filtering capability" — filter types unspecified.** The feature does not specify which filters to add (entity type? date range? severity? license? package name?). **Assumption (pending clarification):** initial filtering will support entity type filtering (SBOM, advisory, package) and a text-field qualifier to narrow search scope, using the existing query builder helpers in `common/src/db/query.rs`.

4. **"Should be fast enough" — non-functional requirement with no measurable target.** This NFR is not actionable without a concrete performance threshold. **Assumption (pending clarification):** this is treated as covered by the performance optimization task (Task 3).

5. **"Don't break existing functionality" — standard but unverifiable as stated.** **Assumption (pending clarification):** existing integration tests in `tests/api/search.rs` serve as the regression baseline. All existing tests must continue to pass.

## Excluded Requirements

| Requirement | Reason for Exclusion |
|---|---|
| Better UI — "Make it look nicer" | Cannot be planned: no design mockups or visual specifications are available, and no frontend repository is in scope. Only `trustify-backend` (a Rust backend service) is available for planning. This requirement needs a frontend repository and Figma designs before it can be decomposed into tasks. |

## trustify-backend

changes:
  - Add filtering parameters to the search endpoint (GET /api/v2/search) to support entity type filtering and search scope qualifiers
  - Extend SearchService to accept filter parameters and apply them to search queries
  - Implement relevance-based result scoring and ordering in SearchService using full-text search ranking
  - Expose sort-by-relevance option on the search endpoint
  - Add database migration for full-text search indexes to improve query performance
  - Optimize search query patterns in SearchService for index utilization
  - Add integration tests for new filtering, relevance scoring, and performance improvements
