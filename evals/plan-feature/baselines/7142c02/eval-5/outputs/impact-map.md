# Repository Impact Map — TC-9005

## Workflow Mode: feature-branch

**Rationale:** The feature exhibits coordinated schema migration atomicity — the database migration adds an enum column and drops the lookup table, while the code changes update all advisory queries, service logic, and ingestion pipeline to use the new column. The non-functional requirements explicitly state that "all changes must land together" because merging the migration without the code changes would break advisory queries (they still join the now-dropped table), and merging the code changes without the migration would reference a column that does not exist. This satisfies atomicity indicator #1 (coordinated schema migrations) and #2 (breaking API changes between migration and code layers).

The `workflow:feature-branch` label will be applied to the TC-9005 feature issue.

## trustify-backend

```
trustify-backend:
  changes:
    - Create PostgreSQL enum type `advisory_status_enum` with values (New, Analyzing, Fixed, Rejected)
    - Add `status` enum column to `advisory` table, backfill from existing `status_id` join
    - Drop `status_id` foreign key column from `advisory` table
    - Drop `advisory_status` lookup table
    - Update SeaORM entity definition in `entity/src/advisory.rs` to use enum `status` column
    - Remove SeaORM entity file for the dropped `advisory_status` table
    - Update `AdvisorySummary` and `AdvisoryDetails` model structs to use enum status field
    - Update `AdvisoryService` (fetch, list, search) to query `status` enum column directly instead of joining `advisory_status`
    - Update advisory list and get endpoints to use enum status for filtering
    - Update shared query builder helpers if advisory status filtering is implemented there
    - Update advisory ingestion pipeline to write enum values directly instead of lookup table insert
    - Update advisory integration tests to exercise enum status filtering and ingestion
```
