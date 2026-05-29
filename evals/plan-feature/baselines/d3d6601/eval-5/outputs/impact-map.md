# Repository Impact Map

## Feature: TC-9005 — Drop status table and migrate to enum column

```
trustify-backend:
  changes:
    - Create PostgreSQL enum type advisory_status_enum with values (New, Analyzing, Fixed, Rejected)
    - Add status enum column to advisory table, backfill from existing status_id join
    - Drop status_id foreign key column from advisory table
    - Drop advisory_status lookup table
    - Update SeaORM entity definition for advisory to use enum column instead of FK relation
    - Remove advisory_status entity definition
    - Update AdvisoryService (fetch, list, search) to query status enum column directly instead of joining advisory_status table
    - Update advisory list and get endpoints to use new status column
    - Update advisory ingestion pipeline to write enum values directly instead of writing to lookup table
    - Update advisory integration tests to reflect new schema
```

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** Multiple atomicity indicators are present:

1. **Coordinated schema migration (indicator #1):** The migration creates an enum type, adds a column, backfills data, drops the foreign key column, and drops the lookup table. The code changes (entity definitions, service queries, ingestion pipeline) depend on the migration having completed. Merging the migration alone would drop the table that existing queries still join, breaking the application. Merging the code changes alone would reference a `status` column that does not exist.

2. **Breaking API changes (indicator #2):** The entity definition change (removing `advisory_status` relation, adding enum field) is consumed by the service layer and endpoints. Merging the entity change without updating the service layer would cause compilation failures. Merging the service layer changes without the entity change would reference fields that do not exist.

**Interdependent tasks:**
- The migration task creates the schema that all code tasks depend on
- The entity update task changes the data model that the service/endpoint/ingestion tasks consume
- The service and ingestion updates depend on both the migration and entity changes being present

All intermediate tasks must land on feature branch `TC-9005` and be merged to `main` atomically.

**Labels:** `workflow:feature-branch`
