## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory HTTP endpoint handlers to remove any direct references to the advisory status join and ensure the status filter query parameter maps to the enum column. Verify that the API response shape remains unchanged so this is transparent to consumers.

## Files to Modify
- `modules/fundamental/src/advisory/endpoints/list.rs` — Update the status filter parameter handling to construct a filter on the `advisory.status` enum column instead of joining `advisory_status`
- `modules/fundamental/src/advisory/endpoints/get.rs` — Remove any status join references if present in the single-advisory fetch path
- `modules/fundamental/src/advisory/endpoints/mod.rs` — Update route registration if any query parameter types changed for status filtering

## Implementation Notes
- The list endpoint likely accepts a `status` query parameter for filtering. This must now filter on `advisory.status` enum column directly using `advisory_status_enum` value matching
- Ensure the `status` field in JSON responses is serialized as a lowercase or original-case string (matching current API behavior) — the `AdvisoryStatusEnum`'s `Display` or `Serialize` impl must produce the same strings as the old lookup table values
- No new routes are needed; this is purely an internal refactor of how status data is sourced and filtered
- Follow existing endpoint pattern: handlers return `Result<Json<T>, AppError>` with `.context()` wrapping

Per Key Conventions (Error handling): All handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` and `get.rs` matching the endpoint handler scope.

Per Key Conventions (Endpoint registration): Each module's `endpoints/mod.rs` registers routes. Applies: task modifies `modules/fundamental/src/advisory/endpoints/mod.rs` matching the endpoint registration scope.

Per Key Conventions (Response types): List endpoints return `PaginatedResults<T>`. Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` which returns paginated advisory results.

## Acceptance Criteria
- [ ] Advisory list endpoint supports status filtering via enum column
- [ ] Advisory detail endpoint returns status from enum column
- [ ] API response JSON shape is identical to the previous implementation
- [ ] No references to `advisory_status` entity or join remain in endpoint code
- [ ] Endpoints compile and route registration is unchanged

## Test Requirements
- [ ] Verify the module compiles: `cargo check -p trustify-module-fundamental`
- [ ] Verify GET /api/v2/advisory returns advisories with correct status strings
- [ ] Verify GET /api/v2/advisory?status=Fixed filters correctly
- [ ] Verify GET /api/v2/advisory/{id} returns the correct status

## Verification Commands
```bash
cargo check -p trustify-module-fundamental
```

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service layer and queries

[sdlc-workflow] Description digest: sha256-md:1102f2b1e4381914d9d4733e95365ff7042159616b16840f5abfa31add782ede
