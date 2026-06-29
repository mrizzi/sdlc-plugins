## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license report endpoint. Tests should validate the full request-response cycle against a real PostgreSQL test database, covering happy path, error cases, compliance policy evaluation, and transitive dependency inclusion.

## Jira Metadata
- **Priority**: Major
- **Fix Versions**: RHTPA 1.5.0

## Files to Create
- `tests/api/license_report.rs` — Integration tests for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `tests/Cargo.toml` — Add test file to the test suite if required by the project's test configuration

## Implementation Notes
Follow the existing integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs`:

1. Set up test fixtures: ingest a test SBOM with known packages and license data using the existing ingestion infrastructure.
2. Include packages with a mix of allowed licenses (MIT, Apache-2.0), denied licenses (GPL-3.0), and unlisted licenses to test all policy evaluation paths.
3. Include at least one transitive dependency chain to verify transitive resolution.
4. Use `assert_eq!(resp.status(), StatusCode::OK)` pattern per project conventions.
5. Deserialize the response body into `LicenseReport` and assert on group counts, compliance flags, and summary statistics.

Test cases to implement:
- Happy path with mixed licenses (some compliant, some not)
- SBOM with all compliant licenses (100% clean report)
- SBOM with no packages (empty groups)
- Non-existent SBOM ID returns 404
- Transitive dependencies are marked correctly
- Summary statistics match group data

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task creates `tests/api/license_report.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — Test setup patterns, fixture ingestion, HTTP client configuration
- `tests/api/advisory.rs` — Additional test pattern reference for response deserialization and assertion
- `tests/api/search.rs` — Test helper patterns

## Acceptance Criteria
- [ ] All integration tests pass against the PostgreSQL test database
- [ ] Tests cover compliant, non-compliant, and mixed-license SBOMs
- [ ] Tests verify transitive dependency marking
- [ ] Tests verify 404 response for non-existent SBOM IDs
- [ ] Tests verify summary statistics accuracy
- [ ] Test fixtures include realistic license combinations

## Test Requirements
- [ ] Integration test: happy path — SBOM with MIT, Apache-2.0, and GPL-3.0 packages returns correct compliance flags per group
- [ ] Integration test: all-compliant SBOM returns all groups with `compliant: true`
- [ ] Integration test: empty SBOM (no packages) returns 200 with empty groups array
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: transitive dependencies appear in report with `transitive: true` flag
- [ ] Integration test: summary statistics (total_packages, compliant_count, non_compliant_count) are correct

## Dependencies
- Depends on: Task 3 — Add license report endpoint and route registration

[sdlc-workflow] Description digest: sha256-md:516a6165a7f6dbe55b9e6873845791e589aa46d43de407812b9efe85517a984c
