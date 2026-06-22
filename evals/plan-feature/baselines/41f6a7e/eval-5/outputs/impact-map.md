# Repository Impact Map — TC-9005

## trustify-backend

### Changes

- Create a reversible database migration that: defines `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected); adds `status` enum column to `advisory` table; backfills `status` from existing `status_id` join; drops `status_id` foreign key column from `advisory` table; drops `advisory_status` lookup table
- Update SeaORM entity definition in `entity/src/advisory.rs` to replace the `status_id` foreign key field with a `status` enum field mapped to `advisory_status_enum`
- Remove the `advisory_status` SeaORM entity (currently implied by the `advisory_status` lookup table, though no standalone file exists — verify during implementation whether an `entity/src/advisory_status.rs` exists and remove if so)
- Update `AdvisorySummary` and `AdvisoryDetails` model structs in `modules/fundamental/src/advisory/model/` to use the enum status directly instead of joining the lookup table
- Update `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs` to query the `status` enum column directly, removing all joins to `advisory_status`
- Update advisory list and get endpoints in `modules/fundamental/src/advisory/endpoints/` to filter by the enum column instead of joining
- Update advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` to write enum values directly instead of inserting into the lookup table
- Update query builder helpers in `common/src/db/query.rs` if any advisory-specific status filtering logic references the lookup table
- Update advisory integration tests in `tests/api/advisory.rs` to reflect the new schema (no status join, direct enum filtering)

## Workflow Mode

**Selected mode:** `feature-branch`

**Rationale:** Multiple atomicity indicators are present:

1. **Coordinated schema migration** — The database migration adds the `status` enum column and drops `status_id` / `advisory_status`. Merging the migration without the code changes would break all advisory queries (they still reference the now-dropped `status_id` column and `advisory_status` table). Merging the code changes without the migration would reference a `status` column that does not exist.
2. **Breaking internal API contract** — The entity layer change (replacing `status_id: i32` with `status: AdvisoryStatusEnum`) propagates to every consumer: service, endpoints, ingestion, and tests. Partial delivery would leave compilation errors.
3. **Explicit NFR** — The feature requirements state: "All changes must land together: merging the migration without the code changes would break all advisory queries."

**Interdependent tasks:** All intermediate tasks (migration, entity update, service/endpoint update, ingestion update, test update) are mutually dependent via the schema change and must land on the feature branch before merging to `main`.
