## Implementation Plan: TC-9005 -- Drop status table and migrate to enum column

### Tasks Created

| # | Summary | Repository | Target Branch | Type |
|---|---|---|---|---|
| 1 | Create feature branch TC-9005 from main | trustify-backend | main | Bookend (create-branch) |
| 2 | Create database migration to replace advisory_status table with enum column | trustify-backend | TC-9005 | Implementation |
| 3 | Update SeaORM entity definitions for advisory status enum | trustify-backend | TC-9005 | Implementation |
| 4 | Update advisory service and model layer to use status enum | trustify-backend | TC-9005 | Implementation |
| 5 | Update advisory ingestion pipeline to write enum values directly | trustify-backend | TC-9005 | Implementation |
| 6 | Update advisory endpoints and integration tests for status enum | trustify-backend | TC-9005 | Implementation |
| 7 | Merge feature branch TC-9005 to main | trustify-backend | main | Bookend (merge-branch) |

### Repositories Affected

- **trustify-backend** -- all 7 tasks target this repository

### Architecture Summary

This plan replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table, eliminating an unnecessary join from all advisory queries. The work is decomposed into five implementation tasks between two bookend tasks:

1. **Database migration** (Task 2): Creates the `advisory_status_enum` PostgreSQL type, adds an enum `status` column to `advisory`, backfills from the existing `status_id` join, then drops the foreign key and the lookup table -- all within a single atomic transaction.
2. **Entity definitions** (Task 3): Updates SeaORM entities to reflect the new schema -- replaces `status_id` with a `status` enum column in the advisory entity and removes the advisory_status entity.
3. **Service/model layer** (Task 4): Removes all `advisory_status` joins from advisory queries and updates model structs to read status from the enum column.
4. **Ingestion pipeline** (Task 5): Updates advisory ingestion to write enum values directly instead of inserting into the lookup table.
5. **Endpoints and tests** (Task 6): Updates REST endpoint handlers and integration tests for the new enum-based filtering.

### Feature-branch workflow

The `workflow:feature-branch` label will be applied to TC-9005. All intermediate tasks (2-6) target the `TC-9005` feature branch. The migration and code changes must land atomically because merging them independently would leave the database or code in an inconsistent state.

### Priority and Fix Versions

- Priority: High (propagated to all tasks)
- Fix Versions: RHTPA 2.0.0 (propagated to all tasks)

### Dependency Graph

```
Task 1 (create-branch)
  |
  +-- Task 2 (migration) --------+
  |     |                         |
  |     +-- Task 3 (entities) ----+-- Task 7 (merge-branch)
  |           |                   |
  |           +-- Task 4 (service)+
  |           |                   |
  |           +-- Task 5 (ingest) +
  |                 |             |
  |                 +-- Task 6 ---+
  |                   (endpoints) |
  +-------------------------------+
```
