## Plan Summary — TC-9005: Drop status table and migrate to enum column

### Workflow Mode
**feature-branch** — all changes staged on branch TC-9005 and merged atomically to main. Rationale: the migration and code changes must land together; merging them independently would leave the database or application in an inconsistent state.

Label `workflow:feature-branch` applied to TC-9005.

### Field Propagation
- **Priority: High** — propagated from feature to all tasks
- **fixVersions: RHTPA 2.0.0** — propagated from feature to all tasks (fixVersion scope defaults to "both" — no Jira Field Defaults section in CLAUDE.md)

### Tasks Created (8)

| # | Task | Target Branch | Type | Dependencies |
|---|---|---|---|---|
| 1 | Create feature branch TC-9005 | main | Bookend (create-branch) | -- |
| 2 | Database migration: create enum, backfill, drop table | TC-9005 | Implementation | Task 1 |
| 3 | Update SeaORM entity definitions | TC-9005 | Implementation | Task 1, Task 2 |
| 4 | Update advisory service and endpoints | TC-9005 | Implementation | Task 1, Task 3 |
| 5 | Update ingestion pipeline | TC-9005 | Implementation | Task 1, Task 3 |
| 6 | Update integration tests | TC-9005 | Implementation | Task 1, Task 4, Task 5 |
| 7 | Update documentation | TC-9005 | Documentation | Tasks 2-6 |
| 8 | Merge feature branch TC-9005 to main | main | Bookend (merge-branch) | Tasks 2-7 |

### Impact Summary
- **Repository**: trustify-backend
- **Files impacted**: ~15 files across migration, entity, service, ingestor, and test layers
- **Schema changes**: Drop advisory_status table, create advisory_status_enum type, add status column to advisory table
- **API changes**: None (response shape unchanged)
- **Risk**: Medium — atomic migration with backfill; tested against production-sized dataset recommended before deployment
