## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering the primary use cases: successful severity aggregation, 404 for missing SBOMs, threshold filtering, and deduplication of advisories. These tests validate the end-to-end behavior of the endpoint against a real PostgreSQL test database, following the project's established integration test patterns.

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for the advisory summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add any necessary test dependencies if not already present (likely none needed if existing test infrastructure covers HTTP testing)

## Implementation Notes
- Follow the existing integration test patterns established in `tests/api/sbom.rs` (SBOM endpoint tests) and `tests/api/advisory.rs` (advisory endpoint tests). These tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.
- Inspect `tests/api/sbom.rs` for test setup patterns: how the test database is initialized, how test data (SBOMs and advisories) is inserted, and how HTTP requests are made to the test server.
- Test data setup should create:
  - An SBOM with advisories at each severity level (critical, high, medium, low) for the happy-path test
  - An SBOM with duplicate advisory links (same advisory ID linked multiple times) for the deduplication test
  - An SBOM with zero advisories for the empty case
- Test cases to implement:
  1. **Happy path**: SBOM with known advisories returns correct severity counts and total
  2. **Not found**: non-existent SBOM ID returns 404
  3. **Empty**: SBOM with no advisories returns all-zero counts
  4. **Deduplication**: SBOM with duplicate advisory links returns deduplicated counts
  5. **Threshold filter**: `?threshold=critical` returns only critical count; `?threshold=high` returns critical + high
  6. **Invalid threshold**: `?threshold=invalid` returns 400
- Verify response JSON shape matches `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` by deserializing into the `AdvisorySeveritySummary` struct.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration tests; reference for test setup, database fixtures, HTTP request patterns, and assertion style
- `tests/api/advisory.rs` — advisory endpoint integration tests; reference for advisory test data creation patterns
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join entity for creating test fixture relationships

## Acceptance Criteria
- [ ] Integration test file exists at `tests/api/advisory_summary.rs`
- [ ] All test cases pass against the PostgreSQL test database
- [ ] Tests cover: happy path, 404, empty SBOM, deduplication, threshold filtering, invalid threshold
- [ ] Tests follow the established test patterns from sibling test files (sbom.rs, advisory.rs)
- [ ] `cargo test` completes successfully with all new tests passing

## Test Requirements
- [ ] Test: valid SBOM with multiple severity-level advisories returns correct counts per level and correct total
- [ ] Test: non-existent SBOM ID returns 404 status
- [ ] Test: SBOM with no linked advisories returns `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`
- [ ] Test: SBOM with duplicate advisory links returns deduplicated counts (same advisory counted once)
- [ ] Test: `?threshold=critical` returns only critical count with other levels zeroed, total equals critical count
- [ ] Test: `?threshold=high` returns critical and high counts, total equals their sum
- [ ] Test: `?threshold=invalid` returns 400 Bad Request

## Verification Commands
- `cargo test --test api -- advisory_summary` — runs the advisory summary integration tests
- `cargo test` — verifies all tests including new ones pass

## Dependencies
- Depends on: Task 4 — Add threshold query parameter support

[sdlc-workflow] Description digest: sha256:cfdb87bb48460ae9640dd170036939e3e632db313c3fd8266e3f83c9006e9ef6
