# Repository Impact Map -- TC-9005

## trustify-backend

### Changes

- Create PostgreSQL enum type `advisory_status_enum` with values (New, Analyzing, Fixed, Rejected) via a new reversible migration
- Add `status` enum column to `advisory` table and backfill from existing `status_id` join in the same migration
- Drop `status_id` foreign key column from `advisory` table after backfill
- Drop `advisory_status` lookup table after all references are removed
- Update SeaORM entity definition in `entity/src/advisory.rs` to replace `status_id` FK field with `status` enum field
- Remove `entity/src/advisory_status.rs` entity file and its registration in `entity/src/lib.rs`
- Update `AdvisorySummary` and `AdvisoryDetails` model structs to use the enum status directly instead of joining the lookup table
- Update `AdvisoryService` (fetch, list, search) to query the `status` enum column instead of joining `advisory_status`
- Update advisory list and get endpoints to use the new status column for filtering
- Update advisory ingestion pipeline to write enum values directly instead of inserting into the lookup table
- Update advisory integration tests to reflect the new schema (no join, enum-based filtering)
- Update query helpers if advisory status filtering is handled via shared query builder

## Workflow Mode

**Selected mode:** `feature-branch`

**Rationale:** Multiple atomicity indicators are present:

1. **Coordinated schema migrations** -- The migration adds an enum column and drops the old FK column and lookup table. All code changes depend on this migration being present; merging code without the migration would reference a non-existent column.
2. **Cross-cutting refactors** -- Entity definitions, service layer, endpoints, and ingestion pipeline all must change together to match the new schema.
3. **Tightly coupled feature components** -- The feature explicitly requires that all changes land together: merging the migration without the code changes would break all advisory queries (they still join the now-dropped table), and merging code changes without the migration would reference a column that does not exist.

**Interdependent tasks:**
- The migration task must land before entity, service, endpoint, and ingestion tasks can function
- Entity changes must land before service/endpoint changes (service imports the entity)
- All intermediate tasks must be merged into the feature branch before the final merge to main
