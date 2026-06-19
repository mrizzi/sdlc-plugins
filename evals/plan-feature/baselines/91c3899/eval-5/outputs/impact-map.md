# Repository Impact Map

## Feature: TC-9005 — Drop status table and migrate to enum column

## Workflow Mode: feature-branch

### Rationale

The feature requires **feature-branch** mode based on the following atomicity indicators:

1. **Coordinated schema migrations** — The database migration adds a new enum type and column, backfills data, drops the foreign key column, and drops the `advisory_status` lookup table. The migration must be atomic: if any step fails, the entire migration rolls back. A partial migration would leave the database in an inconsistent state.

2. **Breaking API changes (cross-cutting)** — All advisory queries currently join the `advisory_status` table. Merging the migration without the code changes would break all advisory queries (they still join the now-dropped table). Merging the code changes without the migration would reference a column (`status`) that does not exist. The Non-Functional Requirements explicitly state: "All changes must land together."

These constraints mean no individual task PR can land on `main` independently without breaking the application. All changes must be developed on a feature branch and merged together.

### Label Decision

Add label `workflow:feature-branch` to feature issue TC-9005 after all tasks are created.

---

## Impact Map

```
trustify-backend:
  changes:
    - Create PostgreSQL enum type `advisory_status_enum` with values (New, Analyzing, Fixed, Rejected)
    - Add `status` enum column to `advisory` table, backfill from `status_id` join
    - Drop `status_id` foreign key column from `advisory` table
    - Drop `advisory_status` lookup table
    - Update SeaORM entity definition for `advisory` to use enum column; remove `advisory_status` entity
    - Update AdvisoryService queries to use `status` column instead of join
    - Update advisory list and get endpoints to use new status column
    - Update advisory ingestion pipeline to write enum values directly
    - Add/update integration tests for advisory endpoints with new status column
```

## Task Summary

| # | Task | Target Branch | Type |
|---|---|---|---|
| 1 | Create feature branch TC-9005 from main | main | bookend (create-branch) |
| 2 | Create database migration for advisory status enum | TC-9005 | intermediate |
| 3 | Update SeaORM entity definitions for advisory status enum | TC-9005 | intermediate |
| 4 | Update advisory service and endpoints to use status enum | TC-9005 | intermediate |
| 5 | Update advisory ingestion pipeline for status enum | TC-9005 | intermediate |
| 6 | Add integration tests for advisory status enum migration | TC-9005 | intermediate |
| 7 | Merge feature branch TC-9005 to main | main | bookend (merge-branch) |
