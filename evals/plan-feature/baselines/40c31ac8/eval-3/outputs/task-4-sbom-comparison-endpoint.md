## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare` endpoint that accepts `left` and `right` query parameters (SBOM IDs) and returns the structured diff computed by `SbomCompareService`. Also add integration tests that verify the endpoint against a real PostgreSQL test database.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- register the new `/compare` route alongside existing SBOM routes

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` -- handler function `compare_sboms(Query<CompareParams>, State<AppState>) -> Result<Json<SbomComparison>, AppError>` with `CompareParams { left: String, right: String }`
- `tests/api/sbom_compare.rs` -- integration tests for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` -- NEW: returns `SbomComparison` JSON with added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler structure, error handling, and response wrapping.
- Extract `left` and `right` SBOM IDs from query parameters. Return `AppError::BadRequest` if either parameter is missing.
- Return `AppError::NotFound` if either SBOM ID does not exist, following the pattern in `endpoints/get.rs`.
- Call `SbomCompareService::compare(left_id, right_id, &db)` from Task 3 to compute the diff.
- Register the route in `endpoints/mod.rs` using the same `Router` builder pattern as `list.rs` and `get.rs`.
- Per CONVENTIONS.md §Error Handling: wrap all fallible operations with `.context()` and return `Result<T, AppError>`. Applies: task modifies `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's `.rs` scope.
- Per CONVENTIONS.md §Test Patterns: integration tests hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task creates `tests/api/sbom_compare.rs` matching the convention's `.rs` test file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- follow this handler's pattern for extracting path/query params and returning JSON
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- route registration pattern to follow
- `common/src/error.rs::AppError` -- use `AppError::BadRequest` for missing params, `AppError::NotFound` for invalid SBOM IDs
- `modules/fundamental/src/sbom/service/compare.rs::SbomCompareService` -- the service created in Task 3; call its `compare()` method

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparison` JSON
- [ ] Returns 400 when `left` or `right` query parameter is missing
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Response p95 latency < 1s for SBOMs with up to 2000 packages each
- [ ] Route is registered under the existing `/api/v2/sbom` prefix

## Test Requirements
- [ ] Integration test: compare two SBOMs with known package differences, verify added_packages and removed_packages in response
- [ ] Integration test: compare two SBOMs with version changes, verify version_changes array with correct direction
- [ ] Integration test: request with missing `left` param returns 400
- [ ] Integration test: request with non-existent SBOM ID returns 404
- [ ] Integration test: compare two identical SBOMs returns all-empty diff sections

## Verification Commands
- `cargo test -p tests -- api::sbom_compare` -- all comparison endpoint integration tests pass
- `cargo check --workspace` -- no compilation errors across the workspace

## Dependencies
- Depends on: Task 1 -- Create feature branch (trustify-backend)
- Depends on: Task 3 -- Add SBOM comparison model types and diff service

## Additional Fields
- priority: Critical
- fixVersions: RHTPA 1.5.0
- labels: ai-generated-jira
