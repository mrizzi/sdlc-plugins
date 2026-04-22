## Repository
trustify-backend

## Description
Add integration tests for the SBOM comparison endpoint. Tests exercise the full HTTP flow against a real PostgreSQL test database, verifying correct diff computation, error handling, and response shape for various scenarios.

## Files to Create
- `tests/api/sbom_compare.rs` — Integration tests for `GET /api/v2/sbom/compare`

## Files to Modify
- `tests/api/mod.rs` — Register the new `sbom_compare` test module (if a mod.rs exists; otherwise the test runner picks it up automatically)

## Implementation Notes
- Follow the integration test pattern in `tests/api/sbom.rs` — set up test data by ingesting two SBOMs with known packages and advisories, then call the comparison endpoint and assert the response.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in existing tests.
- Test scenarios should include:
  1. Two SBOMs with overlapping but different package sets (tests added, removed, version changes).
  2. Two SBOMs where one has an advisory the other does not (tests new/resolved vulnerabilities).
  3. Two SBOMs where a package's license changed.
  4. Missing query parameter returns 400.
  5. Nonexistent SBOM ID returns 404.
  6. Two identical SBOMs return empty diff arrays.
- Deserialize response body into `SbomComparison` to assert field values, not just status code.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM integration test patterns, test setup helpers, SBOM ingestion fixtures
- `tests/api/advisory.rs` — advisory test data setup patterns

## Acceptance Criteria
- [ ] All integration test scenarios pass against the test database
- [ ] Tests cover: normal diff, empty diff, missing params (400), nonexistent SBOM (404)
- [ ] Tests validate response body structure and field values, not just status codes

## Test Requirements
- [ ] At least 6 test cases covering the scenarios listed above
- [ ] Tests are self-contained — each test sets up its own data

## Verification Commands
- `cargo test -p trustify-tests sbom_compare` — all comparison integration tests pass

## Dependencies
- Depends on: Task 2 — Backend comparison service and endpoint
