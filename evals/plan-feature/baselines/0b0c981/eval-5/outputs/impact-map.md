# Repository Impact Map

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** The following atomicity indicators were identified:

1. **Coordinated schema migrations** — The database migration creates a new `advisory_status_enum` type, adds a `status` enum column, backfills data, drops the `status_id` foreign key, and drops the `advisory_status` lookup table. All code changes depend on this migration having run; merging the migration alone would leave the old code joining a table that may be in an intermediate state.
2. **Tightly coupled feature components** — The feature description explicitly states: "merging the migration without the code changes would break all advisory queries (they still join the now-dropped table), and merging the code changes without the migration would reference a column that does not exist." The entity definitions, service layer, endpoints, and ingestion pipeline all depend on the new schema, and none can function independently of the migration.

**Interdependent tasks:** The migration task, entity update task, service/endpoint update task, and ingestion pipeline update task are all mutually dependent — partial delivery of any subset would leave `main` in a broken state.

---

## Impact Map

```
trustify-backend:
  changes:
    - Create PostgreSQL enum type `advisory_status_enum` with values (New, Analyzing, Fixed, Rejected)
    - Add `status` enum column to `advisory` table and backfill from `status_id` join
    - Drop `status_id` foreign key column from `advisory` table
    - Drop `advisory_status` lookup table
    - Update SeaORM entity definition in `entity/src/advisory.rs` to replace `status_id` FK with `status` enum column
    - Remove `entity/src/advisory_status.rs` entity file (lookup table entity no longer needed)
    - Update `entity/src/lib.rs` to remove `advisory_status` module export
    - Update `modules/fundamental/src/advisory/model/summary.rs` to read status from enum column instead of join
    - Update `modules/fundamental/src/advisory/model/details.rs` to read status from enum column instead of join
    - Update `modules/fundamental/src/advisory/service/advisory.rs` to remove advisory_status join from all queries
    - Update `modules/fundamental/src/advisory/endpoints/list.rs` to filter by enum column instead of join
    - Update `modules/fundamental/src/advisory/endpoints/get.rs` if it references status via join
    - Update `modules/ingestor/src/graph/advisory/mod.rs` to write enum values directly instead of inserting into lookup table
    - Update `tests/api/advisory.rs` integration tests to reflect new schema and query patterns
```
