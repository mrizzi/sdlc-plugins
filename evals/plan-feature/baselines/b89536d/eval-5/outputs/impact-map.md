# Repository Impact Map — TC-9005

## trustify-backend

changes:
  - Create a new database migration that defines the `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected), adds a `status` enum column to the `advisory` table, backfills it from the existing `advisory_status` join, drops the `status_id` foreign key column, and drops the `advisory_status` lookup table — all in a single atomic migration
  - Update the SeaORM entity definition in `entity/src/advisory.rs` to replace the `status_id` foreign key field with a `status` enum field of type `advisory_status_enum`
  - Remove the SeaORM entity definition file `entity/src/advisory_status.rs` and its registration in `entity/src/lib.rs`
  - Update `AdvisorySummary` and `AdvisoryDetails` model structs in `modules/fundamental/src/advisory/model/` to use the enum status field directly instead of joining the lookup table
  - Update `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs` to query the `status` enum column directly, removing all joins to the `advisory_status` table
  - Update advisory list and get endpoints in `modules/fundamental/src/advisory/endpoints/` to filter by the new enum column instead of joining the lookup table
  - Update the advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` to write enum values directly to the `status` column instead of inserting into the lookup table
  - Update query helpers in `common/src/db/query.rs` if any advisory-status-specific filtering logic references the old join
  - Update advisory endpoint integration tests in `tests/api/advisory.rs` to reflect the new schema and query patterns

## Workflow Mode

**Mode**: `feature-branch`

**Rationale**: Multiple atomicity indicators are present:

1. **Coordinated schema migration** — the database migration adds the enum column and drops the old table/column. Code changes in entities, services, endpoints, and the ingestor all depend on the new schema. Merging the migration without the code changes would break all advisory queries (they still reference the old join). Merging the code changes without the migration would reference a column that does not exist.
2. **Breaking API changes (internal)** — the entity layer changes from a `status_id` FK relationship to a direct `status` enum field. Every consumer of the advisory entity (service, endpoints, ingestor, tests) must be updated together.
3. **Cross-cutting refactor** — the removal of `advisory_status.rs` entity and all join-based query patterns spans multiple modules (fundamental, ingestor, common, tests).

The feature's own non-functional requirements explicitly state: "All changes must land together."

**Interdependent tasks**: All intermediate tasks (migration, entity update, service/endpoint update, ingestor update, tests) are interdependent — each depends on the schema migration and entity changes, and none can be merged to `main` independently without breaking the application.
