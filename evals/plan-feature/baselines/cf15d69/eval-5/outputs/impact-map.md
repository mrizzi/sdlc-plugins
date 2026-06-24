# Impact Map: TC-9005 — Drop status table and migrate to enum column

## Workflow Mode
**Feature-branch workflow** (`workflow:feature-branch` label applied to TC-9005). All changes land on the `TC-9005` feature branch and merge to `main` atomically via a single PR.

## Task Summary

| Task | Title | Target Branch | Dependencies |
|---|---|---|---|
| 1 | Create feature branch TC-9005 from main | main | (none) |
| 2 | Database migration for advisory status enum | TC-9005 | Task 1 |
| 3 | Update SeaORM entity definitions | TC-9005 | Task 1, Task 2 |
| 4 | Update advisory service layer and queries | TC-9005 | Task 1, Task 3 |
| 5 | Update advisory endpoints | TC-9005 | Task 1, Task 4 |
| 6 | Update advisory ingestion pipeline | TC-9005 | Task 1, Task 3 |
| 7 | Update integration tests | TC-9005 | Task 1, Task 4, Task 5, Task 6 |
| 8 | Merge feature branch TC-9005 into main | main | Tasks 2-7 |

## Dependency Graph

```
Task 1 (create-branch)
  ├── Task 2 (migration)
  │     └── Task 3 (entities)
  │           ├── Task 4 (service)
  │           │     └── Task 5 (endpoints)
  │           └── Task 6 (ingestion)
  │
  └────────── Task 7 (tests) ← depends on Tasks 4, 5, 6
                    │
                    v
              Task 8 (merge-branch) ← depends on Tasks 2-7
```

## Files Impacted

### Migration
| File | Action | Task |
|---|---|---|
| `migration/src/m0002_advisory_status_enum/mod.rs` | Create | 2 |
| `migration/src/lib.rs` | Modify | 2 |

### Entity Layer
| File | Action | Task |
|---|---|---|
| `entity/src/advisory.rs` | Modify | 3 |
| `entity/src/advisory_status_enum.rs` | Create | 3 |
| `entity/src/lib.rs` | Modify | 3 |

### Advisory Service & Endpoints
| File | Action | Task |
|---|---|---|
| `modules/fundamental/src/advisory/service/advisory.rs` | Modify | 4 |
| `modules/fundamental/src/advisory/model/summary.rs` | Modify | 4 |
| `modules/fundamental/src/advisory/model/details.rs` | Modify | 4 |
| `modules/fundamental/src/advisory/model/mod.rs` | Modify | 4 |
| `modules/fundamental/src/advisory/endpoints/list.rs` | Modify | 5 |
| `modules/fundamental/src/advisory/endpoints/get.rs` | Modify | 5 |
| `modules/fundamental/src/advisory/endpoints/mod.rs` | Modify | 5 |

### Ingestion Pipeline
| File | Action | Task |
|---|---|---|
| `modules/ingestor/src/graph/advisory/mod.rs` | Modify | 6 |
| `modules/ingestor/src/service/mod.rs` | Modify | 6 |

### Tests
| File | Action | Task |
|---|---|---|
| `tests/api/advisory.rs` | Modify | 7 |

## Risk Assessment

- **Atomicity**: All changes must land together. The feature-branch workflow ensures this by merging a single PR from TC-9005 to main.
- **Migration reversibility**: The `down()` migration must fully restore the original schema. Task 2 requires explicit testing of the reverse migration.
- **Zero downtime**: The migration runs while the application serves traffic. The backfill step must handle concurrent writes safely.
- **API compatibility**: The response shape is unchanged (status remains a string). No external consumer impact expected.

## Labels
- `workflow:feature-branch` — applied to TC-9005 feature issue
