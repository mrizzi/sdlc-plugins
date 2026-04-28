# Implementation Plan for TC-9201

## Task Summary

**Jira Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend

Add a service method and REST endpoint that aggregates vulnerability advisory severity
counts for a given SBOM. The endpoint returns a summary with counts per severity level
(Critical, High, Medium, Low) and a total, enabling dashboard widgets to render severity
breakdowns without client-side counting.

## Pre-Implementation Checks

### Step 0 -- Validate Project Configuration
- Repository Registry: present (trustify-backend with serena_backend instance)
- Jira Configuration: present (Project key TC, Cloud ID, Feature issue type ID, custom fields)
- Code Intelligence: present (serena_backend with rust-analyzer)
- **Result**: PASS -- all required sections present.

### Step 1 -- Parse Structured Description
- Repository: trustify-backend
- Description: present
- Files to Modify: 3 files listed
- Files to Create: 3 files listed
- API Changes: 1 new endpoint
- Implementation Notes: present with pattern references
- Acceptance Criteria: 5 items
- Test Requirements: 4 items
- Target PR: none (default flow -- create new branch and PR)
- Dependencies: none
- **Result**: PASS -- all required sections present and well-structured.

### Step 2 -- Verify Dependencies
- No dependencies listed.
- **Result**: PASS.

### Step 4 -- Code Understanding (Sibling Analysis)
- Inspected sibling modules: `sbom/`, `advisory/`, `package/` under `modules/fundamental/src/`
- Confirmed model/service/endpoints tripartite pattern
- Confirmed endpoint handler patterns in `advisory/endpoints/get.rs`
- Confirmed service method patterns in `advisory/service/advisory.rs`
- Confirmed model struct patterns in `advisory/model/summary.rs`
- Confirmed test patterns in `tests/api/advisory.rs` and `tests/api/sbom.rs`
- Identified `CONVENTIONS.md` at repo root (would be read for CI check commands)
- Identified `entity/src/sbom_advisory.rs` as the join table entity for SBOM-Advisory linkage
- Full conventions documented in `outputs/conventions.md`

## Files to Modify

| # | File | Change Description |
|---|---|---|
| 1 | `modules/fundamental/src/advisory/service/advisory.rs` | Add `severity_summary` method to `AdvisoryService` |
| 2 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Register the new `/api/v2/sbom/{id}/advisory-summary` route |
| 3 | `modules/fundamental/src/advisory/model/mod.rs` | Add `pub mod severity_summary;` declaration |

## Files to Create

| # | File | Description |
|---|---|---|
| 4 | `modules/fundamental/src/advisory/model/severity_summary.rs` | `SeveritySummary` response struct |
| 5 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | GET handler for `/api/v2/sbom/{id}/advisory-summary` |
| 6 | `tests/api/advisory_summary.rs` | Integration tests for the new endpoint |

## Implementation Order

1. **File 4** -- Create `SeveritySummary` model struct (no dependencies on other new code)
2. **File 3** -- Register the new model module in `model/mod.rs`
3. **File 1** -- Add `severity_summary` service method to `AdvisoryService`
4. **File 5** -- Create the endpoint handler
5. **File 2** -- Register the route in `endpoints/mod.rs`
6. **File 6** -- Write integration tests

## Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary`
  - Input: HTTP request with SBOM ID path parameter -> extracted via `Path<Id>` -- PLANNED
  - Processing: handler calls `AdvisoryService::severity_summary(sbom_id, tx)` -- PLANNED
  - Service queries `sbom_advisory` join table for advisories linked to SBOM -- PLANNED
  - Service joins with advisory data to get severity field from `AdvisorySummary` -- PLANNED
  - Service deduplicates by advisory ID and counts per severity level -- PLANNED
  - Output: returns `SeveritySummary { critical, high, medium, low, total }` as JSON -- PLANNED
  - Error path: returns 404 via `AppError` if SBOM ID does not exist -- PLANNED
  - **Result**: COMPLETE data flow planned from request to response.

## Scope Containment

All planned changes are within the task's Files to Modify and Files to Create lists.
No out-of-scope files are modified. `server/src/main.rs` is explicitly noted as not
needing changes (routes auto-mount via module registration).

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to an SBOM.
Includes SeveritySummary model, AdvisoryService.severity_summary method,
and integration tests.

Implements TC-9201
```

Commit would include `--trailer="Assisted-by: Claude Code"`.

## PR Description

```
## Summary

- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint returning severity counts (critical, high, medium, low, total) for advisories linked to an SBOM
- Add `SeveritySummary` model struct, `AdvisoryService::severity_summary` method, and endpoint handler following existing advisory module patterns
- Add integration tests covering valid SBOM, non-existent SBOM (404), empty advisories, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
```

## Acceptance Criteria Verification Plan

| Criterion | Verification Method |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` | Endpoint handler returns `SeveritySummary` struct; integration test validates response shape |
| Returns 404 when SBOM ID does not exist | Service returns `AppError` not-found; test `test_advisory_summary_nonexistent_sbom` validates 404 |
| Counts only unique advisories (deduplicates by advisory ID) | Service uses `HashSet` or `DISTINCT` in query; test `test_advisory_summary_deduplication` validates |
| All severity levels default to 0 when no advisories | `SeveritySummary` fields initialize to 0; test `test_advisory_summary_empty_sbom` validates |
| Response time under 200ms for SBOMs with up to 500 advisories | Single query with join and GROUP BY; no N+1 queries; performance validated by design |
