## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer, HTTP endpoints, and ingestion pipeline to use the new `status` enum column instead of joining the `advisory_status` lookup table. This eliminates the join from all advisory queries, simplifies the ingestion pipeline to write enum values directly, and updates the advisory model structs to reflect the new schema. Update integration tests to verify the new behavior.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove `advisory_status` table joins from fetch, list, and search queries; filter and select directly on `advisory.status` enum column
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to source status from enum field instead of joined table
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct to source status from enum field instead of joined table
- `modules/fundamental/src/advisory/model/mod.rs` — update any status-related type imports or re-exports
- `modules/fundamental/src/advisory/endpoints/list.rs` — update status filter query to use enum column directly (`WHERE status = 'Fixed'` instead of join-based filter)
- `modules/fundamental/src/advisory/endpoints/get.rs` — update single advisory fetch to use enum column
- `modules/ingestor/src/graph/advisory/mod.rs` — update advisory ingestion to write `AdvisoryStatusEnum` value directly instead of inserting into lookup table and using FK
- `tests/api/advisory.rs` — update integration tests to reflect new schema (no advisory_status table, enum-based status)

## Implementation Notes
- In `advisory.rs` service, remove all `Join` or `find_also_related` calls to `advisory_status::Entity`. Replace with direct column access on `advisory::Column::Status`
- For status filtering in list endpoint, use `advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed)` pattern instead of joining and filtering on the lookup table
- In `AdvisorySummary` and `AdvisoryDetails` structs, change the status field type from the old joined model type to `AdvisoryStatusEnum` (imported from `entity::advisory`)
- Follow the existing query pattern in `common/src/db/query.rs` for filtering and pagination — the shared query builder helpers should continue to work with the enum column
- Follow the existing list endpoint pattern in `modules/fundamental/src/sbom/endpoints/list.rs` for how list queries use `PaginatedResults<T>` from `common/src/model/paginated.rs`
- In the ingestion pipeline (`modules/ingestor/src/graph/advisory/mod.rs`), map the status string from the advisory feed directly to `AdvisoryStatusEnum` variant instead of looking up or inserting into the `advisory_status` table
- For error handling, follow the existing `Result<T, AppError>` pattern with `.context()` wrapping as used throughout the modules
- Integration tests in `tests/api/advisory.rs` should verify status filtering returns correct results using the enum column, following the existing test pattern in `tests/api/sbom.rs`

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting that should continue to work with the enum column
- `common/src/model/paginated.rs` — `PaginatedResults<T>` wrapper used by list endpoints
- `common/src/error.rs` — `AppError` enum for error handling pattern
- `modules/fundamental/src/sbom/service/sbom.rs` — demonstrates the service pattern (fetch, list) without join-based status lookup, useful as reference for simplified advisory queries
- `modules/fundamental/src/sbom/endpoints/list.rs` — demonstrates the list endpoint pattern with filtering and pagination
- `tests/api/sbom.rs` — demonstrates the integration test pattern for endpoint testing

## Acceptance Criteria
- [ ] All advisory queries (list, fetch, search) use `advisory.status` enum column directly without joining `advisory_status` table
- [ ] Advisory list endpoint supports status filtering using the enum column
- [ ] Advisory ingestion pipeline writes enum values directly without lookup table interaction
- [ ] `AdvisorySummary` and `AdvisoryDetails` models reflect the enum-based status field
- [ ] No remaining references to `advisory_status` entity or table in the fundamental or ingestor modules
- [ ] Integration tests pass with the new schema
- [ ] API response shape remains unchanged (status is still a string)

## Test Requirements
- [ ] Integration test: GET /api/v2/advisory returns advisories with status as string (response shape unchanged)
- [ ] Integration test: GET /api/v2/advisory with status filter returns correctly filtered results using enum column
- [ ] Integration test: GET /api/v2/advisory/{id} returns advisory detail with correct enum status
- [ ] Integration test: advisory ingestion writes enum status value correctly
- [ ] Verify no join to advisory_status table in any query (code review / grep verification)

## Verification Commands
- `cargo build --workspace` — full workspace builds without errors
- `cargo test -p modules-fundamental` — fundamental module tests pass
- `cargo test -p modules-ingestor` — ingestor module tests pass
- `cargo test --test api` — integration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main


[sdlc-workflow] Description digest: sha256:92d6cb294f487fc5b2e0f475f0cd961dc104200d0c384e683e79da338bbd1456
