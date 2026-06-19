# Repository Impact Map — TC-9002: Improve search experience

## Workflow Mode

**Mode**: `direct-to-main`

**Rationale**: All changes target a single repository (`trustify-backend`). The scope is
contained within the search module and shared query infrastructure. No cross-repo
coordination is required, so direct-to-main with individual task PRs is appropriate.

## Ambiguities and Open Questions

The feature description (TC-9002) is intentionally vague. The following ambiguities
were identified and must be resolved with the product owner before implementation
proceeds. Tasks below document assumptions made in the interim.

### Ambiguity 1: "Search should be faster" — no performance target

The requirement states search is "currently too slow" but provides no quantified
baseline or target. Questions requiring clarification:
- What is the current measured latency (p50, p95, p99)?
- What is the target latency SLA?
- Is the concern about query execution time, network round-trip, or perceived UI lag?
- At what data volume does the problem manifest (number of SBOMs, advisories)?

**ASSUMPTION (pending clarification)**: The performance issue is database query
execution time. Adding indexes and query optimization will be the first approach.

### Ambiguity 2: "Results should be more relevant" — no relevance definition

"More relevant" is undefined. Questions requiring clarification:
- What does a "relevant" result look like for each entity type?
- Should results be ranked by a scoring algorithm (e.g., TF-IDF, BM25)?
- Is relevance about full-text matching quality, or about returning the right entity types?
- Should exact matches rank higher than partial matches?

**ASSUMPTION (pending clarification)**: Relevance means implementing weighted
full-text search scoring using PostgreSQL's `ts_rank` capabilities, with exact
matches ranked above partial matches.

### Ambiguity 3: "Some kind of filtering capability" — no filter specification

The requirement says "Add filters" with no specifics. Questions requiring clarification:
- Which entity types need filtering (SBOMs? Advisories? Packages? All three?)?
- Which fields should be filterable (severity, date range, license, name)?
- Should filters be combinable (AND semantics, OR semantics, or both)?
- Are filters applied on the search endpoint only, or on list endpoints too?

**ASSUMPTION (pending clarification)**: Filters will be added to both the search
endpoint and entity list endpoints. Filterable fields will be based on existing model
fields: severity for advisories, license for packages, and date range for SBOMs.
Filters will use AND semantics when combined.

### Ambiguity 4: "Should be fast enough" (NFR) — no quantified NFR

The non-functional requirement "Should be fast enough" has no measurable threshold.

**ASSUMPTION (pending clarification)**: Search queries should complete within 500ms
at p95 under normal load. This will be validated with integration test timing but
not enforced as a hard gate.

### Ambiguity 5: "Don't break existing functionality" — no regression baseline

No existing test coverage baseline is stated. It is unclear which behaviors are
considered contractual vs. incidental.

**ASSUMPTION (pending clarification)**: All existing integration tests in `tests/api/`
must continue to pass. No existing API response shapes will be changed in a
backward-incompatible way.

## Out of Scope

**"Better UI" (non-MVP)**: This requirement is marked as non-MVP and cannot be
planned without design mockups or access to a frontend repository. The target
repository (`trustify-backend`) is a Rust backend service with no frontend code.
This requirement is excluded from the plan entirely.

## Impact Summary

| # | Area | Files Affected | Task |
|---|---|---|---|
| 1 | Database migration — search indexes | `migration/src/` (new migration) | Task 1 |
| 2 | Search service — relevance scoring | `modules/search/src/service/mod.rs` | Task 2 |
| 3 | Search endpoint — filter parameters | `modules/search/src/endpoints/mod.rs` | Task 3 |
| 4 | Shared query infrastructure — filter helpers | `common/src/db/query.rs` | Task 4 |
| 5 | Entity list endpoints — filter support | `modules/fundamental/src/*/endpoints/list.rs` | Task 4 |
| 6 | Integration tests — search and filter coverage | `tests/api/search.rs` | Task 5 |
| 7 | Search caching — response caching | `modules/search/src/endpoints/mod.rs` | Task 6 |

## Task Sequence

1. **Task 1**: Add database indexes for full-text search columns
2. **Task 2**: Enhance SearchService with relevance-scored full-text search
3. **Task 3**: Add filter query parameters to search endpoint
4. **Task 4**: Add filter support to entity list endpoints (SBOM, advisory, package)
5. **Task 5**: Add integration tests for search relevance and filtering
6. **Task 6**: Add caching layer for search endpoint responses

Tasks 1 and 2 are sequential (indexes must exist before relevance queries use them).
Tasks 3 and 4 depend on Task 2 (filter logic builds on the enhanced search service).
Task 5 depends on Tasks 3 and 4 (tests validate the new functionality).
Task 6 can proceed after Task 2 (caching is independent of filters).
