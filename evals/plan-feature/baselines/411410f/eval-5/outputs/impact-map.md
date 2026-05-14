# Repository Impact Map -- TC-9005

## Feature Summary

Drop the `advisory_status` lookup table and replace it with a PostgreSQL enum column (`status`) directly on the `advisory` table. This eliminates join overhead on every advisory query, simplifies the ingestion pipeline, and reduces schema complexity.

## Workflow Mode Decision

**Mode: feature-branch**

**Label: `workflow:feature-branch`**

**Rationale:** This feature has hard atomicity constraints that prevent incremental delivery to main:

1. **Coordinated schema migration** -- The migration creates an enum type, adds a column, backfills data, drops the foreign key, and drops the lookup table. A partial migration leaves the database inconsistent.
2. **Tightly coupled code and schema changes** -- Merging the migration without the code changes breaks all advisory queries (they still join the now-dropped table). Merging the code changes without the migration references a column that does not exist.
3. **The feature description explicitly states** "All changes must land together."

All changes must be accumulated on a feature branch and merged to main atomically.

## Repository: trustify-backend

### migration/

| File | Action | Reason |
|---|---|---|
| `migration/src/lib.rs` | Modify | Register new migration module |
| `migration/src/m0002_advisory_status_enum/mod.rs` | Create | Migration: create `advisory_status_enum` type, add `status` column, backfill from join, drop `status_id` FK column, drop `advisory_status` table |

### entity/

| File | Action | Reason |
|---|---|---|
| `entity/src/advisory.rs` | Modify | Replace `status_id: i32` foreign key with `status: AdvisoryStatusEnum` enum column; add enum type definition |
| `entity/src/lib.rs` | Modify | Remove `advisory_status` module re-export |
| `entity/src/advisory_status.rs` | Delete | Entity for the dropped `advisory_status` lookup table |

### modules/fundamental/ (advisory domain)

| File | Action | Reason |
|---|---|---|
| `modules/fundamental/src/advisory/model/summary.rs` | Modify | Update `AdvisorySummary` to read `status` directly from the enum column instead of joining `advisory_status` |
| `modules/fundamental/src/advisory/model/details.rs` | Modify | Update `AdvisoryDetails` to read `status` from enum column |
| `modules/fundamental/src/advisory/model/mod.rs` | Modify | Remove any `advisory_status` model imports/re-exports |
| `modules/fundamental/src/advisory/service/advisory.rs` | Modify | Remove `advisory_status` join from all advisory queries; filter by enum column directly |
| `modules/fundamental/src/advisory/endpoints/list.rs` | Modify | Update status filter to use enum column instead of join |
| `modules/fundamental/src/advisory/endpoints/get.rs` | Modify | Update single-advisory fetch to use enum column |

### modules/ingestor/ (ingestion pipeline)

| File | Action | Reason |
|---|---|---|
| `modules/ingestor/src/graph/advisory/mod.rs` | Modify | Write enum value directly to `advisory.status` instead of inserting into lookup table and setting `status_id` |

### tests/

| File | Action | Reason |
|---|---|---|
| `tests/api/advisory.rs` | Modify | Update integration tests to reflect new schema (no join, enum status values) |

## Dependency Chain

```
Task 1: Create feature branch TC-9005
  |
  +-- Task 2: Database migration (enum type, column, backfill, drop table)
  |     |
  |     +-- Task 3: Update SeaORM entity definitions
  |           |
  |           +-- Task 4: Update advisory service and model layers
  |           |     |
  |           |     +-- Task 5: Update advisory endpoints
  |           |
  |           +-- Task 6: Update advisory ingestion pipeline
  |
  +-- Task 7: Update integration tests (depends on Tasks 4, 5, 6)
        |
        +-- Task 8: Merge feature branch TC-9005
```
