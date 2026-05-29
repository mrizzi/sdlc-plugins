# Task 4 -- Update advisory service, models, and endpoints to use enum status

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer, model structs, and HTTP endpoints to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join from all advisory queries, reducing advisory list endpoint p95 latency by approximately 40ms. The response shape remains identical to callers -- status is still returned as a string.

## Files to Modify
- `modules/fundamental/src/advisory/model/summary.rs` -- update `AdvisorySummary` struct to read `status` as `AdvisoryStatusEnum` from the advisory entity directly instead of from a joined `advisory_status` record; ensure serialization still outputs a string
- `modules/fundamental/src/advisory/model/details.rs` -- update `AdvisoryDetails` struct similarly to use the enum status field directly
- `modules/fundamental/src/advisory/model/mod.rs` -- update any shared model helpers or type re-exports related to advisory status
- `modules/fundamental/src/advisory/service/advisory.rs` -- remove all `advisory_status` table joins from `AdvisoryService` methods (fetch, list, search); replace `status_id` filter conditions with direct `status` enum column comparisons using `WHERE status = 'Fixed'` style queries
- `modules/fundamental/src/advisory/endpoints/list.rs` -- update the list endpoint handler to filter by enum `status` column instead of joining the lookup table; update any query parameter parsing for status filter values
- `modules/fundamental/src/advisory/endpoints/get.rs` -- update the get endpoint handler to read status from the enum column
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- update route registration if any status-related types are imported from the old advisory_status entity
- `common/src/db/query.rs` -- update shared query helpers if any advisory-status-specific filtering or sorting logic references the `advisory_status` table or `status_id` column

## Implementation Notes
- The key change in `AdvisoryService` is removing `.join()` or `.find_also_related()` calls that join the `advisory_status` table. Replace these with direct column access on the `advisory` entity
- For status filtering in list endpoints, use SeaORM column equality: `advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed)` instead of joining and filtering on the lookup table
- Ensure that JSON serialization of `AdvisoryStatusEnum` produces the same string values as before (e.g., `"Fixed"`, `"New"`) to maintain API backward compatibility. Use `#[serde(rename_all = ...)]` or explicit `#[serde(rename = "...")]` as needed
- Follow the existing service patterns in `modules/fundamental/src/sbom/service/sbom.rs` for query construction and error handling with `.context()` wrapping
- Follow the existing endpoint patterns in `modules/fundamental/src/sbom/endpoints/list.rs` for handler structure and `PaginatedResults<T>` return type
- The `common/src/db/query.rs` helpers for filtering and pagination may reference status-related logic -- inspect before modifying
- Per docs/constraints.md SS2 (Commit Rules): commit message must follow Conventional Commits format and reference TC-9005
- Per docs/constraints.md SS5.4 (Code Change Rules): reuse existing query builder helpers in `common/src/db/query.rs` rather than duplicating filtering logic

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs` -- reference for SeaORM query construction patterns (find, filter, paginate) without joins
- `modules/fundamental/src/sbom/endpoints/list.rs` -- reference for endpoint handler patterns and `PaginatedResults` usage
- `modules/fundamental/src/sbom/model/summary.rs` -- reference for model struct layout with direct entity field mapping
- `common/src/db/query.rs` -- shared query builder helpers for filtering and pagination

## Acceptance Criteria
- [ ] All advisory queries (list, get, search) no longer join the `advisory_status` table
- [ ] Advisory list endpoint supports filtering by status using the enum column (e.g., `?status=Fixed`)
- [ ] API response shape is unchanged -- `status` field still appears as a string in JSON responses
- [ ] `AdvisorySummary` and `AdvisoryDetails` structs use `AdvisoryStatusEnum` directly
- [ ] No remaining references to `advisory_status` entity or `status_id` column in the advisory module
- [ ] `cargo build -p fundamental` compiles without errors

## Test Requirements
- [ ] Verify advisory list endpoint returns correct results when filtering by each status value (New, Analyzing, Fixed, Rejected)
- [ ] Verify advisory get endpoint returns the correct status string in the response
- [ ] Verify advisory search includes status in results correctly
- [ ] Verify that response JSON shape matches the pre-migration format (backward compatibility)

## Verification Commands
- `cargo build -p fundamental` -- compiles without errors
- `cargo test -p fundamental` -- all module tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum

[sdlc-workflow] Description digest: sha256:c15c4bbb4e737bfec2a0af450aded66bbfee93cb453cbc57b4c60b9800ad8389
