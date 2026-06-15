# Repository Impact Map — TC-9005

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** Multiple atomicity indicators are present:

1. **Coordinated schema migrations** — The migration creates an enum type, adds a new `status` column, backfills data from the `advisory_status` join, drops the `status_id` FK column, and drops the `advisory_status` table. The code changes in the service layer, endpoints, and ingestion pipeline depend on the new column existing and the old table being absent. Merging the migration alone would break all advisory queries that still join the now-dropped table. Merging the code changes alone would reference a `status` column that does not yet exist.

2. **Breaking API changes** — The advisory service, endpoint handlers, and ingestion pipeline all switch from joining `advisory_status` via `status_id` to reading the `status` enum column directly. These code changes are tightly coupled to the migration: neither side functions correctly without the other.

3. **Cross-cutting refactors** — The entity layer change (removing `advisory_status.rs`, modifying `advisory.rs`) affects every module that imports or references the advisory status entity. Partial delivery would leave imports and type references in an inconsistent state.

**Interdependent tasks:** All intermediate tasks (migration, entity updates, service/endpoint updates, ingestion updates, integration tests) are mutually dependent — each assumes the schema state produced by the migration and the entity definitions from the entity update.

**Label decision:** Apply `workflow:feature-branch` label to feature issue TC-9005.

---

## Impact Map

```
trustify-backend:
  changes:
    - Create PostgreSQL enum type advisory_status_enum and migration to add status column, backfill from advisory_status join, drop status_id FK column, and drop advisory_status table
    - Update SeaORM entity definition for advisory to use enum status column and remove advisory_status entity
    - Update AdvisoryService (fetch, list, search) to query status column directly instead of joining advisory_status table
    - Update advisory endpoint handlers (list, get) to use new status field without join
    - Update advisory ingestion pipeline to write enum values directly instead of writing to lookup table
    - Update integration tests for advisory endpoints to reflect schema and query changes
```
