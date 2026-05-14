# Task 3: Improve Search Result Relevance Scoring

## Repository
trustify-backend

## Target Branch
main

## Description
Implement relevance-based ranking for search results so that the most useful results appear first. This addresses the TC-9002 requirement that "results should be more relevant" and users "complain about irrelevant results."

**Assumption (pending clarification)**: "Relevant" is assumed to mean the following ranking strategy, since no definition of relevance was provided in the feature description:
1. Exact matches on name/title rank above partial matches.
2. PostgreSQL `ts_rank` score is used as the primary ranking signal.
3. Advisory severity acts as a secondary ranking boost (critical > high > medium > low > none).
4. Results are grouped by entity type in the response (SBOMs, advisories, packages) so users can distinguish between them.

These assumptions should be validated with the product owner, ideally with example queries and expected result orderings.

**Assumption (pending clarification)**: The search response currently returns a flat list of mixed entity types. This task assumes the response should include a `relevance_score` field per result to support client-side re-ranking or display, but the exact response shape is not specified in TC-9002.

## Files to Modify
- `modules/search/src/service/mod.rs` — Add `ts_rank` scoring to the full-text search queries built in Task 2; implement ranking logic that orders results by relevance score descending; add optional severity-based boost for advisory results
- `modules/search/src/endpoints/mod.rs` — Update the `GET /api/v2/search` response to include a `relevance_score` field per result item
- `common/src/model/paginated.rs` — Consider extending `PaginatedResults<T>` or creating a `ScoredResult<T>` wrapper that includes a `relevance_score: f64` field alongside each result item

## Files to Create
- `modules/search/src/model/mod.rs` — Define a `SearchResult` struct that wraps entity summaries with a `relevance_score` field and an `entity_type` discriminator (e.g., "sbom", "advisory", "package")

## Implementation Notes
- Use PostgreSQL's `ts_rank(tsvector, tsquery)` function to compute relevance scores. This function is natively supported and will leverage the GIN indexes from Task 1.
- In `modules/search/src/service/mod.rs`, modify the search queries to:
  1. Select `ts_rank(to_tsvector('english', column), to_tsquery('english', ?)) AS rank` alongside entity data.
  2. Order results by `rank DESC`.
  3. For advisory results, apply a severity-based weight multiplier: critical = 1.5x, high = 1.3x, medium = 1.0x, low = 0.8x. The severity field is available on `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`.
- Create a new `SearchResult` model in `modules/search/src/model/mod.rs` following the module convention of `model/ + service/ + endpoints/`. The struct should contain:
  - `entity_type: String` — discriminator ("sbom", "advisory", "package")
  - `relevance_score: f64` — computed from `ts_rank`
  - `summary: serde_json::Value` — the serialized entity summary (polymorphic over `SbomSummary`, `AdvisorySummary`, `PackageSummary`)
- Update the search endpoint in `modules/search/src/endpoints/mod.rs` to return `PaginatedResults<SearchResult>` instead of the current response type.
- Follow error handling patterns from `common/src/error.rs`: return `Result<T, AppError>` with `.context()`.

## Acceptance Criteria
- [ ] Search results are ordered by relevance score (most relevant first)
- [ ] Each search result includes a `relevance_score` field in the API response
- [ ] Each search result includes an `entity_type` discriminator
- [ ] Exact name/title matches rank higher than partial matches
- [ ] Advisory results with higher severity receive a ranking boost
- [ ] The `GET /api/v2/search` endpoint returns `PaginatedResults<SearchResult>`
- [ ] Existing search functionality continues to work (no breaking changes to existing query behavior)

## Test Requirements
- [ ] Integration test in `tests/api/search.rs`: search for an exact advisory title and verify it ranks first in results
- [ ] Integration test: search for a term that matches both a high-severity advisory and a low-severity advisory; verify the high-severity result ranks higher
- [ ] Integration test: verify that the response includes `relevance_score` and `entity_type` fields
- [ ] Verify that pagination still works correctly with the new `SearchResult` response type

## Dependencies
- Depends on: Task 2 — Optimize SearchService Query Execution
