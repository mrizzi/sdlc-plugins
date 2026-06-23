# Task 5: Add integration tests for the advisory summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Create a comprehensive integration test suite for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The tests verify correct behavior for valid SBOMs with advisories, nonexistent SBOMs, threshold query parameter filtering, and response shape validation. These tests exercise the full stack from HTTP request through service logic to database queries against a real PostgreSQL test database.

## Files to Create
- `tests/api/sbom_advisory_summary.rs` — integration test module containing all test cases for the advisory summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add the new test file to the test harness if required by the project's test configuration (some Rust projects auto-discover test files, others require explicit listing)

## Implementation Notes
- Follow the test patterns established in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These files demonstrate how to:
  - Set up a test PostgreSQL database with fixtures
  - Create an Axum test client using the application's route tree
  - Issue HTTP requests and assert on status codes and JSON response bodies
- Each test should seed the database with known data: create an SBOM, create advisories with specific severities, and link them via the `sbom_advisory` join table using the entities from `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/sbom_advisory.rs`.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code assertions, consistent with existing tests in the Key Conventions §Testing section.
- For JSON body assertions, deserialize the response body into `AdvisorySeveritySummary` and assert individual field values.
- Test case outline:
  1. **Valid SBOM returns correct counts**: Seed an SBOM with 2 critical, 1 high, 3 medium, 0 low advisories. Assert response `{ critical: 2, high: 1, medium: 3, low: 0, total: 6 }`.
  2. **Nonexistent SBOM returns 404**: Call with a random UUID. Assert `StatusCode::NOT_FOUND`.
  3. **Threshold filter works**: Seed same data as test 1. Call with `?threshold=high`. Assert `{ critical: 2, high: 1, medium: 0, low: 0, total: 3 }`.
  4. **Response shape validation**: Assert response `Content-Type` is `application/json`. Assert all expected fields (`critical`, `high`, `medium`, `low`, `total`) are present and are non-negative integers.
  5. **Deduplication**: Link the same advisory to the SBOM twice (via different packages). Assert the advisory is counted only once.
- Per Key Conventions §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task creates `tests/api/sbom_advisory_summary.rs` matching the convention's `tests/api/` scope.

## Reuse Candidates
- `tests/api/sbom.rs` — reference for test setup, database seeding, HTTP client creation, and assertion patterns
- `tests/api/advisory.rs` — reference for creating advisory test fixtures with specific severity levels
- `entity/src/sbom.rs` — SBOM entity for creating test SBOMs
- `entity/src/advisory.rs` — Advisory entity for creating test advisories with specific severities
- `entity/src/sbom_advisory.rs` — join table entity for linking test advisories to test SBOMs
- `modules/fundamental/src/sbom/model/advisory_summary.rs::AdvisorySeveritySummary` — response struct to deserialize and assert against

## Acceptance Criteria
- [ ] Integration test file exists at `tests/api/sbom_advisory_summary.rs`
- [ ] Test `valid_sbom_returns_advisory_severity_counts` passes -- correct counts returned for a seeded SBOM
- [ ] Test `nonexistent_sbom_returns_404` passes -- 404 status for a random UUID
- [ ] Test `threshold_filter_excludes_lower_severities` passes -- threshold=high returns only critical and high counts
- [ ] Test `response_shape_has_all_fields` passes -- JSON response contains all expected fields with correct types
- [ ] Test `duplicate_advisory_links_are_deduplicated` passes -- same advisory linked twice counts as 1
- [ ] All tests are deterministic and do not depend on external state or ordering

## Test Requirements
- [ ] Test: valid SBOM with 2 critical, 1 high, 3 medium, 0 low advisories returns `{ critical: 2, high: 1, medium: 3, low: 0, total: 6 }`
- [ ] Test: SBOM with no advisories returns `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`
- [ ] Test: non-existent SBOM returns HTTP 404
- [ ] Test: duplicate advisory linkage (same advisory linked via multiple packages) counts advisory only once
- [ ] Test: `?threshold=critical` returns only critical count, others zero
- [ ] Test: `?threshold=medium` returns critical + high + medium counts, low is zero
- [ ] Test: invalid `?threshold=invalid` returns HTTP 400
- [ ] Tests use isolated database transactions or test fixtures that do not interfere with each other
- [ ] Tests follow existing naming and structure conventions from `tests/api/sbom.rs`

## Verification Commands
- `cargo test --test api -- sbom_advisory_summary` — all advisory summary integration tests pass
- `cargo test --test api` — full API test suite passes (no regressions)

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint handler and route registration

---

> [sdlc-workflow] Description digest: sha256-md:e5b8g9d40f7c329175h4e0b68d9fc2g45i2edh26h8f05491gcb7d63e8h1f0254
