## additional_fields
```
{ "labels": ["ai-generated-jira"], "priority": {"name": "Critical"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }
```

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Create the REST endpoint `GET /api/v2/sbom/compare?left={id1}&right={id2}` that returns a structured diff between two SBOMs. The endpoint delegates to the comparison service (Task 3), validates query parameters, and returns the `SbomComparisonResult` as JSON. Add integration tests covering normal diff, empty diff, invalid SBOM IDs, and missing query parameters.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Axum handler for GET /api/v2/sbom/compare with left/right query parameter extraction and validation
- `tests/api/sbom_compare.rs` — Integration tests for the comparison endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the compare route alongside existing SBOM routes
- `tests/api/mod.rs` — Add `mod sbom_compare;` to include new test module (if test modules are registered this way)

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns `SbomComparisonResult` JSON with six diff categories (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)

## Implementation Notes
Create the endpoint handler following the existing patterns in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs`. The handler should:

1. Extract `left` and `right` query parameters (both required)
2. Return 400 Bad Request if either parameter is missing
3. Call `SbomComparisonService::compare(left, right)` from Task 3
4. Return the `SbomComparisonResult` as JSON with 200 OK
5. Return 404 Not Found if either SBOM ID does not exist (propagated from the service error)

Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` using the existing route registration pattern. The compare endpoint should be registered alongside the existing `/api/v2/sbom` routes.

Integration tests should follow the pattern in `tests/api/sbom.rs`:
- Test normal comparison between two SBOMs with known differences
- Test comparison of two identical SBOMs (empty diff)
- Test with invalid/non-existent SBOM IDs (expect 404)
- Test with missing query parameters (expect 400)
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern

Per CONVENTIONS.md §Endpoint registration: each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules. Register the compare route in the SBOM module's endpoint registration.
Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task creates `tests/api/sbom_compare.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Existing GET endpoint handler pattern; reference for query parameter extraction and response serialization
- `modules/fundamental/src/sbom/endpoints/list.rs` — Existing list endpoint; reference for route registration and handler structure
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern to follow
- `common/src/error.rs::AppError` — Standard error type for 400/404 responses
- `tests/api/sbom.rs` — Existing SBOM integration test patterns

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON
- [ ] Returns 400 Bad Request when `left` or `right` query parameter is missing
- [ ] Returns 404 Not Found when either SBOM ID does not exist
- [ ] Response JSON matches the expected shape with all six diff categories
- [ ] Endpoint is registered and accessible at the correct path
- [ ] Integration tests pass against a real PostgreSQL test database

## Test Requirements
- [ ] Integration test: compare two SBOMs with known package differences returns correct diff
- [ ] Integration test: compare two identical SBOMs returns 200 with all empty arrays
- [ ] Integration test: non-existent left SBOM ID returns 404
- [ ] Integration test: non-existent right SBOM ID returns 404
- [ ] Integration test: missing left query parameter returns 400
- [ ] Integration test: missing right query parameter returns 400
- [ ] Integration test: verify response JSON structure matches SbomComparisonResult schema

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Backend comparison model structs
- Depends on: Task 3 — Backend comparison service logic
