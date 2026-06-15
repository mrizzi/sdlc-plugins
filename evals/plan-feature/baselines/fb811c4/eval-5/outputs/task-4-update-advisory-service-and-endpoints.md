## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and REST endpoints to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join from all advisory queries, reducing the advisory list endpoint p95 latency by approximately 40ms.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — Remove all joins to `advisory_status` table; update queries to filter and select on the `status` enum column directly using `AdvisoryStatusEnum`
- `modules/fundamental/src/advisory/model/summary.rs` — Update `AdvisorySummary` struct to source the status field from the enum column instead of the joined lookup table; adjust `From` impl to map from `AdvisoryStatusEnum`
- `modules/fundamental/src/advisory/model/details.rs` — Update `AdvisoryDetails` struct similarly to use the enum status field
- `modules/fundamental/src/advisory/model/mod.rs` — Update module-level re-exports if status type references change
- `modules/fundamental/src/advisory/endpoints/list.rs` — Update `GET /api/v2/advisory` handler to apply status filters against the enum column instead of joining; update any query parameter parsing for status filter values
- `modules/fundamental/src/advisory/endpoints/get.rs` — Update `GET /api/v2/advisory/{id}` handler to read status from the enum column
- `modules/fundamental/src/advisory/endpoints/mod.rs` — Update route registration if any status-related sub-routes reference the lookup table
- `common/src/db/query.rs` — Update any shared query builder helpers that reference advisory status filtering to use the enum column

## Implementation Notes
Follow the existing query pattern in `modules/fundamental/src/advisory/service/advisory.rs` for building SeaORM queries. The current code likely uses `.find_also_related(advisory_status::Entity)` or similar join patterns — replace these with direct column access on `advisory::Column::Status`.

For status filtering in endpoints, follow the filter pattern in `common/src/db/query.rs` for building WHERE clauses. The enum column filter will use `advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed)` instead of a join-based subquery.

The response shape for `AdvisorySummary` and `AdvisoryDetails` must remain identical — status is still returned as a string to API consumers. Use `serde(rename_all)` or explicit `Serialize` impl to ensure the enum serializes to the same string values as before.

Follow the error handling pattern in `common/src/error.rs` — all handlers return `Result<T, AppError>` with `.context()` wrapping.

List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs` — ensure the paginated response wrapper continues to work with the updated model structs.

## Acceptance Criteria
- [ ] All advisory queries no longer join the `advisory_status` table
- [ ] `GET /api/v2/advisory` returns advisories with status from the enum column
- [ ] `GET /api/v2/advisory/{id}` returns advisory details with status from the enum column
- [ ] Status filter query parameter works correctly against the enum column
- [ ] API response shape is unchanged — status is still a string value (New, Analyzing, Fixed, Rejected)
- [ ] Project compiles with `cargo check`

## Test Requirements
- [ ] Update existing tests in `tests/api/advisory.rs` to verify status filtering works with enum values
- [ ] Add a test that filters advisories by each status value and verifies correct results
- [ ] Verify the API response JSON structure is unchanged (backward compatibility)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005
- Depends on: Task 3 — Update SeaORM entity definitions

[sdlc-workflow] Description digest: sha256-md:57673b5191a7064632aa6530e2b213250c4208abf23c246775d3e5e08d03ace5
