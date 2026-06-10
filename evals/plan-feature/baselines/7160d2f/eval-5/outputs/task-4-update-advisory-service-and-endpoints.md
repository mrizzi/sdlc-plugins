## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and endpoints to query the `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead on every advisory query, which is the primary performance goal of TC-9005 (reducing p95 latency by ~40ms on the advisory list endpoint).

## Files to Modify
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to use enum status field instead of joined status string
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct to use enum status field
- `modules/fundamental/src/advisory/model/mod.rs` — update module-level imports if needed to remove advisory_status entity references
- `modules/fundamental/src/advisory/service/advisory.rs` — update `AdvisoryService` fetch, list, and search methods to remove `advisory_status` join and query `status` column directly; update status filtering to compare against enum values
- `modules/fundamental/src/advisory/endpoints/list.rs` — update list endpoint to use enum-based status filtering (e.g., `WHERE status = 'Fixed'` instead of joining)
- `modules/fundamental/src/advisory/endpoints/get.rs` — update get endpoint to read status from the enum column

## Implementation Notes
- In `AdvisoryService` (advisory.rs), remove all `.join()` or `.find_also_related()` calls that reference `advisory_status::Entity`. Replace with direct column access on `advisory::Column::Status`.
- For status filtering in the list endpoint, use `advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed)` instead of joining and filtering on the lookup table.
- The response shape to API consumers must remain identical — status is still serialized as a string (e.g., `"Fixed"`). The `AdvisoryStatusEnum` should implement `Serialize` to produce the same string values. Verify that `#[derive(Serialize)]` on the enum with `#[serde(rename = "...")]` or default variant naming produces the correct output.
- In the model structs (`AdvisorySummary`, `AdvisoryDetails`), replace any `status: String` field (previously populated from the join) with `status: AdvisoryStatusEnum` and ensure the serialization output is unchanged.
- Use the query builder helpers in `common/src/db/query.rs` for filtering and pagination — these are shared across all list endpoints.
- Reference the SBOM service pattern in `modules/fundamental/src/sbom/service/sbom.rs` for the expected service method structure.
- Reference the SBOM list endpoint in `modules/fundamental/src/sbom/endpoints/list.rs` for the expected endpoint pattern.
- Per docs/constraints.md §2 (Commit Rules): commit must reference TC-9005 in footer, use Conventional Commits format, and include `--trailer="Assisted-by: Claude Code"`.
- Per docs/constraints.md §5 (Code Change Rules): inspect existing service and endpoint code before modifying; follow established patterns.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; reuse for status filter integration
- `modules/fundamental/src/sbom/service/sbom.rs` — reference for service method patterns (fetch, list) without join tables
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for list endpoint patterns with `PaginatedResults<T>`
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper used by all list endpoints

## Acceptance Criteria
- [ ] `AdvisoryService` no longer joins `advisory_status` table in any query
- [ ] Advisory list endpoint supports status filtering using the enum column directly
- [ ] Advisory get endpoint returns status from the enum column
- [ ] API response shape is unchanged — status field is still a string in JSON responses
- [ ] No references to `advisory_status` entity remain in the advisory module
- [ ] All advisory module code compiles without errors

## Test Requirements
- [ ] Run `cargo build -p fundamental` to verify compilation
- [ ] Run `cargo test -p fundamental` to verify no test regressions
- [ ] Verify that the advisory list endpoint correctly filters by enum status values

## Verification Commands
- `cargo build -p fundamental` — expected: compiles without errors
- `cargo test -p fundamental` — expected: all existing tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
