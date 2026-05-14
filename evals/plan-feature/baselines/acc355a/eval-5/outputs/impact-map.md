# Repository Impact Map — TC-9005

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** This feature has multiple atomicity indicators that require all changes to land together:

1. **Coordinated schema migrations** — The database migration creates an enum type, adds a new `status` column, backfills it from the joined `status_id` column, drops the `status_id` foreign key, and drops the `advisory_status` lookup table. The code changes (entity definitions, service layer, endpoints, ingestion pipeline) depend on this migration being present. Merging the migration without the code changes would break all advisory queries (they still join the now-dropped table). Merging the code changes without the migration would reference a column (`status` enum) that does not exist.

2. **Breaking API changes** — The advisory service and endpoints currently query via a join to `advisory_status`. After the migration drops that table, any code still referencing `status_id` or the join would fail. The entity definitions, service queries, and ingestion pipeline must all be updated atomically with the migration.

3. **Cross-cutting refactors** — The change touches entity definitions, service layer, endpoints, ingestion pipeline, and integration tests. Each depends on the same schema change, and partial delivery would leave the codebase in an inconsistent state.

**Interdependent tasks:** The migration task, entity update task, service/endpoint update task, and ingestion pipeline update task are all mutually dependent — none can be merged to `main` independently without breaking the application.

**Action:** Apply the `workflow:feature-branch` label to feature issue TC-9005.

---

## Impact Map

```
trustify-backend:
  changes:
    - Create feature branch TC-9005 from main
    - Create database migration to add advisory_status_enum type, add status enum column to advisory table, backfill from status_id join, drop status_id FK column, and drop advisory_status lookup table
    - Update SeaORM entity definitions: modify entity/src/advisory.rs to replace status_id FK with status enum column, remove entity/src/advisory_status.rs, update entity/src/lib.rs exports
    - Update advisory service layer and endpoints to query using the new status enum column instead of joining advisory_status table
    - Update advisory ingestion pipeline to write enum values directly instead of inserting into lookup table
    - Update advisory integration tests to reflect new schema (no join, direct enum filtering)
    - Merge feature branch TC-9005 to main
```
