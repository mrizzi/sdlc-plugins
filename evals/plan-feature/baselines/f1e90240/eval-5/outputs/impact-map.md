# Repository Impact Map -- TC-9005

## trustify-backend

### changes:
- Create PostgreSQL enum type `advisory_status_enum` with values (New, Analyzing, Fixed, Rejected) via a new SeaORM migration
- Add `status` enum column to `advisory` table, backfill from existing `status_id` join, drop `status_id` FK column, and drop `advisory_status` lookup table -- all in a single atomic migration
- Update SeaORM entity definition in `entity/src/advisory.rs` to replace `status_id: i32` foreign key field with `status: AdvisoryStatusEnum` enum field
- Remove SeaORM entity file `entity/src/advisory_status.rs` (lookup table entity no longer needed) and remove its re-export from `entity/src/lib.rs`
- Update `AdvisorySummary` and `AdvisoryDetails` model structs in `modules/fundamental/src/advisory/model/` to use the new enum field instead of joined status
- Update `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs` to query `advisory.status` directly instead of joining `advisory_status`
- Update advisory list and get endpoints in `modules/fundamental/src/advisory/endpoints/` to filter by enum column instead of join
- Update advisory ingestion in `modules/ingestor/src/graph/advisory/mod.rs` to write enum values directly instead of inserting into lookup table
- Update query helpers in `common/src/db/query.rs` if advisory status filtering is implemented there
- Update advisory integration tests in `tests/api/advisory.rs` to use the new enum-based status filtering
- Update internal architecture documentation to reflect schema change

## Workflow Mode

**Selected mode:** `feature-branch`

**Rationale:** Multiple atomicity indicators are present:

1. **Coordinated schema migration:** The database migration adds the `status` enum column and drops the `status_id` FK column and `advisory_status` table. All code changes (entity definitions, service layer, endpoints, ingestion) depend on this new schema. Merging the migration alone would break all advisory queries that still join the dropped table; merging code changes alone would reference a column that does not exist.

2. **All-or-nothing delivery requirement:** The feature's non-functional requirements explicitly state "all changes must land together." The entity, service, endpoint, and ingestion changes are tightly coupled to the migration -- partial delivery leaves the codebase in an inconsistent state.

**Interdependent tasks:** All implementation tasks (migration, entity update, service/endpoint update, ingestion update, test update) are interdependent because each depends on the schema change and the entity definition change. No single task can be merged to `main` independently without breaking the build.

## Label Decision

Apply label `workflow:feature-branch` to feature issue TC-9005.
