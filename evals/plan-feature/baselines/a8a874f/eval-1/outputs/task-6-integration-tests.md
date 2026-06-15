# Task 6: Write end-to-end integration tests for advisory-summary endpoint

## Repository

trustify-backend

## Target Branch

main

## Dependencies

- Task 3 (advisory-summary endpoint)
- Task 4 (threshold query parameter)
- Task 5 (cache invalidation)

## Description

Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering the full request-response cycle against a real PostgreSQL test database. Tests should validate the happy path, error cases, threshold filtering, severity deduplication, and cache behavior. This task consolidates all endpoint-level integration tests into the existing test infrastructure.

## Files to Modify

- `tests/api/sbom.rs` -- add integration test functions for the advisory-summary endpoint

## Reuse Candidates

- `tests/api/sbom.rs` -- existing SBOM integration tests provide patterns for test setup, database seeding, and assertion style
- `tests/api/advisory.rs` -- advisory integration tests show how advisory test fixtures are created and linked to SBOMs

## Implementation Notes

- Follow the integration test patterns in `tests/api/sbom.rs`. Existing tests use `assert_eq!(resp.status(), StatusCode::OK)` for status assertions and parse JSON response bodies.
- Seed test data by creating an SBOM and linking advisories with different severity levels through the `sbom_advisory` join table. Reference the entity definitions in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/sbom_advisory.rs` for the required fields.
- Test cases to implement:
  1. SBOM with advisories at all four severity levels returns correct counts and total
  2. SBOM with no advisories returns `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`
  3. Non-existent SBOM ID returns 404
  4. Duplicate advisory links are deduplicated (same advisory linked twice produces count of 1)
  5. `?threshold=critical` returns only critical count, others zeroed
  6. `?threshold=high` returns critical + high counts
  7. Invalid threshold value returns 400
  8. Response includes `Cache-Control` header with `max-age=300`
- Use the test database infrastructure from `tests/Cargo.toml` -- tests run against a real PostgreSQL instance.

### Applicable Conventions

- **Testing**: Applies: task modifies `tests/api/sbom.rs` matching the convention's integration test file scope -- tests hit a real PostgreSQL test database with `assert_eq!(resp.status(), StatusCode::OK)` pattern.

## Acceptance Criteria

- [ ] All 8 test cases listed in Implementation Notes are implemented
- [ ] Tests pass against a PostgreSQL test database
- [ ] Tests follow the existing assertion patterns in `tests/api/sbom.rs`
- [ ] Test data setup creates realistic advisory-SBOM relationships
- [ ] No test depends on ordering or external state from other tests

## Test Requirements

- [ ] Test: SBOM with mixed severity advisories returns correct per-severity counts and correct total
- [ ] Test: empty SBOM returns all-zero counts
- [ ] Test: non-existent SBOM returns 404 status
- [ ] Test: duplicate advisory links produce deduplicated counts
- [ ] Test: threshold=critical filters to critical only
- [ ] Test: threshold=high filters to critical and high
- [ ] Test: invalid threshold returns 400 status
- [ ] Test: response includes Cache-Control max-age=300 header

## Verification Commands

- `cargo test --test api -- advisory_summary` -- run only the advisory-summary integration tests
- `cargo test --test api` -- run the full API integration test suite to verify no regressions

[Description digest: sha256-md:f8c2a7b6e5d4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8 would be posted as a comment]
