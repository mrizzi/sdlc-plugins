## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint. Tests should cover the happy path (correct license grouping), non-compliant license detection, transitive dependency inclusion, edge cases (empty SBOM, missing SBOM), and the automated compliance gate use case (CI/CD pipeline checking for `compliant: false`).

## Files to Create
- `tests/api/license_report.rs` — integration tests for the `GET /api/v2/sbom/{id}/license-report` endpoint

## Files to Modify
- `tests/Cargo.toml` — add test module reference if needed for the new test file

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs` for test structure, database setup, and assertion style.
- Tests should hit a real PostgreSQL test database per the project's testing convention.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern established in the existing test files.
- Test scenarios to implement:
  1. **Happy path**: ingest an SBOM with packages having known licenses (e.g., MIT, Apache-2.0), call the license report endpoint, verify packages are correctly grouped by license.
  2. **Non-compliant licenses**: configure a policy that denies GPL-3.0, ingest an SBOM with a GPL-3.0 package, verify the report flags the group as `compliant: false`.
  3. **Transitive dependencies**: ingest an SBOM where package A depends on package B (transitive), verify both appear in the license report.
  4. **Empty SBOM**: ingest an SBOM with no packages, verify the report returns an empty `groups` array.
  5. **Non-existent SBOM**: call the endpoint with a non-existent ID, verify 404 response.
  6. **Compliance gate**: verify the response shape supports a CI/CD pipeline checking `groups[].compliant` to detect violations.
- Per CONVENTIONS.md Key Conventions (Testing): integration tests live in `tests/api/` and use a real PostgreSQL test database with `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task creates `tests/api/license_report.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM integration tests; follow the same test structure, database setup, and HTTP client patterns
- `tests/api/advisory.rs` — existing advisory integration tests; reference for assertion patterns and test organization
- `tests/api/search.rs` — existing search integration tests; reference for additional test patterns

## Acceptance Criteria
- [ ] All six test scenarios pass against a PostgreSQL test database
- [ ] Tests verify the response JSON shape matches the API contract (`{ groups: [{ license, packages, compliant }] }`)
- [ ] Tests verify transitive dependency inclusion
- [ ] Tests verify policy-based compliance flagging
- [ ] Tests cover both success (200) and error (404) response codes
- [ ] No test relies on hardcoded database state — each test sets up its own data

## Test Requirements
- [ ] Integration test: happy path — SBOM with MIT and Apache-2.0 packages returns two license groups
- [ ] Integration test: non-compliant — policy denying GPL-3.0 flags the group as non-compliant
- [ ] Integration test: transitive dependencies — packages from the full dependency tree appear in the report
- [ ] Integration test: empty SBOM — returns empty groups array with 200 status
- [ ] Integration test: non-existent SBOM — returns 404 status
- [ ] Integration test: compliance gate — response shape supports programmatic compliance checking

## Verification Commands
- `cargo test --test api license_report` — all tests pass
- `cargo test --test api license_report -- --nocapture` — view test output for debugging

## Dependencies
- Depends on: Task 2 — Add license report service and endpoint
