# Repository Impact Map — TC-9005

## Feature

**TC-9005**: Drop status table and migrate to enum column

## Workflow Mode

**feature-branch**

### Rationale

The following atomicity indicators are present:

1. **Coordinated schema migrations** — The database migration creates the `advisory_status_enum` type, adds the `status` enum column, backfills data, and drops the `status_id` FK column and `advisory_status` table. The code changes (entity definitions, service queries, ingestion pipeline) depend on the new column existing and the old column/table being absent. Merging the migration without the code changes would break all advisory queries (they still join the now-dropped table). Merging the code changes without the migration would reference a column that does not exist.

2. **Breaking API changes** — Removing the `advisory_status` lookup table and the `status_id` foreign key column breaks every query that joins `advisory` to `advisory_status`. The service layer, endpoints, and ingestion pipeline all must be updated atomically with the migration.

### Interdependent tasks

- The migration task (enum type creation, column addition, backfill, FK/table drop) and the entity update task are tightly coupled: entities must reflect the new schema.
- The service/query update task depends on both the migration and entity changes.
- The ingestion pipeline update depends on the entity changes.
- The endpoint/test updates depend on the service layer changes.

All intermediate tasks are interdependent and must land together on a feature branch before merging to main.

## Label Decision

Add `workflow:feature-branch` label to feature issue TC-9005.

---

## Impact Map

```
trustify-backend:
  changes:
    - Create database migration: define advisory_status_enum PostgreSQL enum type, add status enum column to advisory table, backfill from status_id join, drop status_id FK column, drop advisory_status table
    - Update SeaORM entity definitions: modify entity/src/advisory.rs to replace status_id FK with status enum field, remove entity/src/advisory_status.rs, update entity/src/lib.rs exports
    - Update advisory service layer: modify advisory queries in modules/fundamental/src/advisory/service/advisory.rs to use status enum column instead of advisory_status join
    - Update advisory model structs: modify AdvisorySummary and AdvisoryDetails to use enum status field instead of joined status
    - Update advisory ingestion pipeline: modify modules/ingestor/src/graph/advisory/mod.rs to write enum values directly instead of inserting into lookup table
    - Update advisory endpoints: modify list and get endpoints to filter/return status from enum column
    - Update integration tests: modify tests/api/advisory.rs to test against new enum-based status field
```
