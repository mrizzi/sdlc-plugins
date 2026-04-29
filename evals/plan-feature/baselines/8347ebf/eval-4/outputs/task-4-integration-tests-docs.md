# Task 4 — Add integration tests and documentation for license compliance report

## Repository
trustify-backend

## Description
Add comprehensive integration tests for the license report endpoint covering edge cases, and document the license policy configuration format and the new endpoint for users and operators.

## Files to Modify
- `README.md` — add a section describing the license compliance report feature and link to detailed documentation

## Files to Create
- `tests/api/license_report.rs` — integration tests for the license report endpoint
- `docs/license-policy.md` — documentation for the license policy configuration format (if a `docs/` directory exists; otherwise at repository root)

## Implementation Notes
- **Integration tests** — follow the pattern in `tests/api/sbom.rs`:
  - Use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern
  - Set up test data: create an SBOM with known packages and license mappings, configure a known policy
  - Test cases should cover:
    - SBOM with all compliant licenses returns `compliant: true` for every group
    - SBOM with mixed compliant and non-compliant licenses returns correct flags per group
    - SBOM with transitive dependencies includes those packages in the report
    - SBOM with zero packages returns an empty `groups` array
    - Non-existent SBOM ID returns 404
    - Large SBOM (near 1000 packages boundary) completes within acceptable time
  - Ensure the test module is included in `tests/` (check `Cargo.toml` or test runner configuration)
- **Documentation** — document:
  - The `license-policy.json` configuration format with example
  - How to customize allowed/denied license lists
  - The endpoint URL, HTTP method, request parameters, and response shape
  - Example `curl` commands for calling the endpoint
  - How to integrate with CI/CD pipelines (reference UC-2 from the feature)

## Reuse Candidates
- `tests/api/sbom.rs` — follow this test file's structure, setup, and assertion patterns
- `tests/api/advisory.rs` — additional reference for integration test patterns

## Acceptance Criteria
- [ ] Integration tests pass against a PostgreSQL test database
- [ ] All edge cases listed above are covered by tests
- [ ] License policy documentation clearly explains the configuration format
- [ ] Endpoint documentation includes request/response examples

## Test Requirements
- [ ] Integration test: SBOM with all compliant licenses
- [ ] Integration test: SBOM with non-compliant licenses
- [ ] Integration test: SBOM with transitive dependencies
- [ ] Integration test: empty SBOM (no packages)
- [ ] Integration test: non-existent SBOM returns 404

## Documentation Updates
- `README.md` — add section about the license compliance report feature
- `docs/license-policy.md` (new) — full documentation of the license policy configuration format, endpoint usage, and CI/CD integration guidance

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint
