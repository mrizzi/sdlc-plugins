## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests cover the full request-response cycle against a real PostgreSQL test database, verifying correct severity aggregation, 404 handling, threshold filtering, advisory deduplication, and cache invalidation behavior.

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for the advisory-summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add any necessary test dependencies if not already present (verify before modifying)

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs` for test setup, HTTP client configuration, and assertion style.
- Use the established pattern of `assert_eq!(resp.status(), StatusCode::OK)` for status code assertions.
- Tests should run against a real PostgreSQL test database, consistent with the project's integration test approach.
- Test setup should:
  1. Ingest a test SBOM
  2. Ingest test advisories with known severity levels (e.g., 2 critical, 3 high, 1 medium, 1 low)
  3. Correlate the advisories with the SBOM via the ingestion pipeline
- Test cases to implement:
  - **Success case**: verify response body matches expected severity counts `{ critical: 2, high: 3, medium: 1, low: 1, total: 7 }`
  - **404 case**: request with a non-existent SBOM ID returns HTTP 404
  - **Deduplication**: link the same advisory to the SBOM twice, verify it is counted only once
  - **Threshold filtering**: `?threshold=high` returns only critical and high counts with zeroed medium/low and recalculated total
  - **Threshold filtering (critical)**: `?threshold=critical` returns only critical count with all others zeroed
  - **Empty case**: SBOM with no linked advisories returns all zeros `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`
- Reference the test utilities and fixtures used in `tests/api/sbom.rs` for SBOM ingestion in tests.
- Reference `tests/api/advisory.rs` for advisory ingestion test patterns.

## Reuse Candidates
- `tests/api/sbom.rs` — integration test patterns for SBOM endpoints; reuse test setup (SBOM ingestion), HTTP client configuration, and assertion patterns
- `tests/api/advisory.rs` — integration test patterns for advisory endpoints; reuse advisory ingestion setup and correlation logic
- `common/src/model/paginated.rs::PaginatedResults` — reference for understanding response wrapper patterns (this endpoint does not use pagination, but the test infrastructure is shared)

## Acceptance Criteria
- [ ] Integration test file exists at `tests/api/advisory_summary.rs`
- [ ] Tests cover: success response, 404, deduplication, threshold filtering, empty SBOM
- [ ] All tests pass against the PostgreSQL test database
- [ ] Tests follow the established test patterns from sibling test files

## Test Requirements
- [ ] Test that `GET /api/v2/sbom/{id}/advisory-summary` returns correct counts for an SBOM with known advisory data
- [ ] Test that a non-existent SBOM ID returns HTTP 404
- [ ] Test that duplicate advisory-SBOM links do not inflate counts
- [ ] Test that `?threshold=high` filters out medium and low counts and recalculates total
- [ ] Test that `?threshold=critical` returns only critical count
- [ ] Test that an SBOM with zero advisories returns all-zero counts

## Verification Commands
- `cargo test --test api advisory_summary` — all advisory-summary integration tests should pass

## Dependencies
- Depends on: Task 2 — Add advisory-summary endpoint with caching and threshold filter
