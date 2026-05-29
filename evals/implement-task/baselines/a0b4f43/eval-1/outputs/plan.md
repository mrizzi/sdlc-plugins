# Implementation Plan: TC-9201

## Task Summary

**Jira Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Target Branch**: main

## Pre-Implementation Analysis (Sibling Code Inspection)

Before making any changes, I would inspect the following existing files to understand established patterns:

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** — Read to understand the existing GET handler pattern: how path parameters are extracted via `Path<Id>`, how the service is called, and how the JSON response is returned. This is the sibling endpoint handler that the new `severity_summary.rs` endpoint must mirror.

2. **`modules/fundamental/src/advisory/service/advisory.rs`** — Read to understand the `AdvisoryService` struct and its existing `fetch` and `list` methods. The new `severity_summary` method must follow the same signature pattern (taking `&self, sbom_id: Id, tx: &Transactional<'_>`) and error handling approach.

3. **`modules/fundamental/src/advisory/model/summary.rs`** — Read to understand the `AdvisorySummary` struct and its `severity` field. This is the source data structure whose severity values will be aggregated in the new summary endpoint.

4. **`common/src/error.rs`** — Read to understand the `AppError` enum and its `IntoResponse` implementation. All new code must return `Result<T, AppError>` and use `.context()` wrapping for error propagation, matching this module's conventions.

## Branch Strategy

Create branch **TC-9201** from the target branch **main**:

```
git checkout main && git pull origin main
git checkout -b TC-9201
```

## Files to Modify

### 1. `modules/fundamental/src/advisory/service/advisory.rs`

**Purpose**: Add a `severity_summary` method to `AdvisoryService`.

The new method follows the existing `fetch` and `list` method pattern:
- Signature: `pub async fn severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<SeveritySummary, AppError>`
- Queries the `sbom_advisory` join table to find advisories linked to the given SBOM ID
- For each linked advisory, reads the `severity` field from the `AdvisorySummary` model
- Deduplicates by advisory ID to avoid double-counting
- Aggregates counts per severity level (Critical, High, Medium, Low)
- Returns a `SeveritySummary` struct with counts and a total
- Uses `.context("Failed to fetch severity summary for SBOM")` for error wrapping

### 2. `modules/fundamental/src/advisory/endpoints/mod.rs`

**Purpose**: Register the new severity summary route.

Add an import for the new `severity_summary` handler module and register the route following the existing pattern of `Router::new().route("/path", get(handler))`:
- Add `mod severity_summary;` declaration
- Add `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get))` to the router chain

### 3. `modules/fundamental/src/advisory/model/mod.rs`

**Purpose**: Register the new `severity_summary` model module.

Add `pub mod severity_summary;` alongside the existing `pub mod summary;` and `pub mod details;` declarations.

## Files to Create

### 4. `modules/fundamental/src/advisory/model/severity_summary.rs`

**Purpose**: Define the `SeveritySummary` response struct.

- Define `SeveritySummary` with fields: `critical: u32`, `high: u32`, `medium: u32`, `low: u32`, `total: u32`
- Derive `Serialize`, `Deserialize`, `Debug`, `Clone`, `Default` (matching the derive pattern from sibling model structs like `AdvisorySummary`)
- Implement `Default` so all severity counts initialize to 0
- Add a constructor or builder method for convenience in the service layer

### 5. `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

**Purpose**: GET handler for `/api/v2/sbom/{id}/advisory-summary`.

Following the pattern observed in `advisory/endpoints/get.rs`:
- Extract the SBOM ID from the path using `Path<Id>`
- Obtain the `AdvisoryService` from the Axum state/extension
- Call `service.severity_summary(id, &tx).await`
- Return `Ok(Json(result))` on success
- Return 404 `AppError` when the SBOM ID does not exist, consistent with existing SBOM endpoints
- All errors wrapped with `.context()` and returned as `Result<Json<SeveritySummary>, AppError>`

### 6. `tests/api/advisory_summary.rs`

**Purpose**: Integration tests for the new endpoint.

Following the test patterns in `tests/api/advisory.rs` and `tests/api/sbom.rs`:
- **Test valid SBOM with known advisories**: Set up test data with an SBOM linked to advisories of known severities, call `GET /api/v2/sbom/{id}/advisory-summary`, assert correct counts per severity level
- **Test non-existent SBOM ID**: Call with an invalid ID, assert `resp.status() == StatusCode::NOT_FOUND`
- **Test SBOM with no advisories**: Create an SBOM with no advisory links, assert all counts are 0 and total is 0
- **Test deduplication**: Link the same advisory to an SBOM multiple times, assert it is counted only once

## Commit Plan

After implementing all changes, stage and commit with a Conventional Commits message and the `--trailer` flag:

```
git add \
  modules/fundamental/src/advisory/service/advisory.rs \
  modules/fundamental/src/advisory/endpoints/mod.rs \
  modules/fundamental/src/advisory/endpoints/severity_summary.rs \
  modules/fundamental/src/advisory/model/mod.rs \
  modules/fundamental/src/advisory/model/severity_summary.rs \
  tests/api/advisory_summary.rs

git commit -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary that returns per-severity
counts (critical, high, medium, low) and a total for advisories linked
to a given SBOM. Includes SeveritySummary model, AdvisoryService method,
endpoint handler, and integration tests.

Refs: TC-9201" \
  --trailer='Assisted-by: Claude Code'
```

## Scope Verification

All files in this plan fall within the scope defined by the task:

- **Modified files**: `advisory/service/advisory.rs`, `advisory/endpoints/mod.rs`, `advisory/model/mod.rs` -- all listed in "Files to Modify"
- **Created files**: `advisory/model/severity_summary.rs`, `advisory/endpoints/severity_summary.rs`, `tests/api/advisory_summary.rs` -- all listed in "Files to Create"
- **No unrelated files** are modified. The task notes `server/src/main.rs` requires no changes (routes auto-mount), so it is excluded.
