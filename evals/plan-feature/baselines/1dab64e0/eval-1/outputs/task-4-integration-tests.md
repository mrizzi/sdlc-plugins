## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests should cover the success path with various advisory severity distributions, 404 for non-existent SBOMs, the threshold query parameter filtering, deduplication of advisories, and cache behavior. Tests hit a real PostgreSQL test database following the existing integration test patterns.

## Files to Create
- `tests/api/sbom_advisory_summary.rs` — integration tests for the advisory-summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add test module declaration for the new test file if required by the test harness

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs` for test setup, database fixtures, and assertion style.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code assertions.
- Set up test data with multiple advisories at different severity levels (Critical, High, Medium, Low) linked to an SBOM via the `sbom_advisory` join table.
- Include a test case with duplicate advisory links to verify deduplication.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task creates `tests/api/sbom_advisory_summary.rs` matching the convention's Rust syntax scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests; follow the same test setup, fixture creation, and assertion patterns
- `tests/api/advisory.rs` — existing advisory endpoint integration tests; reference for setting up advisory test data and linking advisories to SBOMs

## Acceptance Criteria
- [ ] All test cases pass against a real PostgreSQL test database
- [ ] Tests cover: success with mixed severities, 404 for missing SBOM, threshold filtering, zero-advisory SBOM, deduplication
- [ ] Tests follow existing integration test conventions and patterns

## Test Requirements
- [ ] Test GET /api/v2/sbom/{id}/advisory-summary returns correct counts for SBOM with advisories at Critical, High, Medium, and Low severities
- [ ] Test GET /api/v2/sbom/{id}/advisory-summary returns 404 for non-existent SBOM ID
- [ ] Test GET /api/v2/sbom/{id}/advisory-summary?threshold=critical returns only critical count
- [ ] Test GET /api/v2/sbom/{id}/advisory-summary?threshold=high returns critical and high counts
- [ ] Test GET /api/v2/sbom/{id}/advisory-summary returns all zeros for SBOM with no linked advisories
- [ ] Test that duplicate advisories (same advisory ID linked to SBOM multiple times) are deduplicated in counts

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching and threshold filter
