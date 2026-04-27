## Repository
trustify-backend

## Description
Add comprehensive integration tests for the license compliance report endpoint covering report generation, compliance flags, edge cases, and policy evaluation.

## Files to Create
- `tests/api/license_report.rs` — integration test module for `GET /api/v2/sbom/{id}/license-report`

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs` for test setup, database fixtures, and assertion style.
- Tests must hit a real PostgreSQL test database — no mocking.
- Set up test data: ingest a test SBOM with packages using known licenses (mix of MIT, Apache-2.0, GPL-3.0, and unknown licenses), configure a test license policy.
- Verify that non-compliant licenses are correctly flagged in the response.

## Reuse Candidates
- `tests/api/sbom.rs` — integration test patterns, test data setup
- `tests/api/advisory.rs` — fixture creation patterns

## Acceptance Criteria
- [ ] Integration tests pass against a real PostgreSQL test database
- [ ] Tests cover: correct grouping, compliance evaluation, 404, edge cases
- [ ] Tests follow existing `tests/api/` patterns

## Test Requirements
- [ ] Test: report correctly groups packages by license
- [ ] Test: compliance flags match policy (allowed → true, denied → false)
- [ ] Test: 404 response for non-existent SBOM ID
- [ ] Test: SBOM with no packages returns empty groups
- [ ] Test: packages with unknown licenses use policy default_compliant value

## Dependencies
- Depends on: Task 3 — License report endpoint
