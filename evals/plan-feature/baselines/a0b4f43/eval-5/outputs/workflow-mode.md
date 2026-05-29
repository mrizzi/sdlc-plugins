# Workflow Mode Decision — TC-9005

**Selected mode:** `feature-branch`

**Label to apply:** `workflow:feature-branch` on the TC-9005 feature issue

**Rationale:** Multiple atomicity indicators are present:

1. **Coordinated schema migrations** — The database migration creates the `advisory_status_enum` type, adds the `status` column, backfills data, drops the `status_id` FK column, and drops the `advisory_status` lookup table. All code changes (entity definitions, service layer, endpoints, ingestion pipeline) depend on this migration having completed. Merging the migration without the code changes would break all advisory queries because they still join the now-dropped `advisory_status` table. Merging the code changes without the migration would reference a `status` column that does not yet exist.

2. **Breaking API changes** — Removing the `advisory_status` table and the `status_id` FK column is a breaking change for every advisory query, service method, and endpoint handler in the codebase. All consumers must be updated simultaneously.

3. **Tightly coupled feature components** — The entity definition changes (removing `advisory_status.rs`, modifying `advisory.rs`), service layer changes, endpoint changes, and ingestion pipeline changes form a dependency chain where no subset functions correctly without the others.

**Interdependent tasks:**
- Task 2 (migration) creates the schema that Tasks 3-7 depend on
- Task 3 (entity definitions) provides the Rust types that Tasks 4-7 consume
- Task 4 (service layer) provides the updated query logic that Task 5 (endpoints) depends on
- Task 6 (ingestion) depends on the entity types from Task 3
- Task 7 (tests) validates the behavior of all preceding tasks
