## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler and register it in the
SBOM route module. This endpoint calls `SbomService::advisory_severity_summary`, applies
a 5-minute cache header, and supports an optional `?threshold` query parameter to filter
severity counts above a given severity level. The endpoint returns the
`AdvisorySeveritySummary` JSON response.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler function for `GET /api/v2/sbom/{id}/advisory-summary` with cache configuration and optional threshold query param

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route and add `pub mod advisory_summary;`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with 5-minute cache; optional `?threshold=critical|high|medium|low` query param filters to counts at or above the specified severity

## Implementation Notes
- Follow the existing endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` — that handler demonstrates how to:
  - Extract path parameters (`Path<Uuid>`)
  - Call `SbomService` methods
  - Return `Result<Json<T>, AppError>` from the handler
  - Handle 404 errors for missing SBOMs
- For route registration, follow the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` — existing routes like `list.rs` and `get.rs` are registered there. Add the new route as `.route("/api/v2/sbom/:id/advisory-summary", get(advisory_summary::handler))`.
- **Caching:** Use `tower-http` caching middleware as described in the repo conventions. Apply a `Cache-Control: max-age=300` header (5 minutes) to the response. Follow the cache configuration pattern used in existing endpoint route builders.
- **Threshold query parameter (non-MVP but included for completeness):** Define a `ThresholdQuery` struct with `#[derive(Deserialize)]` containing `threshold: Option<String>`. When `threshold` is provided, filter the `AdvisorySeveritySummary` to zero out counts below the threshold severity (e.g., `?threshold=high` zeroes out `medium` and `low`, recalculates `total`). Severity ordering: critical > high > medium > low.
- The handler signature should be: `async fn handler(Path(id): Path<Uuid>, Query(params): Query<ThresholdQuery>, service: Extension<SbomService>) -> Result<Json<AdvisorySeveritySummary>, AppError>`
- Per `docs/constraints.md` section 2 (Commit Rules): commits must reference TC-9001, use Conventional Commits format, and include the AI assistance trailer.
- Per `docs/constraints.md` section 3 (PR Rules): the feature branch must be named after the Jira issue ID and the PR link must be posted to the Jira task.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — handler pattern for path param extraction, service invocation, and error response for a single-SBOM endpoint
- `modules/fundamental/src/sbom/endpoints/list.rs` — handler pattern for query param extraction and paginated response building
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern showing how to mount handlers on the Axum router

## Dependencies
- Depends on: Task 2 — Add severity aggregation query to SbomService

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` for a valid SBOM ID
- [ ] Endpoint returns 404 when the SBOM ID does not exist
- [ ] Response includes `Cache-Control: max-age=300` header
- [ ] Optional `?threshold` query param filters severity counts correctly (zeroes out levels below threshold, recalculates total)
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`
- [ ] Project compiles without errors (`cargo check`)

## Test Requirements
- [ ] Handler unit test: verify 200 response with correct JSON shape for a valid SBOM
- [ ] Handler unit test: verify 404 response for non-existent SBOM
- [ ] Handler unit test: verify `Cache-Control` header is present with `max-age=300`
- [ ] Handler unit test: verify `?threshold=high` zeroes out medium and low counts and recalculates total
- [ ] Handler unit test: verify `?threshold=critical` returns only critical count with total matching critical

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors
