# Impact Map: TC-9005 Drop status table and migrate to enum column

## Workflow Mode

**Feature-branch** -- The feature's non-functional requirements mandate atomicity ("Migration must be atomic: if any step fails, the entire migration rolls back") and co-landing ("All changes must land together: merging the migration without the code changes would break all advisory queries"). These constraints require a feature branch so all intermediate changes are merged together into main as a single unit.

**Label**: `workflow:feature-branch`

## Impact Summary

| Area | Files Impacted | Nature of Change |
|---|---|---|
| Database migration | `migration/src/` (new migration module) | Create enum type, add column, backfill data, drop FK, drop table |
| Entity definitions | `entity/src/advisory.rs`, `entity/src/lib.rs` | Replace `status_id` FK with `status` enum column; remove advisory_status entity |
| Advisory service | `modules/fundamental/src/advisory/service/advisory.rs` | Remove status join, query enum column directly |
| Advisory models | `modules/fundamental/src/advisory/model/summary.rs`, `modules/fundamental/src/advisory/model/details.rs` | Update structs to use enum instead of joined status |
| Advisory endpoints | `modules/fundamental/src/advisory/endpoints/list.rs`, `modules/fundamental/src/advisory/endpoints/get.rs` | Update filtering to use enum column |
| Ingestion pipeline | `modules/ingestor/src/graph/advisory/mod.rs` | Write enum value directly instead of lookup table insert |
| Integration tests | `tests/api/advisory.rs` | Update tests to reflect new status column behavior |

## Task Sequence

| # | Task | Target Branch | Dependencies |
|---|---|---|---|
| 1 | Create feature branch TC-9005 from main | main | None |
| 2 | Add database migration for advisory status enum | TC-9005 | Task 1 |
| 3 | Update SeaORM entity definitions for advisory status enum | TC-9005 | Task 1 |
| 4 | Update advisory service and endpoints to use status enum | TC-9005 | Task 1 |
| 5 | Update advisory ingestion pipeline to write enum status | TC-9005 | Task 1 |
| 6 | Add integration tests for advisory status enum migration | TC-9005 | Task 1 |
| 7 | Merge feature branch TC-9005 to main | main | Tasks 2, 3, 4, 5, 6 |

## Risk Notes

- The migration must be tested against a production-sized dataset before deployment
- Zero downtime requirement: the migration must be safe to run while the application is serving traffic
- Partial migration (enum exists but table not dropped, or vice versa) would leave the database inconsistent
