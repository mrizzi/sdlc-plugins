# Plan Summary: TC-9005 -- Drop status table and migrate to enum column

## Overview
This plan decomposes TC-9005 into **8 tasks** (2 bookend tasks + 6 implementation tasks) using **feature-branch workflow mode** to ensure all changes land atomically on `main`.

## Workflow Mode
**Feature-branch** (`workflow:feature-branch` label applied to all tasks). The feature branch `TC-9005` is created from `main` and merged back after all intermediate tasks are complete.

### Atomicity Rationale
The feature requires coordinated delivery because:
- The database migration drops the `advisory_status` table -- merging it without updating all queries would break the application
- The code changes reference the new `status` enum column -- merging them without the migration would fail at runtime
- Entity, service, ingestion, and endpoint layers are tightly coupled through the schema change

## Task Summary

| # | Task | Type | Target Branch | Dependencies |
|---|---|---|---|---|
| 1 | Create feature branch TC-9005 from main | Bookend (create-branch) | main | None |
| 2 | Create database migration for advisory status enum | Implementation | TC-9005 | Task 1 |
| 3 | Update SeaORM entity definitions for advisory status enum | Implementation | TC-9005 | Task 1, Task 2 |
| 4 | Update advisory service layer and models | Implementation | TC-9005 | Task 1, Task 3 |
| 5 | Update advisory ingestion pipeline | Implementation | TC-9005 | Task 1, Task 3 |
| 6 | Update advisory endpoints for enum status | Implementation | TC-9005 | Task 1, Task 4 |
| 7 | Update advisory integration tests | Implementation | TC-9005 | Task 1, Task 4, Task 5, Task 6 |
| 8 | Merge feature branch TC-9005 to main | Bookend (merge-branch) | main | Tasks 2-7 |

## Inherited Field Propagation
The following fields are inherited from the parent feature TC-9005 and propagated to all tasks:
- **Priority**: High
- **Fix Versions**: RHTPA 2.0.0
- **Labels**: ai-generated-jira, workflow:feature-branch

## Key Design Decisions
1. **Migration approach**: Single atomic migration that creates the enum, backfills, drops FK, and drops the table in one transaction. Reversible via `down` migration.
2. **Enum definition**: Separate `advisory_status_enum.rs` file in the entity crate using SeaORM's `DeriveActiveEnum` macro, making the enum reusable across service and ingestor modules.
3. **Task ordering**: Migration first, then entities, then service/ingestion (parallelizable), then endpoints, then tests. This respects the data dependency chain.
4. **API compatibility**: No external API changes. Status remains a string in API responses; the enum-to-string conversion happens in the model layer.

## Convention Enrichment
Applicable conventions from the repository's Key Conventions were applied:
- SeaORM entity and migration patterns (Tasks 2, 3)
- `Result<T, AppError>` with `.context()` error handling (Tasks 4, 5)
- `PaginatedResults<T>` response wrapper for list endpoints (Tasks 4, 6)
- Shared query helpers from `common/src/db/query.rs` (Task 4)
- Integration test patterns with real PostgreSQL (Task 7)
- Route registration via `endpoints/mod.rs` (Task 6)

## Files Impacted
- **Created**: 2 files (migration module, enum definition)
- **Modified**: 13 files (entities, service, models, ingestion, endpoints, tests, migration lib)
- **Removed**: 1 file (advisory_status entity)
