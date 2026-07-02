# Repository Impact Map — TC-9002: Improve search experience

## Ambiguities Identified

The feature description contains several ambiguities that must be resolved before implementation can proceed with full confidence. The following are flagged for clarification with the product owner:

1. **"Search should be faster" — no performance baseline or target defined.** The description says search is "currently too slow" but provides no metrics (current response time, target response time, percentile thresholds). **Assumption (pending clarification):** "faster" means reducing p95 search query latency to under 500ms by adding database indexes and optimizing the query path.

2. **"Results should be more relevant" — no relevance criteria specified.** "Users complain about irrelevant results" does not define what makes a result relevant. There is no ranking algorithm, weighting scheme, or relevance scoring criteria described. **Assumption (pending clarification):** "more relevant" means implementing PostgreSQL full-text search ranking (ts_rank/ts_rank_cd) so results are ordered by textual match quality rather than insertion order or alphabetical order.

3. **"Add filters — some kind of filtering capability" — filter fields, operations, and behavior unspecified.** The description does not state which fields should be filterable, what filter operations to support (exact match, substring, range, multi-select), or how multiple filters combine (AND vs OR). **Assumption (pending clarification):** filters will cover entity type, date range, and severity — using AND semantics — leveraging the existing shared query builder helpers in `common/src/db/query.rs`.

4. **"Should be fast enough" (non-functional requirement) — no quantifiable metric.** This NFR provides no measurable threshold. **Assumption (pending clarification):** interpreted as p95 latency under 500ms for search queries returning up to 100 results.

5. **"Don't break existing functionality" — no regression criteria.** No specific backward-compatibility requirements or regression test coverage expectations are defined. **Assumption (pending clarification):** existing GET /api/v2/search endpoint contract (request parameters, response shape) must remain backward-compatible; new parameters are additive only.

## Scope Exclusion

- **"Better UI" (non-MVP):** This requirement is excluded from the implementation plan. It cannot be planned without design mockups or a frontend repository. The Repository Registry in CLAUDE.md lists only `sdlc-plugins` (this plugin repo); no frontend repository is configured. When a frontend repository and Figma designs become available, a separate planning session should address this requirement.

## Impact Map

```
trustify-backend:
  changes:
    - Add database migration with GIN indexes on text-searchable columns to improve search query performance
    - Optimize SearchService full-text search query and implement result relevance ranking using ts_rank
    - Add filter query parameters (entity type, date range, severity) to the GET /api/v2/search endpoint
    - Add integration tests covering search performance, relevance ordering, and filter behavior
```

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified:
- No coordinated schema migrations across tasks — the database index migration (Task 1) is self-contained and does not break existing functionality if merged independently.
- No breaking API changes — all search endpoint changes are additive (new query parameters, new response fields for ranking score); the existing contract is preserved.
- No cross-cutting refactors — changes are localized to the search module and a new migration.
- No tightly coupled frontend/backend — this plan covers backend only; the "Better UI" requirement is excluded from scope.

All tasks can be merged independently to `main` without leaving the codebase in a broken state.
