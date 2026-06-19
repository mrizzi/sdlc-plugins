## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests should cover the happy path (valid SBOM with advisories at various severity levels), the 404 case (non-existent SBOM ID), the threshold filter query parameter, deduplication of advisories, and an SBOM with no advisories returning zero counts.

## Files to Create
- `tests/api/sbom_advisory_summary.rs` — Integration tests for the advisory-summary endpoint

## Implementation Notes
Follow the integration test pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests hit a real PostgreSQL test database and use the pattern:

```rust
assert_eq!(resp.status(), StatusCode::OK);
```

Test setup should:
1. Create test SBOM(s) via the ingestion pipeline or direct DB insertion
2. Create advisory records with different severity levels linked to the SBOM via the `sbom_advisory` join table
3. Call the endpoint and verify the response body

Test cases to implement:
- **Happy path**: SBOM with advisories at critical (2), high (3), medium (1), low (0) severity — verify counts match
- **Empty advisories**: SBOM with no linked advisories — verify all counts are 0 and total is 0
- **Non-existent SBOM**: Request with invalid SBOM ID — verify 404 status
- **Threshold filter**: Use `?threshold=high` — verify only critical and high counts are included
- **Deduplication**: Same advisory linked to SBOM multiple times — verify it is counted only once

Per CONVENTIONS.md §Testing: integration tests go in `tests/api/` and use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task creates `tests/api/sbom_advisory_summary.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `tests/api/sbom.rs` — Integration test patterns for SBOM endpoints, including test DB setup and teardown
- `tests/api/advisory.rs` — Integration test patterns for advisory endpoints, including advisory creation helpers
- `common/src/model/paginated.rs::PaginatedResults` — Reference for how list endpoints are tested (though this endpoint does not use pagination)

## Acceptance Criteria
- [ ] All test cases pass against a PostgreSQL test database
- [ ] Happy path test verifies correct severity counts in the response body
- [ ] 404 test verifies non-existent SBOM returns 404 status
- [ ] Threshold filter test verifies filtered response
- [ ] Deduplication test verifies advisories are not double-counted
- [ ] Zero-advisory test verifies all counts are 0

## Test Requirements
- [ ] Integration test: valid SBOM with mixed severity advisories returns correct counts
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: SBOM with no advisories returns zero counts
- [ ] Integration test: threshold query parameter filters response correctly
- [ ] Integration test: duplicate advisory links are deduplicated in counts

## Verification Commands
- `cargo test --test api` — Run integration tests against the test database
- `cargo test sbom_advisory_summary` — Run only the new test module

## Dependencies
- Depends on: Task 4 — Create advisory-summary endpoint with caching