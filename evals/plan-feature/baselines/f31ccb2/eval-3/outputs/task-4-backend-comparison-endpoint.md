# Task 4 — Add GET /api/v2/sbom/compare endpoint

**Summary:** Add GET /api/v2/sbom/compare endpoint

**Labels:** ai-generated-jira

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Create the HTTP endpoint `GET /api/v2/sbom/compare?left={id1}&right={id2}` that accepts two SBOM IDs as query parameters, invokes the comparison service logic, and returns the structured diff as a JSON response. Register the route in the SBOM endpoint module.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — endpoint handler for `GET /api/v2/sbom/compare`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the comparison route alongside existing SBOM routes

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns `SbomComparisonResult` JSON with added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs`:
  - Handler function signature accepts Axum extractors (Query params, State with DB connection)
  - Returns `Result<Json<SbomComparisonResult>, AppError>`
  - Errors use `.context()` wrapping consistent with `common/src/error.rs::AppError`
- Define a query parameter struct with `left` and `right` fields (both required SBOM IDs) using `serde::Deserialize`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` using the same route registration pattern as existing endpoints (e.g., `.route("/compare", get(compare_sboms_handler))`).
- The route must be registered at the correct path to produce `/api/v2/sbom/compare` — check how existing routes like `/api/v2/sbom` and `/api/v2/sbom/{id}` are mounted in `server/src/main.rs`.
- Return HTTP 400 if either `left` or `right` parameter is missing.
- Return HTTP 404 if either SBOM ID does not exist (propagated from the service layer error).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for endpoint handler pattern with Axum extractors and JSON response
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for list endpoint pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — reference for route registration pattern
- `common/src/error.rs::AppError` — error handling with IntoResponse implementation

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with SbomComparisonResult JSON
- [ ] Missing `left` or `right` query parameter returns 400
- [ ] Non-existent SBOM ID returns 404
- [ ] Response JSON shape matches the contract defined in the feature specification
- [ ] Route is registered and accessible via the SBOM endpoint module

## Test Requirements
- [ ] Integration test: valid comparison request returns 200 with correct diff structure
- [ ] Integration test: missing query parameters return 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: comparison of two identical SBOMs returns empty diff sections

## Verification Commands
- `cargo test --test api sbom::compare` — expected: all comparison endpoint tests pass
- `curl "http://localhost:8080/api/v2/sbom/compare?left={id1}&right={id2}"` — expected: 200 response with valid JSON

## Dependencies
- Depends on: Task 3 — Add SBOM comparison diffing service logic
