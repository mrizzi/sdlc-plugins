# Repository Impact Map — TC-9005

## trustify-backend

```
trustify-backend:
  changes:
    - Create PostgreSQL enum type `advisory_status_enum` with values (New, Analyzing, Fixed, Rejected)
    - Add `status` enum column to `advisory` table, backfill from `status_id` join, drop `status_id` FK column, drop `advisory_status` lookup table (single atomic migration)
    - Update SeaORM entity `entity/advisory.rs` to replace `status_id` FK with `status` enum column
    - Remove SeaORM entity `entity/advisory_status.rs` (no longer needed)
    - Update `AdvisorySummary` and `AdvisoryDetails` model structs to use enum status field instead of join
    - Update `AdvisoryService` (fetch, list, search) to query `status` column directly instead of joining `advisory_status`
    - Update advisory list and get endpoints to use the new status column for filtering
    - Update advisory ingestion pipeline to write enum values directly instead of inserting into lookup table
    - Update advisory integration tests to reflect new schema and query patterns
```

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** The following atomicity indicators are present:

1. **Coordinated schema migration** — The database migration creates an enum type, adds a column, backfills data, drops a foreign key, and drops a table. The code changes (entity definitions, service layer, endpoints, ingestor) depend on the migration having completed. Merging the migration without the code changes would break all advisory queries (they still reference the old join). Merging the code changes without the migration would reference a column that does not exist.

2. **Cross-cutting refactor** — The removal of the `advisory_status` table and `status_id` foreign key touches the entity layer, service layer, endpoints, and ingestion pipeline simultaneously. Partial delivery would leave the codebase in an inconsistent state where some code joins on a dropped table.

**Interdependent tasks:** All intermediate tasks (migration, entity update, service/endpoint updates, ingestor update, test updates) are mutually dependent — none can be merged to `main` independently without breaking the application.
