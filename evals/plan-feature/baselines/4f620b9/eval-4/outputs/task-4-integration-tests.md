# Task 4 — Add integration tests for the license report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/license-report` endpoint. Tests should cover the full request-response cycle against a real PostgreSQL test database, validating response structure, compliance evaluation, edge cases, and performance characteristics.

## Files to Modify
- `tests/Cargo.toml` — add any necessary test dependencies

## Files to Create
- `tests/api/license_report.rs` — integration tests for the license report endpoint covering happy path, error cases, edge cases, and compliance scenarios

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` — it demonstrates the test setup (database provisioning, HTTP client configuration) and assertion patterns (`assert_eq!(resp.status(), StatusCode::OK)`) used throughout the test suite.
- Test scenarios should include:
  - An SBOM with packages having only approved licenses (all groups `compliant: true`)
  - An SBOM with packages having denied licenses (at least one group `compliant: false`)
  - An SBOM with packages having licenses not in any policy list (grouped under "Unknown")
  - An SBOM with no packages (empty groups array)
  - A request for a non-existent SBOM ID (404 response)
  - An SBOM with transitive dependencies to verify they are included in the report
- Per constraints doc section 2 (Commit Rules): use Conventional Commits format, reference TC-9004 in the footer, and include `--trailer="Assisted-by: Claude Code"`.
- Per constraints doc section 5 (Code Change Rules): scope changes to listed files; inspect existing test code before writing new tests.
- Per constraints doc section 5.9-5.10: prefer parameterized tests when multiple test cases exercise the same behavior with different inputs, but only if the existing test suite uses parameterized patterns.
- Per constraints doc section 5.11-5.13: add doc comments to every test function; use given-when-then inline comments for non-trivial tests.

## Reuse Candidates
- `tests/api/sbom.rs` — follow the same test setup, HTTP client configuration, and assertion patterns
- `tests/api/advisory.rs` — additional reference for integration test structure and database seeding

## Acceptance Criteria
- [ ] All integration tests pass against the PostgreSQL test database
- [ ] Tests cover happy path (compliant SBOM), violation detection (non-compliant licenses), and edge cases (empty SBOM, unknown licenses, non-existent SBOM)
- [ ] Test assertions validate both the HTTP status code and the response body structure

## Test Requirements
- [ ] Integration test: SBOM with only approved licenses returns all groups as compliant
- [ ] Integration test: SBOM with denied licenses returns the relevant groups as non-compliant
- [ ] Integration test: SBOM with unknown licenses includes an "Unknown" license group
- [ ] Integration test: empty SBOM returns 200 with empty groups
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: transitive dependencies are included in the license report

## Verification Commands
- `cargo test --test api -- license_report` — run all license report integration tests
- `cargo test --test api -- license_report -- --nocapture` — run with output for debugging

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint

[sdlc-workflow] Description digest: sha256-md:dced98545977103ddc6ed24b3f65801f527fe7f44534101c4c8a58ae8bd084c1
