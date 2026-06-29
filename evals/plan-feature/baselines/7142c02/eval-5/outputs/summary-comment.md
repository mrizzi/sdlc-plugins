# Implementation Plan Summary — TC-9005: Drop status table and migrate to enum column

## Workflow Mode
**feature-branch** — The `workflow:feature-branch` label will be applied to the TC-9005 feature issue. This feature requires all changes to land together because the database migration and code changes are tightly coupled: merging the migration without the code changes would break all advisory queries (they still join the now-dropped table), and merging the code changes without the migration would reference a column that does not exist. This satisfies the coordinated schema migration atomicity indicator.

## Tasks Created

| # | Task | Repository | Target Branch | Type |
|---|---|---|---|---|
| 1 | Create feature branch TC-9005 from main | trustify-backend | main | Bookend (create-branch) |
| 2 | Create database migration for advisory status enum | trustify-backend | TC-9005 | Implementation |
| 3 | Update SeaORM entity definitions for advisory status enum | trustify-backend | TC-9005 | Implementation |
| 4 | Update advisory service and endpoints to use enum status | trustify-backend | TC-9005 | Implementation |
| 5 | Update advisory ingestion pipeline to write enum status directly | trustify-backend | TC-9005 | Implementation |
| 6 | Update integration tests for advisory status enum migration | trustify-backend | TC-9005 | Implementation |
| 7 | Merge feature branch TC-9005 to main | trustify-backend | main | Bookend (merge-branch) |

## Repositories Affected
- **trustify-backend** — All changes are in a single repository

## Architecture Summary
This feature replaces the `advisory_status` lookup table with a PostgreSQL enum column (`advisory_status_enum`) directly on the `advisory` table. The change spans four layers of the codebase:

1. **Database layer**: A reversible migration creates the enum type, adds the `status` column, backfills from the existing FK join, drops the FK column, and drops the lookup table.
2. **Entity layer**: SeaORM entity definitions are updated to use the enum field, and the `advisory_status` entity is removed.
3. **Service/Endpoint layer**: All advisory queries are updated to filter on the enum column directly, eliminating the join. The API response shape is preserved (status remains a string).
4. **Ingestion layer**: The advisory ingestion pipeline writes enum values directly instead of inserting into the lookup table first.

## Inherited Fields
- **Priority**: High — propagated to all tasks
- **Fix Version**: RHTPA 2.0.0 — propagated to all tasks (fixVersion scope defaults to "both" since no Jira Field Defaults section exists in CLAUDE.md)

## Dependency Chain
```
Task 1 (create-branch)
  └── Task 2 (migration) ──┐
  └── Task 3 (entities) ────┤ (depends on Task 2)
  └── Task 4 (service) ─────┤ (depends on Task 3)
  └── Task 5 (ingestion) ───┤ (depends on Task 3)
  └── Task 6 (tests) ───────┤ (depends on Tasks 4, 5)
                             │
Task 7 (merge-branch) ──────┘ (depends on Tasks 2-6)
```
