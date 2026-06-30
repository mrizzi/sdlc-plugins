# Repository Impact Map — TC-9005

## Feature: Drop status table and migrate to enum column

### trustify-backend

changes:
  - Create reversible database migration: define `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected), add `status` enum column to `advisory` table, backfill from existing `status_id` join, drop `status_id` foreign key column, drop `advisory_status` lookup table
  - Update SeaORM entity definition in `entity/src/advisory.rs` to replace `status_id` integer foreign key with `status` enum column mapped to a Rust enum
  - Remove SeaORM entity file `entity/src/advisory_status.rs` and its registration in `entity/src/lib.rs`
  - Update `AdvisorySummary` and `AdvisoryDetails` model structs in `modules/fundamental/src/advisory/model/` to use the enum status field directly instead of joining the lookup table
  - Update `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs` to query the `status` enum column directly, removing all joins to `advisory_status`
  - Update advisory list and get endpoints in `modules/fundamental/src/advisory/endpoints/` to filter by enum column instead of joined table
  - Update advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` to write enum values directly instead of inserting into the lookup table first
  - Update advisory integration tests in `tests/api/advisory.rs` to reflect the new schema (enum-based status filtering, no lookup table references)

---

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** The following atomicity indicators are present:

1. **Coordinated schema migration** — The database migration adds the `status` enum column and drops the `status_id` FK column and `advisory_status` table. All code changes depend on this migration having run. Merging the migration without the code changes would break all advisory queries (they still reference the old join). Merging code changes without the migration would reference a column that does not exist.

2. **Tightly coupled components** — The entity layer, service layer, endpoint layer, and ingestion pipeline all reference the `advisory_status` join. All must be updated atomically — a partial update where some code uses the old FK and some uses the new enum would produce runtime errors.

The feature's non-functional requirements explicitly state: "All changes must land together."

**Interdependent tasks:** All intermediate tasks (migration, entity update, service update, endpoint update, ingestion update, test update) are interdependent — none can be merged to `main` independently without breaking the application.

The `workflow:feature-branch` label will be applied to the feature issue TC-9005.
