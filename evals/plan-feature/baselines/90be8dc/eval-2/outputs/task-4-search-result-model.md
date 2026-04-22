## Repository
trustify-backend

## Description
Create a structured search result model that includes relevance score metadata alongside the matched entity data. Currently the search module lacks a dedicated model directory. Adding a proper result model enables the API to return relevance scores to consumers, which is essential for the "more relevant results" requirement — users and frontend clients can see and use the relevance ranking.

## Files to Create
- `modules/search/src/model/mod.rs` — Define `SearchResult` struct wrapping matched entities with a `score: f32` relevance field, and a `SearchResultType` enum (Sbom, Advisory, Package) for typed discrimination

## Files to Modify
- `modules/search/src/lib.rs` — Register the new `model` submodule
- `modules/search/src/service/mod.rs` — Return `SearchResult` items (with score) instead of raw entity data
- `modules/search/src/endpoints/mod.rs` — Serialize `SearchResult` in JSON responses, ensuring `score` field is included in output

## API Changes
- `GET /api/v2/search` — MODIFY: Response items now include a `score` float field indicating relevance ranking and a `type` string field indicating the entity type (sbom, advisory, package)

## Implementation Notes
Follow the model pattern used in other modules (e.g., `modules/fundamental/src/sbom/model/`):

1. Define `SearchResult` as a struct with fields: `score: f32`, `result_type: SearchResultType`, and the entity summary (use an enum or trait object to hold `SbomSummary`, `AdvisorySummary`, or `PackageSummary`).
2. Implement `serde::Serialize` for `SearchResult` to produce clean JSON output.
3. Consider using `#[serde(tag = "type")]` for the entity type discriminator to produce clean JSON like `{"type": "advisory", "score": 0.95, ...}`.
4. Update `SearchService` in `modules/search/src/service/mod.rs` to construct `SearchResult` instances from query results, populating the `score` from `ts_rank`.
5. Update the endpoint in `modules/search/src/endpoints/mod.rs` to return `PaginatedResults<SearchResult>` using the wrapper from `common/src/model/paginated.rs`.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Entity summary struct included in search results
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Entity summary struct included in search results
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Entity summary struct included in search results
- `common/src/model/paginated.rs::PaginatedResults` — Paginated response wrapper for search results

## Acceptance Criteria
- [ ] `SearchResult` struct includes `score`, `type`, and entity data fields
- [ ] JSON serialization produces clean output with `type` discriminator and `score` field
- [ ] Search endpoint returns `PaginatedResults<SearchResult>` with relevance scores
- [ ] Results are ordered by `score` descending in the response
- [ ] The `type` field correctly identifies each result as sbom, advisory, or package

## Test Requirements
- [ ] `SearchResult` serializes to expected JSON format
- [ ] Score values are correctly populated from database `ts_rank` results
- [ ] All three entity types serialize correctly within `SearchResult`

## Verification Commands
- `cargo test -p search` — All search tests pass
- `cargo clippy -p search` — No linting warnings

## Dependencies
- Depends on: Task 2 — Implement relevance-ranked search in SearchService
