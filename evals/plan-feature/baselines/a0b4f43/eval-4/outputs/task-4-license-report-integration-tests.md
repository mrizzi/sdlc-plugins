## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint. The tests verify the end-to-end flow: ingesting an SBOM with packages that have various licenses, configuring a license policy, calling the report endpoint, and validating the response structure, grouping logic, compliance flags, and transitive dependency inclusion. Tests follow the existing integration test patterns in `tests/api/`.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for the license report endpoint

## Files to Modify
- `tests/Cargo.toml` — Add the license_report test module if test modules are registered explicitly

## Implementation Notes
- Follow the integration test pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.
- Test setup should:
  1. Ingest a test SBOM with known packages and licenses (use the existing ingestion test patterns)
  2. Place a test license policy JSON file (or configure the policy path for the test)
  3. Call `GET /api/v2/sbom/{id}/license-report` against the test server
  4. Validate the response
- Test scenarios to cover:
  - Happy path: SBOM with multiple licenses, all compliant
  - Policy violation: SBOM with a denied license, verify `compliant: false` and `policy_violations` count
  - Transitive dependencies: Verify that indirect dependency licenses appear in the report
  - Empty SBOM: SBOM with no packages returns an empty groups array
  - Non-existent SBOM: Returns 404
- Automated compliance gate test: Verify that the response structure supports CI/CD pipeline integration (the `policy_violations` field is present and is a number, enabling pipeline `if violations > 0 then fail` logic)
- Per `docs/constraints.md` §5 (Code Change Rules): Changes must be scoped to the files listed. Code must not duplicate existing functionality.
- Per `docs/constraints.md` §2 (Commit Rules): Every commit must reference TC-9004 in the footer, follow Conventional Commits, and include `--trailer="Assisted-by: Claude Code"`.
- Per `docs/constraints.md` §3 (PR Rules): The branch must be named after the Jira issue ID, and PR link must be posted to Jira after opening.

## Reuse Candidates
- `tests/api/sbom.rs` — Existing SBOM integration tests; follow the same test setup, server initialization, and assertion patterns
- `tests/api/advisory.rs` — Existing advisory integration tests; follow the same pattern for test database setup and HTTP request helpers

## Acceptance Criteria
- [ ] Integration tests cover the happy path (compliant SBOM), policy violation path, transitive dependency inclusion, empty SBOM, and non-existent SBOM cases
- [ ] All tests pass against a PostgreSQL test database
- [ ] Tests validate both the HTTP status codes and the response body structure
- [ ] Tests verify the `policy_violations` count matches the number of non-compliant groups

## Test Requirements
- [ ] Integration test: Happy path — SBOM with only allowed licenses returns 200 with all groups `compliant: true` and `policy_violations: 0`
- [ ] Integration test: Policy violation — SBOM with a denied license returns 200 with the denied group `compliant: false` and `policy_violations >= 1`
- [ ] Integration test: Transitive dependencies — indirect dependency licenses appear in the report groups
- [ ] Integration test: Empty SBOM — returns 200 with an empty `groups` array
- [ ] Integration test: Non-existent SBOM — returns 404

## Verification Commands
- `cargo test --test api -- license_report` — All license report integration tests pass

## Dependencies
- Depends on: Task 3 — License report endpoint (provides the endpoint under test)
