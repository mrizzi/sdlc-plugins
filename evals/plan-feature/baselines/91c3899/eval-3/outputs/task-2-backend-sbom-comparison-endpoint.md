# Task 2 — Add SBOM comparison REST endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/compare?left={id1}&right={id2}` REST endpoint that invokes the comparison service from Task 1 and returns a JSON response with the structured diff. Register the route in the SBOM endpoint module and mount it alongside existing SBOM routes. Add integration tests covering the endpoint's HTTP behavior.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Axum handler for GET /api/v2/sbom/compare with query parameter extraction (left, right), validation, service invocation, and JSON response
- `tests/api/sbom_compare.rs` — Integration tests for the comparison endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Add `pub mod compare;` and register the /compare route in the router
- `tests/api/mod.rs` — Add `mod sbom_compare;` if a test module index exists, or ensure the new test file is included

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: accepts two SBOM IDs as query parameters, returns SbomComparisonResult JSON with six diff categories (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler structure: extract query parameters, call service, return JSON response.
- Define a query parameter struct (e.g., `CompareQuery { left: String, right: String }`) using Axum's `Query` extractor.
- Validate that both `left` and `right` are provided and are valid SBOM IDs. Return 400 Bad Request if either is missing or invalid. Return 404 if either SBOM ID does not exist.
- The handler should call the comparison service method created in Task 1 and serialize the result as JSON.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing routes. See the existing route registration pattern in that file — routes are added to an Axum Router.
- Per CONVENTIONS.md §Endpoint registration: each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` and modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint file scope.
- Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's Rust handler file scope.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task creates `tests/api/sbom_compare.rs` matching the convention's test file scope.
- Non-functional requirement: endpoint p95 response time must be <1s for SBOMs with up to 2000 packages each.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET handler demonstrating the Axum handler pattern, query/path extraction, and JSON response serialization
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route registration showing how to add new routes to the SBOM router
- `common/src/error.rs::AppError` — standard error enum with IntoResponse implementation for error responses
- `tests/api/sbom.rs` — existing SBOM integration tests demonstrating test database setup, HTTP request construction, and assertion patterns

## Acceptance Criteria
- [ ] GET /api/v2/sbom/compare?left={id1}&right={id2} returns 200 with a valid SbomComparisonResult JSON body
- [ ] Missing or invalid query parameters return 400 Bad Request
- [ ] Non-existent SBOM IDs return 404 Not Found
- [ ] The endpoint is registered and accessible alongside existing /api/v2/sbom routes
- [ ] Response Content-Type is application/json

## Test Requirements
- [ ] Integration test: compare two SBOMs with known package differences and verify the response body contains correct added/removed packages
- [ ] Integration test: compare two SBOMs with version changes and verify direction field (upgrade/downgrade)
- [ ] Integration test: compare two SBOMs with advisory differences and verify new/resolved vulnerabilities
- [ ] Integration test: request with missing `left` parameter returns 400
- [ ] Integration test: request with non-existent SBOM ID returns 404
- [ ] Integration test: comparing an SBOM with itself returns empty diff arrays

## Verification Commands
- `cargo test --test api sbom_compare` — all comparison endpoint integration tests pass

## Dependencies
- Depends on: Task 1 — Add SBOM comparison model and service
