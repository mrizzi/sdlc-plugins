# Task 3 — Add SBOM comparison REST endpoint

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint that accepts two SBOM IDs as query parameters, invokes the comparison service created in Task 2, and returns the structured diff as a JSON response. The endpoint follows the existing Axum handler pattern used by other SBOM endpoints.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Axum handler for the comparison endpoint with query parameter extraction and response serialization

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — add route registration for `GET /compare` under the `/api/v2/sbom` prefix
- `tests/api/sbom.rs` — add integration tests for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: accepts two SBOM IDs as query parameters, returns `SbomComparisonResult` JSON with fields: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/`: see `list.rs` and `get.rs` for the handler structure.
- Route registration follows the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` — add the new route alongside existing SBOM routes.
- Use Axum `Query` extractor for the `left` and `right` query parameters. Define a `CompareQuery` struct with `left: String` and `right: String` fields.
- The handler should:
  1. Extract `left` and `right` SBOM IDs from query parameters
  2. Validate both IDs are present (return 400 Bad Request if missing)
  3. Call `SbomComparisonService` (from Task 2) to compute the diff
  4. Return 404 if either SBOM ID does not exist
  5. Return 200 with the `SbomComparisonResult` serialized as JSON
- Error handling: return `Result<Json<SbomComparisonResult>, AppError>` using the `AppError` pattern from `common/src/error.rs`.
- Integration tests should follow the pattern in `tests/api/sbom.rs` — hit a real PostgreSQL test database, assert response status and body shape.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing SBOM get handler demonstrating the Axum handler pattern, error handling, and response structure
- `modules/fundamental/src/sbom/endpoints/list.rs` — existing SBOM list handler showing query parameter extraction
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow
- `common/src/error.rs::AppError` — error type for endpoint error handling

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with the structured diff JSON
- [ ] Response JSON shape matches: `{ added_packages: [...], removed_packages: [...], version_changes: [...], new_vulnerabilities: [...], resolved_vulnerabilities: [...], license_changes: [...] }`
- [ ] Returns 400 when `left` or `right` query parameter is missing
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Endpoint is registered under the `/api/v2/sbom` route prefix
- [ ] Response time p95 < 1s for SBOMs with up to 2000 packages each

## Test Requirements
- [ ] Integration test: compare two valid SBOMs returns 200 with correct diff structure
- [ ] Integration test: compare with a non-existent SBOM ID returns 404
- [ ] Integration test: compare with missing query parameters returns 400
- [ ] Integration test: compare two identical SBOMs returns 200 with all empty arrays
- [ ] Integration test: compare two SBOMs with known differences verifies correct added/removed/changed counts

## Verification Commands
- `cargo test --test api sbom::compare` — all comparison endpoint integration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison diff model and service
