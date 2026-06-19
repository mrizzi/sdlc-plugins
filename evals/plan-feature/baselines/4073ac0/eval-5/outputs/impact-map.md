# Impact Map: TC-9005 — Drop status table and migrate to enum column

## Feature Summary

Replace the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. This eliminates unnecessary join overhead on advisory queries, simplifies the schema, and reduces advisory list endpoint p95 latency by ~40ms.

## Workflow Mode Decision

**Mode:** `workflow:feature-branch`

**Rationale:** The feature's non-functional requirements impose strong atomicity constraints that preclude direct-to-main delivery:

1. **Migration-code co-dependency:** The database migration drops the `advisory_status` table and adds a new `status` enum column. If the migration lands without the code changes, all advisory queries break because they still join the now-dropped table. If the code changes land without the migration, they reference an `advisory.status` column that does not exist.
2. **Explicit atomicity requirement:** The feature description states "All changes must land together" and "if any step fails, the entire migration rolls back."
3. **Multi-file, multi-layer scope:** Changes span migration, entity, service, endpoint, ingestion, and test layers — requiring multiple implementation tasks that must all merge atomically.

Feature-branch workflow allows intermediate tasks to merge into the `TC-9005` branch independently, with a final merge to `main` delivering all changes atomically.

**Label decision:** Apply `workflow:feature-branch` label to feature issue TC-9005.

## Impact Areas

### 1. Database Migration

| Aspect | Detail |
|---|---|
| Scope | New migration file in `migration/src/` |
| Changes | Create `advisory_status_enum` PostgreSQL enum type; add `status` enum column to `advisory` table; backfill from `advisory_status` join; drop `status_id` FK column; drop `advisory_status` table |
| Risk | High — migration must be atomic and reversible; partial application leaves DB inconsistent |

### 2. Entity Layer (SeaORM)

| Aspect | Detail |
|---|---|
| Scope | `entity/src/advisory.rs`, `entity/src/lib.rs` |
| Changes | Update `advisory` entity to replace `status_id` FK with `status` enum column; remove `advisory_status` entity and its registration |
| Risk | Medium — entity changes must align exactly with migration schema |

### 3. Advisory Service Layer

| Aspect | Detail |
|---|---|
| Scope | `modules/fundamental/src/advisory/service/advisory.rs`, `modules/fundamental/src/advisory/model/summary.rs`, `modules/fundamental/src/advisory/model/details.rs` |
| Changes | Remove `advisory_status` join from all advisory queries; update model structs to read `status` directly from the `advisory` entity; update filtering to use enum column |
| Risk | Medium — all query paths must be updated consistently |

### 4. Advisory Endpoints

| Aspect | Detail |
|---|---|
| Scope | `modules/fundamental/src/advisory/endpoints/list.rs`, `modules/fundamental/src/advisory/endpoints/get.rs` |
| Changes | Update status filter parameter handling to use enum values directly instead of join-based filtering |
| Risk | Low — endpoint changes follow from service layer changes |

### 5. Advisory Ingestion Pipeline

| Aspect | Detail |
|---|---|
| Scope | `modules/ingestor/src/graph/advisory/mod.rs`, `modules/ingestor/src/service/mod.rs` |
| Changes | Write enum value directly to `advisory.status` instead of inserting into lookup table and referencing by FK |
| Risk | Medium — ingestion pipeline must map status strings to enum values |

### 6. Integration Tests

| Aspect | Detail |
|---|---|
| Scope | `tests/api/advisory.rs` |
| Changes | Update test setup to use enum status values; update assertions to reflect removed join; add tests for status filtering with enum column |
| Risk | Low — tests validate the other changes |

## Task Breakdown

| Task | Title | Target Branch | Dependencies |
|---|---|---|---|
| 1 | Create feature branch TC-9005 from main | main | None |
| 2 | Create database migration for advisory status enum | TC-9005 | Task 1 |
| 3 | Update SeaORM entity definitions for advisory status enum | TC-9005 | Task 1 |
| 4 | Update advisory service layer and models to use enum column | TC-9005 | Task 1 |
| 5 | Update advisory endpoints for enum-based status filtering | TC-9005 | Task 1 |
| 6 | Update advisory ingestion pipeline to write enum status | TC-9005 | Task 1 |
| 7 | Update advisory integration tests for enum status | TC-9005 | Task 1 |
| 8 | Merge feature branch TC-9005 to main | main | Tasks 2, 3, 4, 5, 6, 7 |
