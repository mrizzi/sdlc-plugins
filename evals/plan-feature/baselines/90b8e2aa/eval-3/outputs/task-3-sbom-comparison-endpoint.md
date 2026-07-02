## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the GET /api/v2/sbom/compare REST endpoint that accepts `left` and `right` SBOM IDs as query parameters and returns a structured diff result computed by the comparison service from Task 2. Add comprehensive integration tests covering success, error, and edge cases.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler for GET /api/v2/sbom/compare with query parameter extraction and comparison service invocation
- `tests/api/sbom_compare.rs` — Integration tests for the comparison endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the /compare route alongside existing SBOM routes

## API Changes
- `GET /api/v2/sbom/compare?left={id}&right={id}` — NEW: Returns SbomComparisonResult JSON with six diff sections (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)

## Implementation Notes
- Follow the endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (GET /api/v2/sbom/{id}) for handler structure, parameter extraction, and response formatting.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing SBOM routes following the established route registration pattern.
- Extract `left` and `right` query parameters using Axum's `Query` extractor with a dedicated query params struct.
- Return 400 Bad Request if either `left` or `right` parameter is missing.
- Return 404 Not Found if either SBOM ID does not exist (propagated from the comparison service error).
- Call the comparison service from Task 2 and return `Result<Json<SbomComparisonResult>, AppError>`.
- Per the backend key conventions (Endpoint registration): each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules. Register the compare route in the SBOM endpoints module.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's Rust endpoint scope.
- Per the backend key conventions (Testing): integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task creates `tests/api/sbom_compare.rs` matching the convention's Rust test file scope.
- Non-functional: p95 response time target < 1s for SBOMs with up to 2000 packages each.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing handler pattern for SBOM detail endpoint (parameter extraction, service call, response formatting)
- `modules/fundamental/src/sbom/endpoints/list.rs` — existing handler pattern for SBOM list endpoint (query parameter handling)
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow
- `common/src/error.rs::AppError` — error handling enum with IntoResponse implementation
- `tests/api/sbom.rs` — existing SBOM integration test patterns to follow

## Acceptance Criteria
- [ ] GET /api/v2/sbom/compare?left={id1}&right={id2} returns 200 with correct SbomComparisonResult JSON
- [ ] Returns 400 Bad Request when `left` or `right` query parameter is missing
- [ ] Returns 404 Not Found when either SBOM ID does not exist
- [ ] Response JSON contains all six sections: added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes
- [ ] Comparing identical SBOMs returns empty arrays for all sections

## Test Requirements
- [ ] Integration test: compare two SBOMs with known differences, verify all six diff sections contain correct data
- [ ] Integration test: request with missing `left` query parameter returns 400
- [ ] Integration test: request with missing `right` query parameter returns 400
- [ ] Integration test: request with non-existent SBOM ID returns 404
- [ ] Integration test: comparing identical SBOMs returns empty diff sections

## Verification Commands
- `cargo test --test api sbom_compare` — all comparison endpoint integration tests pass

## Documentation Updates
- API documentation should include the new GET /api/v2/sbom/compare endpoint with query parameters, request/response examples, and error codes

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison model types and diff service logic
