## Repository
trustify-backend

## Target Branch
main

## Description
Implement the `GET /api/v2/sbom/{id}/advisory-summary` HTTP endpoint handler that exposes the advisory severity aggregation service. The handler extracts the SBOM ID from the path, an optional `threshold` query parameter, calls the service method, and returns the `AdvisorySeveritySummary` as JSON. Configure 5-minute response caching via `tower-http` middleware on this route.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Axum handler function `get_advisory_summary` that extracts `Path(id)` and `Query(params)` (with optional `threshold` field), calls the service method, and returns `Json<AdvisorySeveritySummary>` or an `AppError`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Add `pub mod advisory_summary;` and register the new route `/api/v2/sbom/{id}/advisory-summary` in the router with 5-minute cache configuration

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with optional `?threshold=critical|high|medium|low` query parameter

## Implementation Notes
Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for how the existing `GET /api/v2/sbom/{id}` handler extracts path parameters and returns a JSON response. The new handler should:

1. Extract the SBOM ID from the path using Axum's `Path` extractor.
2. Define a query parameter struct (e.g., `AdvisorySummaryQuery`) with an `Option<SeverityThreshold>` field named `threshold`.
3. Use Axum's `Query` extractor to parse the optional threshold parameter.
4. Call the service method from Task 2 with the SBOM ID and optional threshold.
5. Return the result as `Json<AdvisorySeveritySummary>`.

For caching, follow the pattern used in other endpoint route builders in `modules/fundamental/src/sbom/endpoints/mod.rs`. Use `tower-http` caching middleware with a 5-minute (`max-age=300`) cache control header on this specific route.

Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` and use `.context()` wrapping.
Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Endpoint registration: register routes in `endpoints/mod.rs` and ensure `server/main.rs` mounts the module.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Module pattern: create the endpoint file under `endpoints/` following the `model/ + service/ + endpoints/` structure.
Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` module scope.

Per CONVENTIONS.md §Caching: use `tower-http` caching middleware in the endpoint route builder with appropriate cache control headers.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing SBOM GET handler pattern for path extraction and JSON response
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern with caching middleware

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns JSON with `critical`, `high`, `medium`, `low`, `total` fields
- [ ] Optional `?threshold` query parameter filters severity counts
- [ ] Returns 404 when SBOM ID does not exist
- [ ] Response includes `Cache-Control: max-age=300` header for 5-minute caching
- [ ] Route is registered in the SBOM module's router in `endpoints/mod.rs`
- [ ] Handler returns `Result<Json<AdvisorySeveritySummary>, AppError>`

## Test Requirements
- [ ] Test that valid request returns 200 with correct JSON shape
- [ ] Test that non-existent SBOM ID returns 404
- [ ] Test that `?threshold=critical` returns only critical counts (others zeroed)
- [ ] Test that response includes appropriate cache-control headers

## Dependencies
- Depends on: Task 1 — Advisory summary model (provides response types)
- Depends on: Task 2 — Advisory summary service (provides aggregation logic)

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}

[sdlc-workflow] Description digest: sha256-md:a930996125258e5e8af3b7d8b613f63c37ba3de25edf86535b8d81d0b2b29c57
