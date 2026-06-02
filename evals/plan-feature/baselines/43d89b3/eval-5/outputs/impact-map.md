# Repository Impact Map — TC-9005

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** The following atomicity indicators were identified:

1. **Coordinated schema migrations** — The database migration creates the `advisory_status_enum` type, adds the `status` enum column, backfills data, drops the `status_id` FK column, and drops the `advisory_status` table. The code changes (entity definitions, service queries, ingestion pipeline) depend on the new column existing and the old table being removed. Merging the migration without the code changes would break all advisory queries (they still join the now-dropped table). Merging the code changes without the migration would reference a column that does not exist.
2. **Breaking API changes** — The entity layer changes (removing `advisory_status` entity, changing `advisory` entity from `status_id` FK to `status` enum) break the service and endpoint layers if applied independently.

**Interdependent tasks:** The migration task, entity update task, service/endpoint update task, and ingestion pipeline task are all mutually dependent — none can be merged to `main` independently without breaking the application.

## Impact Map

```
trustify-backend:
  changes:
    - Create database migration to add advisory_status_enum type, add status enum column to advisory table, backfill from status_id join, drop status_id FK column, and drop advisory_status table
    - Update SeaORM entity definitions: modify advisory entity to use status enum column, remove advisory_status entity
    - Update AdvisoryService queries and advisory endpoints to use the new status enum column instead of the advisory_status join
    - Update advisory ingestion pipeline to write enum status values directly instead of writing to the lookup table
    - Update advisory integration tests to reflect the new schema and query patterns
```

## Label Decision

Add label `workflow:feature-branch` to feature issue TC-9005.
