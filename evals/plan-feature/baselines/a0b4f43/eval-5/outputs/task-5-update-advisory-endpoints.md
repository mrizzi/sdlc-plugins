## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory endpoint handlers to work with the new enum-based status field. The list endpoint must support filtering by `advisory_status_enum` values directly, and the get endpoint must return the status as a string from the enum. Since the service layer changes (Task 4) handle the underlying query modifications, this task focuses on the endpoint-level filtering logic and response serialization to ensure the API contract remains unchanged.

## Files to Modify
- `modules/fundamental/src/advisory/endpoints/list.rs` — update status filter parameter parsing to work with `AdvisoryStatusEnum` values; remove any references to `advisory_status` table or ID-based filtering
- `modules/fundamental/src/advisory/endpoints/get.rs` — update response construction if it directly accesses status fields; ensure enum status serializes to the same string format as before
- `modules/fundamental/src/advisory/endpoints/mod.rs` — update imports and route registration if filter parameter types change

## Implementation Notes
- The list endpoint (`GET /api/v2/advisory`) likely accepts a status filter query parameter. Update the parsing to convert the string parameter directly to an `AdvisoryStatusEnum` variant instead of looking up a status ID.
- Ensure the status enum serializes to PascalCase strings (New, Analyzing, Fixed, Rejected) in JSON responses to maintain backward compatibility with the existing API response shape.
- Follow the endpoint patterns in `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/sbom/endpoints/get.rs` for consistent error handling (all handlers return `Result<T, AppError>` with `.context()` wrapping per the project conventions).
- Per `docs/constraints.md` §5.3: follow the patterns referenced in Implementation Notes.
- Per `docs/constraints.md` §2 (Commit Rules): commit message must follow Conventional Commits format and reference TC-9005.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference endpoint demonstrating the project's list endpoint pattern with filter parameters
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference endpoint demonstrating the get-by-ID pattern
- `common/src/error.rs` — `AppError` enum for consistent error handling

## Acceptance Criteria
- [ ] `GET /api/v2/advisory` supports filtering by status using enum string values (New, Analyzing, Fixed, Rejected)
- [ ] `GET /api/v2/advisory/{id}` returns status as a string matching the previous response format
- [ ] Invalid status filter values return an appropriate error response
- [ ] No references to `advisory_status` table remain in endpoint code
- [ ] API response shape for advisory endpoints is unchanged (backward compatible)

## Test Requirements
- [ ] Verify the fundamental module compiles: `cargo check -p fundamental`
- [ ] Verify no compilation errors when building the full server: `cargo check -p server`

## Verification Commands
- `cargo check -p fundamental` — compiles without errors
- `cargo check -p server` — full server compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main