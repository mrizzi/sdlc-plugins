# Repository Impact Map — TC-9005

## Workflow Mode Decision

**Mode: feature-branch**

**Rationale:** Two atomicity indicators are present:

1. **Coordinated schema migrations** — The database migration creates the `advisory_status_enum` type, adds the `status` enum column, backfills data, drops the `status_id` FK column, and drops the `advisory_status` table. All code changes in the service layer, endpoints, and ingestion pipeline depend on this new schema. Merging the migration alone would drop the table that existing code still joins; merging the code alone would reference a column that does not exist.

2. **Breaking API changes (internal)** — The entity layer change (removing `advisory_status.rs`, modifying `advisory.rs`) breaks all consumers of the `Advisory` entity until the service layer and ingestion pipeline are updated to use the new enum field instead of the old FK relation.

The feature description explicitly states: "All changes must land together: merging the migration without the code changes would break all advisory queries."

**Interdependent tasks:** The migration task, entity update task, service/endpoint update task, and ingestion pipeline update task are all mutually dependent — none can be merged to `main` independently without breaking the application.

**Label decision:** Apply `workflow:feature-branch` label to TC-9005.

---

## Impact Map

```
trustify-backend:
  changes:
    - Create PostgreSQL enum type `advisory_status_enum` with values (New, Analyzing, Fixed, Rejected) via database migration
    - Add `status` enum column to `advisory` table and backfill from `status_id` join
    - Drop `status_id` foreign key column from `advisory` table
    - Drop `advisory_status` lookup table
    - Update SeaORM entity definitions: modify `entity/advisory.rs` to use enum column, remove `entity/advisory_status.rs`
    - Update `entity/lib.rs` to remove `advisory_status` module re-export
    - Update AdvisoryService (fetch, list, search) to query `status` enum column directly instead of joining `advisory_status`
    - Update advisory list endpoint to filter by enum column instead of join
    - Update advisory ingestion pipeline to write enum values directly instead of lookup table insert
    - Update advisory integration tests to cover new enum-based queries and ingestion
```
