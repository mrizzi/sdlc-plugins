# Repository Impact Map — TC-9005

## trustify-backend

### changes:
- Create a new database migration that defines the `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected), adds a `status` enum column to the `advisory` table, backfills it from the existing `advisory_status` join, drops the `status_id` foreign key column, and drops the `advisory_status` lookup table
- Update the SeaORM entity definition in `entity/src/advisory.rs` to replace the `status_id` foreign key field with a `status` enum field of type `advisory_status_enum`
- Remove the SeaORM entity file `entity/src/advisory_status.rs` (lookup table entity no longer needed) and remove its re-export from `entity/src/lib.rs`
- Update `modules/fundamental/src/advisory/service/advisory.rs` (AdvisoryService) to query the `status` column directly instead of joining `advisory_status`
- Update `modules/fundamental/src/advisory/model/summary.rs` (AdvisorySummary) and `modules/fundamental/src/advisory/model/details.rs` (AdvisoryDetails) to source status from the enum column instead of a joined relation
- Update `modules/fundamental/src/advisory/endpoints/list.rs` and `modules/fundamental/src/advisory/endpoints/get.rs` to filter/return status using the enum column
- Update `modules/ingestor/src/graph/advisory/mod.rs` to write the enum value directly to the `status` column instead of inserting into the lookup table
- Update `common/src/db/query.rs` if advisory status filtering helpers reference the old join
- Update `tests/api/advisory.rs` to reflect the new schema (no join, enum column filtering)

## Workflow Mode

**Mode:** `feature-branch`

**Rationale:** Multiple atomicity indicators are present:

1. **Coordinated schema migration** — The database migration adds the `advisory_status_enum` type and `status` column while dropping the `status_id` FK and `advisory_status` table. All code changes (entity definitions, service queries, ingestion pipeline) depend on this migration having run. Merging the migration without the code changes would break all advisory queries (they still reference the old join). Merging the code changes without the migration would reference a column that does not exist.

2. **Cross-cutting refactor** — The schema change touches the entity layer, service layer, endpoint layer, ingestion pipeline, and tests. Each of these changes is interdependent: the entity change defines the new enum field, the service change queries it, the endpoints filter by it, and the ingestor writes to it. Partial delivery would leave the codebase in an inconsistent state.

**Interdependent tasks:** All intermediate tasks (migration, entity update, service/endpoint update, ingestor update, tests) are tightly coupled. The migration must land before entity/service changes can compile, and entity changes must land before service/endpoint/ingestor changes can compile.

**Feature branch name:** `TC-9005`
