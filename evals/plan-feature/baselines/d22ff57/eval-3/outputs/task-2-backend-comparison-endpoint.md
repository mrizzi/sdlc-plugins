# Task 2 — Backend: Add SBOM comparison endpoint and integration tests

## Repository
trustify-backend

## Description
Wire the SBOM comparison service method (from Task 1) to a new HTTP endpoint at `GET /api/v2/sbom/compare?left={id1}&right={id2}`. Register the route in the SBOM endpoints module and add integration tests that validate the endpoint end-to-end against a real PostgreSQL test database.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/compare` route alongside existing SBOM routes

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — handler for `GET /api/v2/sbom/compare`
- `tests/api/sbom_compare.rs` — integration tests for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns structured diff as JSON with fields: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`

## Implementation Notes
- Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs` — extract query parameters, call the service, return JSON response.
- The handler should parse `left` and `right` query parameters as SBOM IDs (likely UUIDs or i64 depending on the entity definition in `entity/src/sbom.rs`).
- Return `Result<Json<SbomComparisonResult>, AppError>` to match the existing error handling pattern.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` — follow the existing route registration pattern (likely `Router::new().route(...)` in an Axum router builder).
- Integration tests should follow the pattern in `tests/api/sbom.rs` — set up test data (ingest two SBOMs with known packages and advisories), call the endpoint, and assert the response contains the expected diff.
- Per constraints.md Section 2 (Commit Rules): commit messages must follow Conventional Commits, reference Jira issue ID in footer, and include `--trailer="Assisted-by: Claude Code"`.
- Per constraints.md Section 3 (PR Rules): branch must be named after the Jira issue ID.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference pattern for single-SBOM endpoint handler structure
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference pattern for query parameter extraction
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern
- `tests/api/sbom.rs` — existing SBOM integration tests; follow the same test setup and assertion patterns
- `common/src/error.rs::AppError` — error handling for invalid/missing SBOM IDs

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with structured diff JSON
- [ ] Returns 400 if `left` or `right` query parameter is missing
- [ ] Returns 404 if either SBOM ID does not exist
- [ ] Response JSON matches the expected shape: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`
- [ ] Route is registered and discoverable alongside existing SBOM routes

## Test Requirements
- [ ] Integration test: compare two SBOMs with known differences, verify all diff categories populated correctly
- [ ] Integration test: compare two identical SBOMs, verify empty diff arrays
- [ ] Integration test: request with missing `left` parameter returns 400
- [ ] Integration test: request with missing `right` parameter returns 400
- [ ] Integration test: request with non-existent left SBOM ID returns 404
- [ ] Integration test: request with non-existent right SBOM ID returns 404
- [ ] Integration test: verify response content-type is `application/json`

## Verification Commands
- `cargo test --test api sbom_compare` — all comparison endpoint integration tests pass
- `cargo build` — project compiles without errors

## Dependencies
- Depends on: Task 1 — Backend: Add SBOM comparison diff model and service
