# Repository Impact Map — TC-9005

## Feature: Drop status table and migrate to enum column

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** Two atomicity indicators are present:

1. **Coordinated schema migrations** — The database migration adds the `advisory_status_enum` type and `status` enum column to the `advisory` table, then drops the `status_id` FK column and the `advisory_status` lookup table. All code changes (entity definitions, service layer, endpoints, ingestion pipeline) depend on this migration having run. Merging the migration without the code changes would break all advisory queries (they still join the now-dropped table). Merging the code changes without the migration would reference a column (`status`) that does not exist.

2. **Breaking API changes** — The advisory service, endpoints, and ingestion pipeline switch from joining `advisory_status` via `status_id` to reading/writing the `status` enum column directly. These code changes are tightly coupled to the schema migration — neither side functions independently.

**Interdependent tasks:** All intermediate tasks (migration, entity update, service/endpoint update, ingestion update, test update) are mutually dependent and must land together on the feature branch before merging to main.

---

## trustify-backend

### Changes

- Create database migration to define `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected), add `status` enum column to `advisory` table, backfill from existing `status_id` join, drop `status_id` foreign key column, and drop `advisory_status` lookup table
- Update SeaORM entity definition in `entity/src/advisory.rs` to replace `status_id` foreign key with `status` enum column mapping
- Update `entity/src/lib.rs` to remove the `advisory_status` module registration if present
- Update advisory model structs in `modules/fundamental/src/advisory/model/summary.rs` and `modules/fundamental/src/advisory/model/details.rs` to use enum status field instead of joined status
- Update `modules/fundamental/src/advisory/service/advisory.rs` to query `status` enum column directly instead of joining `advisory_status` table
- Update advisory endpoint handlers in `modules/fundamental/src/advisory/endpoints/list.rs` and `modules/fundamental/src/advisory/endpoints/get.rs` to use updated service/model
- Update advisory ingestion in `modules/ingestor/src/graph/advisory/mod.rs` to write enum values directly instead of referencing lookup table
- Update advisory integration tests in `tests/api/advisory.rs` to validate enum-based status filtering and ingestion

### Label Decision

- Add `workflow:feature-branch` label to feature issue TC-9005
