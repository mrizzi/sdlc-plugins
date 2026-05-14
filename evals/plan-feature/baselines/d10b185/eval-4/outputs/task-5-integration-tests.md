# Task 5 — Add integration tests for license report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the `GET /api/v2/sbom/{id}/license-report` endpoint. Tests should cover the full request-response cycle against a real PostgreSQL test database, validating the response shape, compliance logic, and error handling. This follows the established integration test pattern in the `tests/api/` directory.

## Files to Create
- `tests/api/license_report.rs` — integration tests for the license report endpoint

## Files to Modify
- `tests/Cargo.toml` — add any necessary test dependencies (if not already present)

## Implementation Notes
- Follow the integration test pattern from `tests/api/sbom.rs` — it demonstrates:
  - Setting up test fixtures (ingesting an SBOM with known package/license data)
  - Making HTTP requests to the API endpoint
  - Asserting response status codes with `assert_eq!(resp.status(), StatusCode::OK)`
  - Deserializing and validating response bodies
- Test data setup should:
  1. Ingest a test SBOM with packages that have known licenses (e.g., MIT, Apache-2.0, GPL-3.0-only)
  2. Set up a test license policy (or use the default `config/license-policy.json`)
  3. Call the license report endpoint and validate the grouped output
- Use the existing test database infrastructure — integration tests in `tests/api/` hit a real PostgreSQL test database per the repo conventions.
- Per constraints doc section 5.2: inspect existing test code in `tests/api/sbom.rs` and `tests/api/advisory.rs` before writing new tests.
- Per constraints doc section 5.9: prefer parameterized tests when multiple test cases exercise the same behavior with different inputs.
- Per constraints doc section 5.11: add a doc comment to every test function.
- Per constraints doc section 5.12: add given-when-then inline comments to non-trivial test functions.

## Reuse Candidates
- `tests/api/sbom.rs` — demonstrates SBOM endpoint integration test patterns including fixture setup and assertions
- `tests/api/advisory.rs` — demonstrates advisory endpoint integration test patterns; useful reference for error case testing
- `tests/api/search.rs` — demonstrates search endpoint testing patterns

## Acceptance Criteria
- [ ] Integration test: calling the endpoint for an SBOM with all-compliant licenses returns 200 with all groups marked `compliant: true`
- [ ] Integration test: calling the endpoint for an SBOM with a denied license returns 200 with that group marked `compliant: false`
- [ ] Integration test: calling the endpoint for a non-existent SBOM ID returns 404
- [ ] Integration test: response shape validation — `groups` array contains `license`, `packages`, and `compliant` fields
- [ ] Integration test: verify packages are correctly grouped by license (same license in one group)
- [ ] All tests pass (`cargo test --test api`)

## Test Requirements
- [ ] At least 5 integration test cases covering: all-compliant, mixed-compliance, all-non-compliant, non-existent SBOM, and response shape validation
- [ ] Tests use the established PostgreSQL test database pattern from `tests/api/`
- [ ] Each test function has a doc comment explaining what it tests
- [ ] Non-trivial tests include given-when-then inline comments

## Dependencies
- Depends on: Task 4 — Add GET /api/v2/sbom/{id}/license-report endpoint
