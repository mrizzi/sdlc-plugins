## Repository Impact Map — TC-9005: Drop status table and migrate to enum column

### Workflow Mode Decision

**Mode: feature-branch**

Rationale: The Non-Functional Requirements specify two atomicity constraints that require all changes to land together:

1. "Migration must be atomic: if any step fails, the entire migration rolls back" — a partial migration (enum column exists but lookup table is already dropped, or vice versa) would leave the database in an inconsistent state.
2. "All changes must land together: merging the migration without the code changes would break all advisory queries (they still join the now-dropped table), and merging the code changes without the migration would reference a column that does not exist."

These constraints mean the database migration, entity definition updates, service/endpoint changes, ingestion pipeline updates, and integration test updates cannot be merged incrementally to main. A feature branch (TC-9005) is required to stage all changes together and merge them atomically via a single PR to main.

**Label: `workflow:feature-branch`** — to be applied to TC-9005 in Jira.

### Impacted Repository: trustify-backend

#### Database Layer
| File | Change Type | Description |
|---|---|---|
| `migration/src/m0002_advisory_status_enum/mod.rs` | CREATE | Atomic migration: create advisory_status_enum type, add status column, backfill from join, drop status_id FK, drop advisory_status table |
| `migration/src/lib.rs` | MODIFY | Register new migration module |
| `migration/Cargo.toml` | MODIFY | Add enum support dependencies if needed |

#### Entity Layer
| File | Change Type | Description |
|---|---|---|
| `entity/src/advisory.rs` | MODIFY | Replace status_id FK column with status enum column using DeriveActiveEnum |
| `entity/src/advisory_status.rs` | DELETE | Remove lookup table entity — table has been dropped |
| `entity/src/lib.rs` | MODIFY | Remove advisory_status module declaration |

#### Service and Endpoint Layer
| File | Change Type | Description |
|---|---|---|
| `modules/fundamental/src/advisory/service/advisory.rs` | MODIFY | Remove advisory_status joins from all query methods; filter by enum column |
| `modules/fundamental/src/advisory/model/summary.rs` | MODIFY | Source status from enum column instead of joined field |
| `modules/fundamental/src/advisory/model/details.rs` | MODIFY | Source status from enum column instead of joined field |
| `modules/fundamental/src/advisory/model/mod.rs` | MODIFY | Update shared model imports for status type |
| `modules/fundamental/src/advisory/endpoints/list.rs` | MODIFY | Update status filter to compare against enum column |
| `modules/fundamental/src/advisory/endpoints/get.rs` | MODIFY | Update single advisory retrieval to use enum column |

#### Ingestion Pipeline
| File | Change Type | Description |
|---|---|---|
| `modules/ingestor/src/graph/advisory/mod.rs` | MODIFY | Write enum values directly instead of inserting into lookup table |
| `modules/ingestor/src/service/mod.rs` | MODIFY | Update IngestorService status handling |

#### Integration Tests
| File | Change Type | Description |
|---|---|---|
| `tests/api/advisory.rs` | MODIFY | Update tests for enum-based status; remove advisory_status table references |

#### Documentation
| File | Change Type | Description |
|---|---|---|
| `README.md` | MODIFY | Update schema descriptions to reflect enum column |

### Task Dependency Chain

```
Task 1 (create-branch) ──> Task 2 (migration)
                       ──> Task 3 (entities) ──> Task 4 (service/endpoints) ──> Task 6 (tests)
                       ──> Task 3 (entities) ──> Task 5 (ingestion)         ──> Task 6 (tests)
Tasks 2-6 ──> Task 7 (documentation)
Tasks 2-7 ──> Task 8 (merge-branch)
```
