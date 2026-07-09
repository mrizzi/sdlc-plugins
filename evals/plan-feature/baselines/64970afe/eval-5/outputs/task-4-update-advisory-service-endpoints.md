## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and HTTP endpoints to query the `advisory.status` enum column directly, eliminating the join with the now-removed `advisory_status` lookup table. This covers the AdvisoryService (fetch, list, search methods), the advisory list endpoint (`GET /api/v2/advisory`), and the advisory get endpoint (`GET /api/v2/advisory/{id}`). The external response shape remains unchanged -- status is still returned as a string to maintain API backward compatibility.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` -- remove join with `advisory_status` table; query `advisory.status` enum column directly for filtering and selection
- `modules/fundamental/src/advisory/model/summary.rs` -- update `AdvisorySummary` struct to source status from the enum field instead of the joined table
- `modules/fundamental/src/advisory/model/details.rs` -- update `AdvisoryDetails` struct to source status from the enum field
- `modules/fundamental/src/advisory/endpoints/list.rs` -- update status filter parameter handling to compare against enum values directly
- `modules/fundamental/src/advisory/endpoints/get.rs` -- update single advisory retrieval to use enum status field

## Implementation Notes
- In `advisory.rs` service, replace any `join` or `inner_join` with the `advisory_status` table with direct column access on `advisory::Column::Status`. For status filtering in list queries, use SeaORM's `Condition` with enum value comparison: `advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed)` instead of joining and filtering on the lookup table's name column.
- The `AdvisorySummary` and `AdvisoryDetails` structs should derive the status field value from `advisory.status` directly. The serialized output remains a string (e.g., "Fixed") for API backward compatibility -- SeaORM's `DeriveActiveEnum` with `string_value` attributes handles this serialization automatically.
- Remove any `use` imports referencing the `advisory_status` entity module.
- Per CONVENTIONS.md §Error handling: all handlers must return `Result<T, AppError>` with `.context()` wrapping for error propagation.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's handler file scope.
- Per CONVENTIONS.md §Response types: list endpoints must return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's endpoint file scope.
- Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs` for advisory list queries.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's service query file scope.
- Reference `modules/fundamental/src/sbom/service/sbom.rs` for the established service query pattern using direct column access without lookup table joins.

## Reuse Candidates
- `common/src/db/query.rs` -- shared query builder helpers for filtering and pagination, already used by advisory service queries
- `common/src/model/paginated.rs` -- `PaginatedResults<T>` response wrapper for list endpoints
- `common/src/error.rs` -- `AppError` enum and `IntoResponse` implementation for error handling
- `modules/fundamental/src/sbom/service/sbom.rs` -- sibling service demonstrating direct column queries without lookup table joins

## Acceptance Criteria
- [ ] Advisory list endpoint (`GET /api/v2/advisory`) returns correct results when filtering by status
- [ ] Advisory get endpoint (`GET /api/v2/advisory/{id}`) returns advisory with correct status string
- [ ] No queries reference the `advisory_status` table or use a join for status resolution
- [ ] Response JSON shape is unchanged -- status remains a string field in the API response
- [ ] Endpoint latency improves due to eliminated join (target: ~40ms p95 reduction on advisory list)

## Test Requirements
- [ ] Verify advisory list endpoint returns all advisories when no status filter is applied
- [ ] Verify advisory list endpoint correctly filters by each status value (New, Analyzing, Fixed, Rejected)
- [ ] Verify advisory get endpoint returns the correct status string for a specific advisory
- [ ] Verify response JSON shape matches the previous format (backward compatibility check)

## Verification Commands
- `cargo test -p fundamental` -- fundamental module tests pass
- `cargo build -p fundamental` -- module compiles successfully

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
