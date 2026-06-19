# Repository Impact Map -- TC-9005

## Feature Summary
Drop the `advisory_status` lookup table and migrate to a PostgreSQL enum column on the `advisory` table. Replace the `status_id` foreign key join with a direct `status` enum column, simplifying queries and improving performance.

## Workflow Mode Decision

**Mode: feature-branch**

**Rationale:** The feature exhibits clear atomicity constraints that require all changes to land together:

1. **Atomic migration requirement**: "Migration must be atomic: if any step fails, the entire migration rolls back" -- the database migration creates an enum type, adds a column, backfills data, drops the FK column, and drops the lookup table. A partial migration would leave the database in an inconsistent state.
2. **Cross-component coupling**: "All changes must land together: merging the migration without the code changes would break all advisory queries (they still join the now-dropped table), and merging the code changes without the migration would reference a column that does not exist." The migration, entity definitions, service layer, ingestion pipeline, and tests are tightly coupled -- any subset landing on main independently would produce a broken build.
3. **Breaking schema change**: Dropping the `advisory_status` table and `status_id` column is irreversible at the application layer -- all code referencing these must be updated simultaneously.

These indicators clearly require feature-branch mode to ensure all-or-nothing delivery.

**Label**: Apply `workflow:feature-branch` to TC-9005.

## Impacted Repository
**trustify-backend**

## Impact Areas

### 1. Database Migration Layer
- **New**: `migration/src/m0002_advisory_status_enum/mod.rs` -- Migration creating enum type, adding column, backfilling, dropping FK column and lookup table
- **Modify**: `migration/src/lib.rs` -- Register new migration module
- **Modify**: `migration/Cargo.toml` -- Dependencies for migration

### 2. Entity Definitions (SeaORM)
- **Modify**: `entity/src/advisory.rs` -- Replace `status_id` FK field with `status` enum field; remove `advisory_status` relation
- **Modify**: `entity/src/lib.rs` -- Remove `advisory_status` module; add enum module
- **New**: `entity/src/advisory_status_enum.rs` -- `AdvisoryStatusEnum` with `DeriveActiveEnum` mapping to PostgreSQL enum
- **Remove**: `entity/src/advisory_status.rs` (if exists) -- Lookup table entity no longer needed

### 3. Advisory Service and Endpoints
- **Modify**: `modules/fundamental/src/advisory/service/advisory.rs` -- Remove `advisory_status` joins from all queries; use `advisory.status` column directly
- **Modify**: `modules/fundamental/src/advisory/model/summary.rs` -- Update `AdvisorySummary` to use `AdvisoryStatusEnum`
- **Modify**: `modules/fundamental/src/advisory/model/details.rs` -- Update `AdvisoryDetails` to use `AdvisoryStatusEnum`
- **Modify**: `modules/fundamental/src/advisory/model/mod.rs` -- Update imports
- **Modify**: `modules/fundamental/src/advisory/endpoints/list.rs` -- Update status filter to use enum values
- **Modify**: `modules/fundamental/src/advisory/endpoints/get.rs` -- Update response construction
- **Modify**: `modules/fundamental/src/advisory/endpoints/mod.rs` -- Update route registration if filter types change
- **Modify**: `common/src/db/query.rs` -- Update shared query helpers if they contain advisory-status join logic

### 4. Ingestion Pipeline
- **Modify**: `modules/ingestor/src/graph/advisory/mod.rs` -- Replace lookup-table status resolution with direct enum mapping
- **Modify**: `modules/ingestor/src/service/mod.rs` -- Update if status resolution logic exists here

### 5. Integration Tests
- **Modify**: `tests/api/advisory.rs` -- Update test setup and assertions for enum-based status

## Task Dependency Graph

```
Task 1: Create feature branch TC-9005 (bookend: create-branch) [Target: main]
  |
  +---> Task 2: Database migration (enum column) [Target: TC-9005]
  |       |
  |       +---> Task 3: Update entity definitions [Target: TC-9005]
  |               |
  |               +---> Task 4: Update advisory service and endpoints [Target: TC-9005]
  |               |
  |               +---> Task 5: Update ingestion pipeline [Target: TC-9005]
  |                       |
  |                       +---> Task 6: Update integration tests [Target: TC-9005]
  |                               (also depends on Task 4)
  |
  +---> Task 7: Merge feature branch TC-9005 (bookend: merge-branch) [Target: main]
          (depends on Tasks 2, 3, 4, 5, 6)
```

## Description Digests

- Task 1 (Create feature branch): `sha256-md:3193f81c13f8415a1684ed22dbb7adf034b35f905899a9d74fa0400d31525b5f`
- Task 2 (Database migration): `sha256-md:388d0195ee0ef9af2aa0e21869efc7f523465f91b84274ca519559d1dbd24cf4`
- Task 3 (Update entity definitions): `sha256-md:c257656cd996b3f39f511d8aef93f8e3fa5697ebd4bf2e91ce768d77bcc5a3c2`
- Task 4 (Update advisory service and endpoints): `sha256-md:ea18697b325fec2d55c1c52d4ccca83c807744f59a77eae0c270a655191d8716`
- Task 5 (Update ingestion pipeline): `sha256-md:408ae93b80aa65620b3c587e693b2605da7aa420832cb1045cf1d15a3575eb65`
- Task 6 (Update integration tests): `sha256-md:90c815dd65f370929108ea5d6ffc448bacc1aa51a221354d34527fb57f26be95`
- Task 7 (Merge feature branch): `sha256-md:c0fdbd6e91ee0a7758eda3c5f5db778fc666a08d99432f07cec71489bcff301f`
