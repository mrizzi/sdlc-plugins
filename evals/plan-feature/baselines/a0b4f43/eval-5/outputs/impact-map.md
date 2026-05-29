# Repository Impact Map — TC-9005

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** Multiple atomicity indicators are present:

1. **Coordinated schema migrations** — The database migration creates a new enum type, adds a column, backfills data, drops a foreign key column, and drops a lookup table. The code changes (entity definitions, service layer, endpoints, ingestion pipeline) depend on the migration having completed. Merging the migration without the code changes would break all advisory queries (they still join the now-dropped table). Merging the code changes without the migration would reference a column (`status`) that does not exist.

2. **Breaking API changes** — Removing the `advisory_status` table and the `status_id` FK column is a breaking change for every advisory query in the codebase. All service-layer queries, endpoint handlers, and the ingestion pipeline must be updated simultaneously.

3. **Tightly coupled feature components** — The entity definition changes (removing `advisory_status.rs`, modifying `advisory.rs`), service layer changes, endpoint changes, and ingestion pipeline changes are all interdependent. No subset of these changes functions correctly without the others.

**Interdependent tasks:**
- The migration task creates the schema that all other tasks depend on
- Entity definition updates depend on the migration and are consumed by service/endpoint/ingestion tasks
- Service layer updates depend on entity definitions and are consumed by endpoint tasks
- Ingestion pipeline updates depend on entity definitions
- Test updates depend on all code changes being in place

## Impact Map

```
trustify-backend:
  changes:
    - Create database migration: add advisory_status_enum type, add status enum column to advisory table, backfill from status_id join, drop status_id FK column, drop advisory_status lookup table
    - Update SeaORM entity entity/advisory.rs: replace status_id integer FK with status enum column using advisory_status_enum
    - Remove SeaORM entity entity/advisory_status.rs and deregister from entity/src/lib.rs
    - Update advisory model structs (AdvisorySummary, AdvisoryDetails) to use enum status field directly instead of joined status
    - Update AdvisoryService to query advisory.status column directly, removing advisory_status table join
    - Update advisory list and get endpoint handlers to filter and return enum status values
    - Update advisory ingestion pipeline to write advisory_status_enum values directly instead of inserting into lookup table
    - Update advisory integration tests to reflect new schema and query patterns
```
