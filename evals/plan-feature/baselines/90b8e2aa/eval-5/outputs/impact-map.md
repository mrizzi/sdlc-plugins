# Repository Impact Map — TC-9005: Drop status table and migrate to enum column

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** Two atomicity indicators are present:

1. **Coordinated schema migrations** — The database migration creates the `advisory_status_enum` type and adds the `status` enum column to the `advisory` table while dropping the `status_id` FK column and the `advisory_status` lookup table. The code changes (entity definitions, service layer, ingestion pipeline) depend on the new column existing and the old column/table being removed. Merging the migration without the code changes would leave advisory queries joining a dropped table; merging the code changes without the migration would reference a column that does not exist.

2. **Breaking API changes** — The service layer, endpoint, and ingestion code changes all reference the new `status` enum column. Without the corresponding migration, these changes break at runtime. Conversely, the migration drops the `advisory_status` table, so existing queries that join it would fail if the code changes have not landed.

**Interdependent tasks:** All intermediate tasks (migration, entity updates, service/model/endpoint updates, ingestion updates, test updates) are mutually dependent — none can land on `main` independently without breaking the application.

**Label:** The `workflow:feature-branch` label will be applied to the feature issue TC-9005.

---

## Impact Map

```
trustify-backend:
  changes:
    - Create database migration to define `advisory_status_enum` PostgreSQL enum type, add `status` enum column to `advisory` table, backfill from `advisory_status` join, drop `status_id` FK column, and drop `advisory_status` lookup table
    - Update SeaORM entity definition in `entity/src/advisory.rs` to replace `status_id` FK field with `status` enum field, and remove `entity/src/advisory_status.rs` entity module
    - Update advisory service queries in `modules/fundamental/src/advisory/service/advisory.rs` to use `status` enum column instead of joining `advisory_status` table
    - Update advisory model structs (`AdvisorySummary`, `AdvisoryDetails`) to source status from enum column
    - Update advisory list and get endpoints to filter and return status using enum column directly
    - Update advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` to write enum values directly instead of inserting into lookup table
    - Update advisory integration tests in `tests/api/advisory.rs` to reflect new schema and removed join
```
