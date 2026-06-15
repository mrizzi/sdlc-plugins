## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Add and update integration tests to validate the complete advisory status enum migration end-to-end. Ensure that advisory listing with status filters, advisory detail retrieval, and advisory ingestion all work correctly with the new enum column. Verify backward compatibility of the API response shape.

## Files to Modify
- `tests/api/advisory.rs` — Update existing advisory integration tests to work with the enum-based status column; add new tests for status filtering, ingestion round-trip, and API response shape validation

## Implementation Notes
Follow the existing integration test patterns in `tests/api/advisory.rs` and sibling test files like `tests/api/sbom.rs`. Tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for response validation.

Key test scenarios to cover:
1. List advisories filtered by each enum status value (New, Analyzing, Fixed, Rejected) — verify the correct subset is returned
2. Get advisory by ID — verify the response includes the status as a string matching the enum value
3. Ingest a new advisory with a status — verify it appears in subsequent list queries with the correct status
4. Verify the API response JSON shape is unchanged from before the migration — status is still a top-level string field, not a nested object

Ensure all existing tests pass without modification to the expected response shape (backward compatibility).

## Acceptance Criteria
- [ ] All existing advisory integration tests pass
- [ ] New test for filtering by each status enum value (New, Analyzing, Fixed, Rejected)
- [ ] New test for advisory detail retrieval with enum status
- [ ] New test for ingestion-to-query round-trip with enum status
- [ ] API response shape backward compatibility is validated
- [ ] All tests pass with `cargo test`

## Test Requirements
- [ ] Filter by status=New returns only advisories with New status
- [ ] Filter by status=Analyzing returns only advisories with Analyzing status
- [ ] Filter by status=Fixed returns only advisories with Fixed status
- [ ] Filter by status=Rejected returns only advisories with Rejected status
- [ ] Advisory detail response includes status as a string field
- [ ] Ingested advisory with status=Fixed is retrievable with correct status

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005
- Depends on: Task 4 — Update advisory service and endpoints
- Depends on: Task 5 — Update ingestion pipeline

[sdlc-workflow] Description digest: sha256-md:13937b71e02f78209a93e70964cc53148f8da88bf8c71df634c0795abecbadf6
