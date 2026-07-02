# Impact Map: TC-9005 -- Drop status table and migrate to enum column

## Feature
**TC-9005**: Drop status table and migrate to enum column

Replace the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table to eliminate unnecessary join overhead, simplify queries, and reduce schema complexity.

## Workflow Mode
**feature-branch**

### Rationale
This feature requires feature-branch workflow mode due to multiple atomicity constraints:

1. **Coordinated schema migration**: The database migration creates an enum type, backfills data, drops a foreign key column, and drops a table. A partial migration (enum column exists but lookup table is already dropped, or vice versa) would leave the database in an inconsistent state.
2. **Tightly coupled components**: The migration, entity definitions, service layer, ingestion pipeline, and endpoints are all interdependent. Merging the migration without the code changes would break all advisory queries (they still join the now-dropped table). Merging the code changes without the migration would reference a column that does not exist.
3. **Breaking internal contract**: The entity layer change (replacing `status_id: i32` with `status: AdvisoryStatusEnum`) is a breaking change that ripples through the service layer, ingestion pipeline, and endpoints. All layers must be updated together.

The `workflow:feature-branch` label is applied to all tasks to indicate this coordinated delivery mode.

## Changes

### Database Layer
| File | Change | Impact |
|---|---|---|
| `migration/src/m0002_advisory_status_enum/mod.rs` | NEW: Migration to create enum type, add column, backfill, drop FK, drop table | Schema change -- all layers must update |
| `migration/src/lib.rs` | MODIFY: Register new migration | Migration discovery |

### Entity Layer
| File | Change | Impact |
|---|---|---|
| `entity/src/advisory.rs` | MODIFY: Replace `status_id` FK with `status` enum column | All advisory queries affected |
| `entity/src/advisory_status_enum.rs` | NEW: `AdvisoryStatusEnum` with `DeriveActiveEnum` | New type used across service and ingestor |
| `entity/src/lib.rs` | MODIFY: Remove `advisory_status` module, add enum module | Module exports |

### Service Layer
| File | Change | Impact |
|---|---|---|
| `modules/fundamental/src/advisory/service/advisory.rs` | MODIFY: Remove `advisory_status` joins from all queries | Query performance improvement |
| `modules/fundamental/src/advisory/model/summary.rs` | MODIFY: Source status from enum column | Model mapping |
| `modules/fundamental/src/advisory/model/details.rs` | MODIFY: Source status from enum column | Model mapping |
| `modules/fundamental/src/advisory/model/mod.rs` | MODIFY: Update imports | Module structure |

### Ingestion Pipeline
| File | Change | Impact |
|---|---|---|
| `modules/ingestor/src/graph/advisory/mod.rs` | MODIFY: Write enum values directly | Ingestion flow simplified |
| `modules/ingestor/src/service/mod.rs` | MODIFY: Remove status lookup logic | Service layer cleanup |

### Endpoint Layer
| File | Change | Impact |
|---|---|---|
| `modules/fundamental/src/advisory/endpoints/list.rs` | MODIFY: Update status filter to use enum | Filtering behavior |
| `modules/fundamental/src/advisory/endpoints/get.rs` | MODIFY: Update status mapping if needed | Response mapping |
| `modules/fundamental/src/advisory/endpoints/mod.rs` | MODIFY: Update route registration if needed | Route setup |

### Test Layer
| File | Change | Impact |
|---|---|---|
| `tests/api/advisory.rs` | MODIFY: Update test data setup to use enum values | Test infrastructure |

## API Impact
No external API changes. The advisory endpoints continue to return status as a string field in the response body. The response shape is identical before and after the migration.

## Risk Assessment
- **High**: Database migration must be tested against production-sized datasets before deployment
- **Medium**: Rollback complexity -- the `down` migration must correctly restore the lookup table with backfilled data
- **Low**: API compatibility -- response shape is unchanged

## Task Dependency Graph
```
Task 1 (create-branch)
  |
  +-- Task 2 (migration)
  |     |
  |     +-- Task 3 (entities)
  |           |
  |           +-- Task 4 (service/models)
  |           |     |
  |           |     +-- Task 6 (endpoints)
  |           |           |
  |           |           +-- Task 7 (tests)
  |           |
  |           +-- Task 5 (ingestion)
  |                 |
  |                 +-- Task 7 (tests)
  |
  Task 8 (merge-branch) -- depends on Tasks 2-7
```
