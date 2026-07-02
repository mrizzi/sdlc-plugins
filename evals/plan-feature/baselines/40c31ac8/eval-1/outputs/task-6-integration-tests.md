## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering the core scenarios: valid SBOM with mixed-severity advisories, non-existent SBOM, empty advisory set, threshold filtering, advisory deduplication, and cache header verification. These tests exercise the full request path against a real PostgreSQL test database.

## Files to Create
- `tests/api/sbom_advisory_summary.rs` — Integration test module for the advisory-summary endpoint

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` for test setup: database fixture creation, HTTP client initialization, request building, and response assertion structure.
- Set up test fixtures by creating an SBOM entity, creating advisory entities with different severity levels (Critical, High, Medium, Low), and linking them via `sbom_advisory` join records using the entities in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/sbom_advisory.rs`.
- Test deduplication by inserting duplicate `sbom_advisory` links for the same advisory and verifying counts are not inflated.
- Test threshold filtering by calling the endpoint with `?threshold=critical`, `?threshold=high`, etc. and verifying only the expected severity levels have non-zero counts.
- Reference assertion patterns in `tests/api/advisory.rs` for creating advisory fixtures with specific severity values.
- Per CONVENTIONS.md §Error Handling: return Result<T, AppError> with .context() wrapping. Applies: task creates `tests/api/sbom_advisory_summary.rs` matching the convention's Rust language scope.
- Per CONVENTIONS.md §Test Patterns: use real PostgreSQL test database with `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task creates `tests/api/sbom_advisory_summary.rs` matching the convention's `tests/api/` directory scope.

## Reuse Candidates
- `tests/api/sbom.rs` — Existing SBOM integration tests to use as template for test setup, fixture creation, and assertion patterns
- `tests/api/advisory.rs` — Advisory integration tests for advisory fixture creation patterns with severity values

## Acceptance Criteria
- [ ] All integration tests pass against PostgreSQL test database
- [ ] Tests cover: valid SBOM response, 404 for missing SBOM, empty advisory set, threshold filter variations, advisory deduplication
- [ ] Tests validate both response JSON structure (field names and types) and correctness of severity counts

## Test Requirements
- [ ] Test: valid SBOM with advisories at Critical, High, Medium, Low severities returns correct counts for each level
- [ ] Test: non-existent SBOM ID returns 404 status code
- [ ] Test: SBOM with no linked advisories returns `{ "critical": 0, "high": 0, "medium": 0, "low": 0, "total": 0 }`
- [ ] Test: `?threshold=critical` returns only critical count with other levels as 0
- [ ] Test: `?threshold=high` returns critical and high counts with medium and low as 0
- [ ] Test: duplicate advisory-SBOM links do not inflate severity counts
- [ ] Test: response includes `Cache-Control` header with `max-age=300`

## Dependencies
- Depends on: Task 4 — Add threshold query parameter support
- Depends on: Task 5 — Add cache invalidation in advisory ingestor

## Additional Fields
- priority: Major
- fixVersions: RHTPA 1.5.0
- labels: ai-generated-jira
