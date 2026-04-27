# Task 5 — Add Integration Tests for Advisory-Summary Endpoint

## Repository
trustify-backend

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering the main success path, error cases, deduplication, threshold filtering, and caching behavior. These tests validate the end-to-end flow from HTTP request through to database aggregation and JSON response.

## Files to Create
- `tests/api/sbom_advisory_summary.rs` — integration test file for the advisory-summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add any necessary test dependencies if not already present

## Implementation Notes
- Follow the integration test patterns established in `tests/api/sbom.rs` and `tests/api/advisory.rs`:
  - Tests hit a real PostgreSQL test database
  - Use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern
  - Set up test data by ingesting SBOMs and advisories through the service layer or test fixtures
- Test scenarios to cover:
  1. **Happy path**: SBOM with advisories at multiple severity levels returns correct counts
  2. **Empty advisories**: SBOM with no linked advisories returns all zeros
  3. **404 case**: Non-existent SBOM ID returns 404
  4. **Deduplication**: Same advisory linked multiple times to an SBOM counts only once
  5. **Threshold filtering**: `?threshold=critical` returns only critical count; `?threshold=high` returns critical and high
  6. **Response schema**: JSON response has exactly the fields `critical`, `high`, `medium`, `low`, `total`
- Per constraints doc section 5.11: add a doc comment to every test function.
- Per constraints doc section 5.12: add given-when-then inline comments to non-trivial test functions.
- Per constraints doc section 5.9: consider parameterized tests for threshold filtering scenarios if the project's testing patterns support it (check sibling test files first per constraint 5.10).

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests; pattern reference for test setup, assertions, and test database usage
- `tests/api/advisory.rs` — existing advisory endpoint integration tests; reference for advisory test data setup
- `modules/fundamental/src/sbom/model/advisory_summary.rs::AdvisorySeveritySummary` — response struct for deserialization in test assertions

## Acceptance Criteria
- [ ] All integration tests pass (`cargo test`)
- [ ] Tests cover: happy path, empty advisories, 404, deduplication, threshold filtering, response schema
- [ ] Tests use the established test patterns from sibling test files
- [ ] Each test function has a doc comment
- [ ] Non-trivial tests have given-when-then inline comments

## Test Requirements
- [ ] Integration test: SBOM with 3 critical, 2 high, 1 medium, 0 low advisories returns `{ critical: 3, high: 2, medium: 1, low: 0, total: 6 }`
- [ ] Integration test: SBOM with no advisories returns `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`
- [ ] Integration test: non-existent SBOM ID returns HTTP 404
- [ ] Integration test: duplicate advisory links are deduplicated in the count
- [ ] Integration test: `?threshold=critical` returns only critical count with other severities zeroed
- [ ] Integration test: `?threshold=high` returns critical and high counts with medium and low zeroed
- [ ] Integration test: response JSON contains exactly the expected fields

## Verification Commands
- `cargo test --test api -- sbom_advisory_summary` — run all advisory-summary integration tests
- `cargo test --test api -- sbom_advisory_summary --nocapture` — run with output for debugging

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary Endpoint
