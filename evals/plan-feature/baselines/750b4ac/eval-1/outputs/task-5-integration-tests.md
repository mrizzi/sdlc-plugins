# Task 5 — Add integration tests for the advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests should cover the happy path (SBOM with advisories at multiple severity levels), the 404 case (non-existent SBOM), the empty case (SBOM with no linked advisories), deduplication behavior (same advisory linked multiple times), and the threshold query parameter. Follow the existing integration test patterns in `tests/api/`.

## Files to Modify
- `tests/Cargo.toml` — add any necessary test dependencies if not already present

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for the advisory-summary endpoint

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Set up test data by ingesting SBOMs and advisories through the ingestion pipeline (or directly inserting test entities), then linking them via the `sbom_advisory` join table.
- Include the new test file in the test module structure — check how `tests/api/sbom.rs` and `tests/api/advisory.rs` are included (likely via a `mod` declaration in a parent file or via Cargo test configuration).
- Test cases to implement:
  1. **Happy path**: create an SBOM, link advisories at critical, high, medium, and low severities, call the endpoint, verify counts match
  2. **404 case**: call the endpoint with a non-existent SBOM ID, verify 404 response
  3. **Empty advisories**: create an SBOM with no linked advisories, verify all counts are 0
  4. **Deduplication**: link the same advisory to an SBOM through multiple paths, verify it is counted only once
  5. **Threshold filtering**: call with `?threshold=critical`, verify only critical counts are returned; repeat for other threshold levels
  6. **Response shape**: verify the JSON response has exactly the expected fields (critical, high, medium, low, total) with correct types
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task creates `tests/api/advisory_summary.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests; follow test setup, fixtures, and assertion patterns
- `tests/api/advisory.rs` — existing advisory endpoint integration tests; reference for advisory-related test data setup
- `entity/sbom_advisory.rs` — SBOM-Advisory join table entity; use for linking test data

## Acceptance Criteria
- [ ] Integration tests exist for the advisory-summary endpoint in `tests/api/advisory_summary.rs`
- [ ] Tests cover: happy path with mixed severity advisories, 404 for missing SBOM, empty advisory set, deduplication, threshold filtering
- [ ] All tests pass against the PostgreSQL test database
- [ ] Tests follow existing patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`

## Test Requirements
- [ ] Test verifying correct severity counts for an SBOM with advisories at all severity levels
- [ ] Test verifying 404 response for non-existent SBOM ID
- [ ] Test verifying all-zero counts for an SBOM with no linked advisories
- [ ] Test verifying deduplication of advisories (same advisory counted once even if linked multiple times)
- [ ] Test verifying threshold query parameter filters counts correctly for each threshold level
- [ ] Test verifying response JSON shape matches `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`

## Verification Commands
- `cargo test --test api -- advisory_summary` — run only the advisory-summary integration tests
- `cargo test` — all tests pass including the new ones

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint and route registration
- Depends on: Task 4 — Add optional threshold query parameter to advisory-summary endpoint

[sdlc-workflow] Description digest: sha256-md:a86611cfd59da3e7f97d046ec9b1ebe111ffd0f1d62f27afdc9fd913c9c737d6
