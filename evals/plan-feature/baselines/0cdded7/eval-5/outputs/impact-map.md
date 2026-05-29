# Repository Impact Map -- TC-9005: Drop status table and migrate to enum column

## trustify-backend

### changes:
- Create a new database migration that defines the `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected), adds a `status` enum column to the `advisory` table, backfills it from the existing `advisory_status` join, drops the `status_id` foreign key column, and drops the `advisory_status` lookup table -- all within a single atomic migration
- Update the SeaORM entity definition in `entity/src/advisory.rs` to replace the `status_id` foreign key field with a `status` enum field of type `advisory_status_enum`
- Remove the SeaORM entity definition file `entity/src/advisory_status.rs` (the lookup table entity) and remove its module declaration from `entity/src/lib.rs`
- Update `AdvisorySummary` and `AdvisoryDetails` model structs in `modules/fundamental/src/advisory/model/` to use the enum status directly instead of joining the lookup table
- Update `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs` to query the `status` enum column directly, removing all joins to the `advisory_status` table
- Update advisory list and get endpoints in `modules/fundamental/src/advisory/endpoints/` to filter by enum column instead of join
- Update the advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` to write enum values directly instead of writing to the lookup table
- Update shared query helpers in `common/src/db/query.rs` if any advisory-status-specific filtering logic exists
- Update advisory integration tests in `tests/api/advisory.rs` to use enum status values and verify the join is no longer used

## Workflow Mode

**Selected mode:** `feature-branch`

**Rationale:** This feature exhibits multiple atomicity indicators:

1. **Coordinated schema migration** (indicator 1): The database migration drops the `advisory_status` table and the `status_id` column. If the migration lands without the code changes, all advisory queries will break because they still join the now-dropped table. If the code changes land without the migration, they reference a `status` enum column that does not exist.

2. **All-or-nothing requirement** (from non-functional requirements): The feature explicitly requires "All changes must land together: merging the migration without the code changes would break all advisory queries, and merging the code changes without the migration would reference a column that does not exist."

**Interdependent tasks:** The migration task, entity update task, service/endpoint update task, and ingestion pipeline task are all tightly coupled -- no subset can be merged to `main` independently without breaking the application.
