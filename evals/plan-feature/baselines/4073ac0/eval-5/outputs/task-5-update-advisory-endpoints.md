## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update advisory endpoint handlers to use enum-based status filtering instead of join-based filtering. The list and get endpoints must pass status filter parameters as enum values to the updated service layer. The response shape remains unchanged — status is still returned as a string to API consumers.

## Files to Modify
- `modules/fundamental/src/advisory/endpoints/list.rs` — Update status filter parameter handling to convert the query string value to `AdvisoryStatusEnum` before passing to the service; remove any reference to `advisory_status` entity
- `modules/fundamental/src/advisory/endpoints/get.rs` — Update advisory detail retrieval if it references `advisory_status` entity or performs its own status join
- `modules/fundamental/src/advisory/endpoints/mod.rs` — Update route registration if status filter parameter types changed; remove `advisory_status` imports

## Implementation Notes
Follow the existing endpoint patterns in `modules/fundamental/src/advisory/endpoints/list.rs`. The list endpoint likely accepts a status filter as a query parameter (string). This string must be parsed into an `AdvisoryStatusEnum` value before being passed to the service method.

Use the existing error handling pattern from `common/src/error.rs` — if the status string does not match a valid enum variant, return an `AppError` with an appropriate status code (400 Bad Request) using `.context()` wrapping.

The response serialization should not change — `AdvisoryStatusEnum` serializes to a string via SeaORM's `DeriveActiveEnum` string values, maintaining backward compatibility with API consumers.

Follow the route registration pattern in `modules/fundamental/src/advisory/endpoints/mod.rs` for any parameter type changes.

## Reuse Candidates
- `common/src/error.rs::AppError` — Error type for invalid status parameter handling
- `modules/fundamental/src/advisory/endpoints/list.rs` — Existing list handler to modify in-place
- `modules/fundamental/src/sbom/endpoints/list.rs` — Sibling endpoint for pattern reference on filter parameter handling

## Acceptance Criteria
- [ ] Advisory list endpoint accepts status filter and correctly filters by enum value
- [ ] Invalid status filter values return 400 Bad Request with descriptive error
- [ ] Advisory get endpoint returns correct status from enum column
- [ ] Response shape is unchanged — status field is still a string
- [ ] No remaining references to `advisory_status` entity in endpoint handlers

## Test Requirements
- [ ] GET `/api/v2/advisory?status=Fixed` returns only advisories with Fixed status
- [ ] GET `/api/v2/advisory?status=InvalidValue` returns 400 error
- [ ] GET `/api/v2/advisory/{id}` returns advisory with correct status string
- [ ] Response body format is unchanged (backward compatible)

## Verification Commands
- `cargo check -p fundamental` — fundamental module compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
