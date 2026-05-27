# Task 5 — Add integration tests for SBOM comparison endpoint

**Summary:** Add integration tests for SBOM comparison endpoint

**Labels:** ai-generated-jira

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/compare` endpoint, covering the full request-response cycle against a test database. Tests should verify the comparison produces correct diffs for various scenarios including added/removed packages, version changes, vulnerability changes, and license changes.

## Files to Create
- `tests/api/sbom_compare.rs` — integration tests for the comparison endpoint

## Files to Modify
- `tests/api/mod.rs` — if a test module registry exists, add `mod sbom_compare;` (check existing test structure first)

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` — tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Test setup should:
  1. Ingest two SBOMs with known package/advisory differences using the existing ingestion infrastructure
  2. Call `GET /api/v2/sbom/compare?left={id1}&right={id2}`
  3. Deserialize the response and verify each diff category
- Test scenarios:
  - Two SBOMs with no differences (empty diff)
  - SBOM with added packages only
  - SBOM with removed packages only
  - SBOM with version changes (both upgrade and downgrade)
  - SBOM with new vulnerabilities (including a critical severity one)
  - SBOM with resolved vulnerabilities
  - SBOM with license changes
  - Combined scenario with multiple diff categories
  - Error cases: missing params, non-existent IDs
- Per non-functional requirements: include a performance-oriented test with larger data sets (if feasible in test environment) to validate p95 < 1s for SBOMs with up to 2000 packages.

## Reuse Candidates
- `tests/api/sbom.rs` — reference for SBOM endpoint integration test patterns, test setup, and assertion style
- `tests/api/advisory.rs` — reference for advisory-related test setup

## Acceptance Criteria
- [ ] Integration tests cover all major diff categories (added, removed, version changes, vulnerabilities, license changes)
- [ ] Error cases are tested (missing params return 400, non-existent IDs return 404)
- [ ] Tests follow the existing test patterns in `tests/api/sbom.rs`
- [ ] All tests pass against the test database

## Test Requirements
- [ ] All test scenarios listed in Implementation Notes are covered
- [ ] Tests use descriptive doc comments explaining each scenario
- [ ] Tests verify response status codes and response body structure

## Verification Commands
- `cargo test --test api sbom_compare` — expected: all comparison integration tests pass

## Dependencies
- Depends on: Task 4 — Add GET /api/v2/sbom/compare endpoint
