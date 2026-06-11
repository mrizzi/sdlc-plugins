# Task 3 — Add SBOM comparison endpoint and integration tests

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare?left={id1}&right={id2}` HTTP endpoint that invokes the comparison service from Task 2 and returns the structured diff as JSON. Register the route in the SBOM endpoints module and add integration tests against a real PostgreSQL test database.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/compare` route

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — handler for GET /api/v2/sbom/compare
- `tests/api/sbom_compare.rs` — integration tests for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: accepts two SBOM IDs as query parameters, returns `SbomComparisonResult` JSON with added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes

## Implementation Notes
- Follow the existing endpoint pattern: each endpoint gets its own file under `endpoints/` (see `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/sbom/endpoints/get.rs` for the established pattern).
- The handler should extract `left` and `right` query parameters, validate they are present, and call `SbomService::compare(left, right)`.
- Return 400 Bad Request if either query parameter is missing.
- Return 404 Not Found if either SBOM ID does not exist.
- Return the `SbomComparisonResult` serialized as JSON with status 200.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing list and get routes.
- Integration tests follow the pattern in `tests/api/sbom.rs` — use a real PostgreSQL test database and `assert_eq!(resp.status(), StatusCode::OK)`.
- Non-functional: endpoint should respond within p95 < 1s for SBOMs with up to 2000 packages each.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow
- `modules/fundamental/src/sbom/endpoints/get.rs` — handler pattern for extracting path/query params and calling service
- `modules/fundamental/src/sbom/endpoints/list.rs` — handler pattern for list endpoints
- `common/src/error.rs::AppError` — error handling for 400/404 responses
- `tests/api/sbom.rs` — integration test patterns for SBOM endpoints

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with structured diff JSON
- [ ] Returns 400 if `left` or `right` query parameter is missing
- [ ] Returns 404 if either SBOM ID does not exist
- [ ] Response shape matches the contract: `{ added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes }`
- [ ] Route is registered and accessible via the server

## Test Requirements
- [ ] Integration test: compare two SBOMs with known differences — verify 200 response with correct diff
- [ ] Integration test: request with missing `left` parameter — verify 400 response
- [ ] Integration test: request with missing `right` parameter — verify 400 response
- [ ] Integration test: request with non-existent SBOM ID — verify 404 response
- [ ] Integration test: compare identical SBOMs — verify 200 with empty diff sections

## Verification Commands
- `cargo test --test api sbom_compare` — all comparison endpoint integration tests pass

## Documentation Updates
- `README.md` — add the new comparison endpoint to the API reference section if one exists

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison model and diff service

[sdlc-workflow] Description digest: sha256-md:a5bf858e33d1c6c3a827f4206e23a61ff5b14975ef12a73f1d4504a260451649
