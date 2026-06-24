## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and model structs to use the new `status` enum column instead of joining the `advisory_status` lookup table. Remove all join logic for advisory status from query construction and update the AdvisorySummary and AdvisoryDetails model structs to source status from the enum column directly.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — Remove `advisory_status` table joins from all query methods (fetch, list, search); read `status` directly from the `advisory` entity column
- `modules/fundamental/src/advisory/model/summary.rs` — Update `AdvisorySummary` struct: change `status` field source from a joined lookup value to the entity's enum field
- `modules/fundamental/src/advisory/model/details.rs` — Update `AdvisoryDetails` struct similarly if it references the status join
- `modules/fundamental/src/advisory/model/mod.rs` — Update any shared model re-exports or type aliases related to status

## Implementation Notes
- In `advisory.rs` service, all `.join()` or `.find_also_related()` calls referencing the `advisory_status` entity must be removed
- The `status` field in query results comes directly from `advisory::Model::status` which is now an `AdvisoryStatusEnum`
- When constructing `AdvisorySummary`, convert the enum to its string representation for API compatibility (e.g., `status.to_string()` or `status.to_value()`)
- Status filtering in the list endpoint's query builder should change from joining + filtering on `advisory_status.name` to filtering directly on `advisory.status` using the enum value
- Follow the existing error handling pattern: all service methods return `Result<T, AppError>` with `.context()` wrapping per `common/src/error.rs`
- Use shared query helpers from `common/src/db/query.rs` for pagination and sorting — these should not need changes since they operate on the primary table

Per Key Conventions (Error handling): All service methods must return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the service scope.

Per Key Conventions (Module pattern): Each domain module follows `model/ + service/ + endpoints/` structure. Applies: task modifies advisory `model/` and `service/` files matching the module pattern scope.

Per Key Conventions (Response types): List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` which builds paginated results.

Per Key Conventions (Query helpers): Shared filtering, pagination, and sorting via `common/src/db/query.rs`. Applies: task modifies advisory service query construction matching the query helpers scope.

## Acceptance Criteria
- [ ] No references to `advisory_status` table or entity remain in advisory service code
- [ ] Advisory list and fetch queries no longer perform a join for status
- [ ] `AdvisorySummary` and `AdvisoryDetails` structs correctly populate status from the enum column
- [ ] Status filtering works directly on the enum column
- [ ] API response shape for advisory endpoints is unchanged (status is still a string)
- [ ] The module compiles without errors

## Test Requirements
- [ ] Verify the fundamental module compiles: `cargo check -p trustify-module-fundamental`
- [ ] Verify advisory list returns correct status strings from the enum column
- [ ] Verify status filtering produces correct results

## Verification Commands
```bash
cargo check -p trustify-module-fundamental
```

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions

[sdlc-workflow] Description digest: sha256-md:79dc8009905fdc80c2fb7f9d69c5fd96bded2dd5c401ccad1f693e537bf658d8
