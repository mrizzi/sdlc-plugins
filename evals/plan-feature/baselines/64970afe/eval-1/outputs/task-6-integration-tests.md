## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests cover the full request lifecycle against a real PostgreSQL test database, validating response shape, severity counting, advisory deduplication, 404 handling, and threshold filtering. These tests provide the primary regression safety net for the advisory severity aggregation feature (TC-9001).

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for the advisory summary endpoint

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs` for test setup, database initialization, HTTP client configuration, and assertion style.
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code assertions, matching the convention used in existing test files.
- Set up test fixtures by inserting SBOMs and advisories with known severity levels into the test database, then linking them via the `sbom_advisory` join table.
- Include edge case tests: SBOM with zero advisories (all counts should be zero), SBOM with duplicate advisory links (verify deduplication yields correct counts), SBOM with advisories at every severity level.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database using `assert_eq!(resp.status(), StatusCode::OK)` pattern. See `tests/api/sbom.rs` for the established test structure and database setup.
  Applies: task creates `tests/api/advisory_summary.rs` matching the convention's tests/api/ directory scope.

## Reuse Candidates
- `tests/api/sbom.rs` — integration test structure, fixture setup, and assertion patterns for SBOM endpoints
- `tests/api/advisory.rs` — integration test structure for advisory endpoints, including advisory fixture creation

## Acceptance Criteria
- [ ] Tests cover successful 200 response with correct severity counts
- [ ] Tests cover 404 response for non-existent SBOM ID
- [ ] Tests cover advisory deduplication (same advisory linked multiple times counted once)
- [ ] Tests cover SBOM with no linked advisories (zero counts)
- [ ] Tests cover threshold query parameter filtering (critical, high, medium, low, invalid)
- [ ] All tests pass against a real PostgreSQL test database

## Test Requirements
- [ ] Test: `GET /api/v2/sbom/{test-id}/advisory-summary` with known fixture data returns expected severity counts
- [ ] Test: `GET /api/v2/sbom/{nonexistent-id}/advisory-summary` returns 404
- [ ] Test: SBOM with duplicate advisory links returns deduplicated counts
- [ ] Test: SBOM with zero advisories returns `{ "critical": 0, "high": 0, "medium": 0, "low": 0, "total": 0 }`
- [ ] Test: `?threshold=critical` returns only critical count with others zeroed
- [ ] Test: `?threshold=invalid` returns 400 Bad Request

## Verification Commands
- `cargo test --test api advisory_summary` — expected: all tests pass

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
