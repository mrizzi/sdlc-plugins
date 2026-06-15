# Impact Map: TC-9005 -- Drop status table and migrate to enum column

## Workflow Mode

**Mode**: `workflow:feature-branch`

**Rationale**: Feature-branch mode is required for this feature due to multiple atomicity constraints identified in the NFRs:

1. **"Migration must be atomic"** -- The database migration creates an enum type, adds a column, backfills data, drops the foreign key, and drops the lookup table. A partial migration would leave the database in an inconsistent state.
2. **"All changes must land together"** -- The migration and code changes are interdependent: merging the migration without the code changes would break all advisory queries (they still reference the dropped join table), and merging the code changes without the migration would reference a column that does not exist.
3. **Schema changes + code changes are interdependent** -- The entity definitions, service layer, ingestion pipeline, and endpoints all depend on the new schema. These cannot be merged independently to main without breaking the application.

Direct-to-main workflow would risk partial deployment where some tasks are merged while others are still in progress, creating a broken state. The feature branch ensures all changes are integrated and tested together before merging to main as a single unit.

## Feature Branch

- **Branch name**: TC-9005
- **Base branch**: main
- **Merge strategy**: Single PR from TC-9005 to main after all intermediate tasks are complete

## Task Summary

| Task | Title | Target Branch | Dependencies |
|------|-------|---------------|--------------|
| 1 | Create feature branch TC-9005 from main | main | (none) |
| 2 | Create PostgreSQL enum type and migration to add status column | TC-9005 | Task 1 |
| 3 | Update SeaORM entity definitions for advisory status enum | TC-9005 | Task 1, Task 2 |
| 4 | Update advisory service and model to use enum status | TC-9005 | Task 1, Task 3 |
| 5 | Update advisory ingestion pipeline to write enum values directly | TC-9005 | Task 1, Task 3 |
| 6 | Update advisory endpoints and integration tests | TC-9005 | Task 1, Task 4, Task 5 |
| 7 | Merge feature branch TC-9005 to main | main | Tasks 2-6 |

## Impact Analysis

### Database Schema

- **New type**: `advisory_status_enum` PostgreSQL enum (New, Analyzing, Fixed, Rejected)
- **Modified table**: `advisory` -- new `status` column of type `advisory_status_enum`; dropped `status_id` column
- **Dropped table**: `advisory_status` lookup table
- **Migration**: Atomic, reversible migration with backfill

### Entity Layer

- **Modified**: `entity/src/advisory.rs` -- `status_id` foreign key replaced with `status` enum column; new `AdvisoryStatusEnum` Rust enum
- **Removed**: `entity/src/advisory_status.rs` -- entity for the dropped lookup table
- **Modified**: `entity/src/lib.rs` -- removed `advisory_status` re-export

### Service Layer

- **Modified**: `modules/fundamental/src/advisory/service/advisory.rs` -- removed `advisory_status` join from all queries
- **Modified**: `modules/fundamental/src/advisory/model/summary.rs` -- status sourced from enum column
- **Modified**: `modules/fundamental/src/advisory/model/details.rs` -- status sourced from enum column

### Ingestion Pipeline

- **Modified**: `modules/ingestor/src/graph/advisory/mod.rs` -- writes enum value directly instead of lookup table insert
- **Modified**: `modules/ingestor/src/service/mod.rs` -- removed advisory_status references if present

### Endpoints

- **Modified**: `modules/fundamental/src/advisory/endpoints/list.rs` -- status filter uses enum
- **Modified**: `modules/fundamental/src/advisory/endpoints/get.rs` -- status from enum column
- **Modified**: `tests/api/advisory.rs` -- updated test fixtures and assertions

### API Surface

- **No breaking changes** -- the advisory API response shape is unchanged; status remains a string field in the JSON response

### Risk Assessment

- **Medium risk**: Database migration involves data backfill and table drops; must be tested against production-sized datasets
- **Mitigation**: Atomic transaction ensures rollback on failure; reversible migration allows rollback after deployment
- **Zero-downtime**: The migration is designed to be safe during live traffic (enum column add + backfill before dropping the old column)

## Dependency Graph

```
Task 1 (create branch)
  |
  v
Task 2 (migration)
  |
  v
Task 3 (entities)
  |       \
  v        v
Task 4    Task 5
(service)  (ingestion)
  |       /
  v      v
Task 6 (endpoints + tests)
  |
  v
Task 7 (merge branch)
```
