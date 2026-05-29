# Repository Impact Map

**Feature:** TC-9005 -- Drop status table and migrate to enum column
**Workflow Mode:** feature-branch

## trustify-backend

### changes:
- Create database migration to define `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected), add `status` enum column to `advisory` table, backfill from `advisory_status` join, drop `status_id` FK column, and drop `advisory_status` lookup table -- all in a single atomic migration
- Update SeaORM entity definition in `entity/src/advisory.rs` to replace `status_id` foreign key field with `status` enum field mapped to `advisory_status_enum`
- Remove SeaORM entity file `entity/src/advisory_status.rs` and its registration in `entity/src/lib.rs`
- Update `AdvisorySummary` and `AdvisoryDetails` model structs in `modules/fundamental/src/advisory/model/` to use the new enum `status` field instead of joining through `advisory_status`
- Update `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs` to query the `status` enum column directly, eliminating the `advisory_status` table join
- Update advisory list and get endpoints in `modules/fundamental/src/advisory/endpoints/` to filter by the new enum column
- Update shared query builder helpers in `common/src/db/query.rs` if advisory status filtering logic exists there
- Update advisory ingestion logic in `modules/ingestor/src/graph/advisory/mod.rs` to write enum values directly instead of inserting into the lookup table
- Update advisory integration tests in `tests/api/advisory.rs` to reflect the new schema and query patterns

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** Multiple atomicity indicators are present:

1. **Coordinated schema migration** -- The database migration adds the `status` enum column and drops the `advisory_status` table. All code changes (entity definitions, service layer, endpoints, ingestion) depend on this migration being present. Merging the migration without the code changes would break all advisory queries (they still join the now-dropped table). Merging the code changes without the migration would reference a column that does not exist.

2. **Breaking API contract (internal)** -- The entity layer change (removing `advisory_status.rs`, changing `advisory.rs`) is consumed by the service layer, endpoints, and ingestor. Partial delivery would leave the codebase in an inconsistent state where some modules reference the old schema and others reference the new one.

**Interdependent tasks:** All implementation tasks are interdependent -- the migration task, entity update task, service/endpoint update task, and ingestion update task must all land on the same branch before merging to `main`.
