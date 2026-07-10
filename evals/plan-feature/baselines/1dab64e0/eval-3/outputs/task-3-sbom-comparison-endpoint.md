## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare` endpoint that accepts `left` and `right` query parameters (SBOM IDs) and returns the structured diff computed by the comparison service created in Task 2. This endpoint enables the frontend comparison page to fetch diff data. Also add integration tests covering various comparison scenarios.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Endpoint handler for `GET /api/v2/sbom/compare?left={id1}&right={id2}` with query parameter extraction and validation
- `tests/api/sbom_compare.rs` — Integration tests for the comparison endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/compare` route in the SBOM endpoint router

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns `SbomComparisonResult` JSON containing added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, and license_changes arrays

## Implementation Notes
Follow the endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs` for handler structure and error handling.

The endpoint handler should:
1. Extract `left` and `right` query parameters using Axum's `Query` extractor
2. Validate that both parameters are present and are valid SBOM IDs; return `400 Bad Request` via `AppError` if missing or invalid
3. Call `SbomCompareService::compare(left, right)` from `modules/fundamental/src/sbom/service/compare.rs`
4. Return the `SbomComparisonResult` as JSON with `200 OK`
5. Return `404 Not Found` if either SBOM ID does not exist

Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing `/api/v2/sbom` routes, following the pattern used for `list.rs` and `get.rs` route registration.

Per CONVENTIONS.md: all endpoint handlers return `Result<T, AppError>` with `.context()` wrapping for error propagation.
Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's `.rs` endpoint file scope.

Per CONVENTIONS.md: register new routes in the module's `endpoints/mod.rs` and ensure `server/main.rs` mounts the module.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` endpoint registration scope.

Per CONVENTIONS.md: integration tests in `tests/api/` use a real PostgreSQL test database with `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task creates `tests/api/sbom_compare.rs` matching the convention's `.rs` test file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Reference for endpoint handler structure, query parameter extraction, and error handling pattern
- `modules/fundamental/src/sbom/endpoints/list.rs` — Reference for route registration and response serialization
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Contains the router setup pattern to follow for adding the new route
- `common/src/error.rs::AppError` — Error type for endpoint error responses
- `tests/api/sbom.rs` — Existing SBOM integration tests; follow the same test setup and assertion patterns

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns `200 OK` with `SbomComparisonResult` JSON
- [ ] Missing `left` or `right` query parameter returns `400 Bad Request`
- [ ] Non-existent SBOM ID returns `404 Not Found`
- [ ] Response JSON matches the expected shape with all six diff category arrays
- [ ] Endpoint responds within p95 < 1s for SBOMs with up to 2000 packages each

## Test Requirements
- [ ] Integration test: valid comparison returns 200 with correct diff structure
- [ ] Integration test: missing query parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: comparing identical SBOMs returns empty diff arrays
- [ ] Integration test: comparison with added/removed packages returns correct categorization

## Verification Commands
- `cargo test --test sbom_compare` — All comparison endpoint integration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison models and diff service
