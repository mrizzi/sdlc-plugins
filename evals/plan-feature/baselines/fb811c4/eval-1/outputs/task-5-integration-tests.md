## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering the happy path, 404 for non-existent SBOMs, threshold filtering, severity deduplication, and cache behavior. These tests validate the full request-response cycle against a real PostgreSQL test database.

## Files to Modify
- `tests/api/sbom.rs` — Add integration test functions for the advisory-summary endpoint

## Implementation Notes
1. **Test location**: Add tests to `tests/api/sbom.rs` alongside the existing SBOM endpoint integration tests. Follow the test patterns already established in that file, including test database setup and teardown.

2. **Test cases to implement**:

   - `test_advisory_summary_returns_counts`: Seed an SBOM with advisories at different severity levels (2 critical, 3 high, 1 medium, 0 low). Call `GET /api/v2/sbom/{id}/advisory-summary`. Assert response status is 200 and body matches `{ critical: 2, high: 3, medium: 1, low: 0, total: 6 }`.

   - `test_advisory_summary_not_found`: Call `GET /api/v2/sbom/{nonexistent-uuid}/advisory-summary`. Assert response status is 404.

   - `test_advisory_summary_deduplication`: Seed an SBOM where the same advisory is linked twice (e.g., through different vulnerability paths). Assert the advisory is counted only once in the total.

   - `test_advisory_summary_threshold_filter`: Seed an SBOM with advisories at all severity levels. Call `GET /api/v2/sbom/{id}/advisory-summary?threshold=high`. Assert only critical and high counts are non-zero; medium and low are 0.

   - `test_advisory_summary_empty_sbom`: Seed an SBOM with no linked advisories. Assert all counts are 0 and total is 0.

3. **Assertion pattern**: Use `assert_eq!(resp.status(), StatusCode::OK)` and deserialize the response body into `AdvisorySeveritySummary` for field-level assertions, following the pattern in `tests/api/advisory.rs`.

4. **Test data setup**: Use the same test fixtures and seeding helpers used by existing tests in `tests/api/sbom.rs`. Create advisories with explicit severity values and link them to the test SBOM via the `sbom_advisory` entity from `entity/src/sbom_advisory.rs`.

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task modifies `tests/api/sbom.rs` matching the convention's integration test scope.

## Test Requirements
- [ ] Test that valid SBOM returns correct severity counts (200 response)
- [ ] Test that non-existent SBOM returns 404
- [ ] Test that duplicate advisories are counted only once
- [ ] Test that threshold parameter filters severity levels correctly
- [ ] Test that SBOM with no advisories returns all-zero counts

## Acceptance Criteria
- [ ] All five test cases pass against the test database
- [ ] Tests follow existing patterns in `tests/api/sbom.rs`
- [ ] No test relies on hardcoded IDs or external state

## Verification Commands
- `cargo test -p trustify-tests --test sbom` — all advisory-summary tests pass

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint

[sdlc-workflow] Description digest: sha256-md:5f2d6e77052fbf7ddfe5c14325a8d41ec2f5df0f3ecbb9ae186ea6c1d5576c4b
