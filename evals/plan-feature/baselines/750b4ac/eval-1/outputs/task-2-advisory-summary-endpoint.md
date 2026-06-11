# Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint and route registration

## Repository
trustify-backend

## Target Branch
main

## Description
Add the HTTP endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary` and register the route in the SBOM endpoints module. This endpoint calls the `SbomService::get_advisory_severity_summary` method from Task 1 and returns the severity counts as a JSON response. It returns 404 if the SBOM does not exist, consistent with other SBOM endpoints.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — endpoint handler for GET /api/v2/sbom/{id}/advisory-summary

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with 200 OK, or 404 if SBOM not found

## Implementation Notes
- Follow the existing endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (GET /api/v2/sbom/{id}) for handler function signature, path parameter extraction, and error handling.
- The handler should extract the SBOM ID from the path, call `SbomService::get_advisory_severity_summary`, and return the result as `Json<AdvisorySeveritySummary>`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing route registration pattern used for `list.rs` and `get.rs`. Add a `.route("/api/v2/sbom/:id/advisory-summary", get(advisory_summary::handler))` entry.
- Use `Result<Json<AdvisorySeveritySummary>, AppError>` as the handler return type, following the convention in `common/src/error.rs` where `AppError` implements `IntoResponse`.
- The 404 case is handled by the service layer (Task 1) which returns an error when the SBOM is not found — the handler simply propagates the error via the `?` operator.
- Per CONVENTIONS.md §Framework: use Axum for HTTP handling.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` endpoint scope.
- Per CONVENTIONS.md §Endpoint registration: each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` module scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET handler for SBOM details; follow its handler signature, path parameter extraction, and error handling pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration file; follow its existing `.route()` pattern for adding the new endpoint
- `common/src/error.rs::AppError` — shared error type implementing IntoResponse; use for error propagation

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 404 when the SBOM ID does not exist
- [ ] The route is registered in the SBOM endpoints module
- [ ] Response content type is application/json

## Test Requirements
- [ ] Endpoint is covered by integration tests in Task 5

## Verification Commands
- `cargo build` — project compiles without errors after adding the new endpoint

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and severity aggregation service method

[sdlc-workflow] Description digest: sha256-md:498b3b238fd03c00c546298160e2a72eee179e93029ccc7b5ba7761ba9011c2f
