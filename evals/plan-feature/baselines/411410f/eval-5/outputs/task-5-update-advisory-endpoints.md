# Task 5 -- Update advisory endpoints for enum status

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory REST endpoints to work with the new enum-based status column. The list endpoint's status filter query parameter must map to enum values instead of joining the lookup table. The get endpoint must return the status string from the enum column. No changes to the external API response shape -- status remains a string field in the JSON response.

## Files to Modify
- `modules/fundamental/src/advisory/endpoints/list.rs` -- Update status filter parameter handling to parse into `AdvisoryStatusEnum` and filter on the enum column; remove any `advisory_status` join logic in the endpoint handler
- `modules/fundamental/src/advisory/endpoints/get.rs` -- Update single-advisory response construction to read status from the enum field; remove any `advisory_status` references
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- Remove any `advisory_status`-related route registrations or imports if present

## Implementation Notes
- In `modules/fundamental/src/advisory/endpoints/list.rs`, the status filter query parameter (e.g., `?status=Fixed`) should be parsed into `AdvisoryStatusEnum` and passed to `AdvisoryService::list`. Use SeaORM's `DeriveActiveEnum` string conversion. If the query parameter does not match a valid enum variant, return an appropriate error via `AppError`.
- In `modules/fundamental/src/advisory/endpoints/get.rs`, the status field in the response is populated from `AdvisoryDetails`, which was updated in Task 4. Verify that the endpoint handler does not independently join `advisory_status`.
- The response shape remains unchanged -- the API contract is stable. The `status` field in the JSON response is still a string (e.g., `"Fixed"`), it just comes from an enum column now.
- Follow the endpoint patterns in `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/sbom/endpoints/get.rs` for the handler function structure.
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs` -- maintain this pattern.
- Route registration in `modules/fundamental/src/advisory/endpoints/mod.rs` should not need structural changes unless it currently registers advisory-status-specific routes.

## Acceptance Criteria
- [ ] `GET /api/v2/advisory?status=Fixed` filters by enum column without joining `advisory_status`
- [ ] `GET /api/v2/advisory/{id}` returns status from enum column
- [ ] API response shape is unchanged -- `status` is still a string field
- [ ] Invalid status filter values return an appropriate error response
- [ ] No remaining references to `advisory_status` entity in the endpoints module
- [ ] `cargo build -p fundamental` compiles without errors

## Test Requirements
- [ ] Integration test: `GET /api/v2/advisory` returns advisories with correct status strings
- [ ] Integration test: `GET /api/v2/advisory?status=Fixed` returns only advisories with status "Fixed"
- [ ] Integration test: `GET /api/v2/advisory?status=Invalid` returns an error response
- [ ] Integration test: `GET /api/v2/advisory/{id}` returns the correct status for a single advisory

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 4 -- Update advisory service and model layers
