# Implementation Plan for TC-9201

**Task**: Add advisory severity aggregation service and endpoint
**Branch**: `TC-9201` (based on `main`)

---

## Overview

This task adds a new REST endpoint `GET /api/v2/sbom/{id}/advisory-summary` that returns aggregated severity counts (critical, high, medium, low, total) for all advisories linked to a given SBOM. The implementation spans three new files and three modified files, following the existing domain module conventions in `trustify-backend`.

---

## Existing Code Inspection

Before implementing, the following existing files were inspected to understand codebase conventions:

1. **advisory/endpoints/get.rs** -- Examined to understand how existing GET endpoints extract path parameters via `Path<Id>`, call service methods, and return `Result<Json<T>, AppError>`. This establishes the endpoint scaffolding pattern to follow.
2. **advisory/service/advisory.rs** -- Inspected to understand service method structure: methods accept `&self`, take an `Id` parameter and `Transactional` context, build SeaORM queries, and return `Result<T, anyhow::Error>` with `.context()` error wrapping.
3. **advisory/model/summary.rs** -- Reviewed to understand the existing summary model pattern, including derive macros (`Serialize`, `Deserialize`, `ToSchema`, `Debug`, `Clone`) and field naming conventions used for response structs.
4. **common/src/error.rs** -- Checked to confirm the `AppError` type definition and how `.context()` from anyhow is used for error propagation throughout the codebase.

---

## Files to Create (3)

### 1. `modules/fundamental/src/advisory/model/severity_summary.rs`
**Purpose**: Define the `SeveritySummary` response struct with per-severity count fields.
**Details**: See `outputs/file-1-description.md`

### 2. `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
**Purpose**: GET handler for the `/api/v2/sbom/{id}/advisory-summary` endpoint.
**Details**: See `outputs/file-2-description.md`

### 3. `tests/api/advisory_summary.rs`
**Purpose**: Integration tests covering valid SBOM, missing SBOM, empty results, and deduplication cases.
**Details**: See `outputs/file-3-description.md`

---

## Files to Modify (3)

### 4. `modules/fundamental/src/advisory/service/advisory.rs`
**Purpose**: Add the `get_severity_summary` method to `AdvisoryService`.
**Details**: See `outputs/file-4-description.md`

### 5. `modules/fundamental/src/advisory/endpoints/mod.rs`
**Purpose**: Register the new route for the severity summary endpoint.
**Details**: See `outputs/file-5-description.md`

### 6. `modules/fundamental/src/advisory/model/mod.rs`
**Purpose**: Register the new `severity_summary` model module and re-export the struct.
**Details**: See `outputs/file-6-description.md`

---

## Files NOT Modified

- `server/src/main.rs` -- No changes needed. Routes auto-mount via module registration.

---

## Dependency Order

1. Create model struct (file 1) -- no dependencies
2. Register model module in `model/mod.rs` (file 6) -- depends on model file existing
3. Add service method to `advisory/service/advisory.rs` (file 4) -- depends on model struct
4. Create endpoint handler (file 2) -- depends on service method
5. Register route in `advisory/endpoints/mod.rs` (file 5) -- depends on endpoint handler
6. Add integration tests (file 3) -- depends on all above

---

## Commit Strategy

Single commit with the following message:

```
feat(advisory): add severity aggregation service and endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated vulnerability advisory severity counts (critical, high,
medium, low, total) for a given SBOM.

- Add SeveritySummary response model
- Add get_severity_summary method to AdvisoryService using sbom_advisory join
- Add GET handler following existing endpoint patterns
- Add integration tests for valid SBOM, missing SBOM, empty, and dedup cases

Refs: TC-9201
--trailer="Assisted-by: Claude Code"
```

---

## Acceptance Criteria Mapping

| Criterion | Implementation |
|---|---|
| Returns `{ critical, high, medium, low, total }` | `SeveritySummary` struct with these fields, serialized via `Json` |
| 404 for missing SBOM | Service checks SBOM existence first, returns `AppError` 404 |
| Deduplicates by advisory ID | SQL query uses `DISTINCT` on advisory ID before counting |
| Defaults to 0 | `SeveritySummary::default()` initializes all counts to 0 |
| Response under 200ms for 500 advisories | Single aggregation query with GROUP BY, no N+1 |

---

## Verification

- Run `cargo build` to confirm compilation
- Run `cargo test` targeting the new test file to validate aggregation logic
- Manually verify the endpoint with a sample SBOM ID via `curl` or integration test
