## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory endpoint integration tests to reflect the new schema and query patterns. The tests currently set up test data by inserting rows into the `advisory_status` lookup table and joining on `status_id`. They need to be updated to insert advisories with the `status` enum column directly. Additionally, verify that status filtering on the list endpoint works correctly with enum values.

## Files to Modify
- `tests/api/advisory.rs` — Update all test setup code to use the `status` enum column instead of inserting into the `advisory_status` table and setting `status_id`; update assertions to check the status field as a string enum value; add or update test cases for status filtering with enum values

## Implementation Notes
- Test setup currently likely creates `advisory_status` rows and inserts advisories with `status_id` FK references. Replace this with direct insertion of advisories using `AdvisoryStatusEnum` variants in the `status` field.
- Follow the existing test pattern in `tests/api/advisory.rs` — the project uses `assert_eq!(resp.status(), StatusCode::OK)` and tests against a real PostgreSQL test database.
- Reference `tests/api/sbom.rs` for the general integration test structure and patterns (setup, request, assertion).
- Ensure tests cover all four status values (New, Analyzing, Fixed, Rejected) to verify the enum mapping is correct end-to-end.
- The response JSON shape should be unchanged, so existing response assertions should largely remain valid — only the setup code and any status-specific assertions need updating.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM integration tests demonstrating the project's test setup, HTTP request, and assertion patterns
- `tests/api/search.rs` — Search integration tests showing how cross-entity queries are tested

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new enum-based schema
- [ ] No test code references the `advisory_status` table or `status_id` field
- [ ] Tests verify status filtering works with enum values on the list endpoint
- [ ] Tests cover all four advisory status values (New, Analyzing, Fixed, Rejected)

## Test Requirements
- [ ] All existing advisory tests pass after updating to use the enum column
- [ ] New or updated test cases verify status filtering with each enum variant
- [ ] Verify test database setup correctly creates advisories with enum status values

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and endpoints
- Depends on: Task 5 — Update ingestion pipeline
