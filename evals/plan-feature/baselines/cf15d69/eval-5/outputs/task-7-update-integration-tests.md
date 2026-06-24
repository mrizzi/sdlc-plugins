## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to reflect the schema change. Tests must no longer set up or reference the `advisory_status` lookup table. Instead, test fixtures should create advisories with the `status` enum column directly. Add test coverage for status filtering via the enum column.

## Files to Modify
- `tests/api/advisory.rs` — Update test fixtures to insert advisories with `status: AdvisoryStatusEnum::*` instead of creating lookup table rows and using `status_id`; update assertions to verify status comes from enum column; add tests for filtering by each enum status value

## Implementation Notes
- Existing test helpers that set up advisory test data likely insert rows into `advisory_status` first, then reference them. Replace with direct enum value assignment on advisory inserts
- Add or update a test case that filters advisories by status (e.g., `GET /api/v2/advisory?status=Fixed`) and asserts the correct subset is returned
- Add a test verifying that the response JSON `status` field is a string matching the enum value (e.g., `"Fixed"`, not an integer ID)
- Follow existing test patterns: use `assert_eq!(resp.status(), StatusCode::OK)` for response assertions per `tests/api/advisory.rs`

Per Key Conventions (Testing): Integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/advisory.rs` matching the integration test scope.

## Acceptance Criteria
- [ ] No references to `advisory_status` lookup table remain in test code
- [ ] Advisory test fixtures use the `status` enum column directly
- [ ] Test coverage exists for filtering advisories by each status value (New, Analyzing, Fixed, Rejected)
- [ ] All advisory integration tests pass
- [ ] Response shape assertions confirm status is a string value

## Test Requirements
- [ ] Run advisory integration tests: `cargo test -p trustify-tests --test advisory`
- [ ] All tests pass against a test database with the new schema

## Verification Commands
```bash
cargo test -p trustify-tests --test advisory
```

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service layer and queries
- Depends on: Task 5 — Update advisory endpoints
- Depends on: Task 6 — Update advisory ingestion pipeline

[sdlc-workflow] Description digest: sha256-md:c49f6e5099f9dde5adf0782eec95fefa273efc78fda562b2a6a095c1f55d7719
