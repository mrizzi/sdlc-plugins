# Implementation Plan for TC-9201

## Task Summary

**Jira Issue**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Branch**: `TC-9201`
**Status**: To Do (would transition to In Progress)
**Dependencies**: None
**Target PR**: None (default flow -- new branch and PR)
**Parent feature**: TC-9001 (is incorporated by)

## Description

Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. The endpoint returns a summary with counts per severity level (Critical, High, Medium, Low) and a total, enabling dashboard widgets to render severity breakdowns without client-side counting.

## Project Configuration Validation (Step 0)

Verified CLAUDE.md contains:
- Repository Registry: trustify-backend with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID
- Code Intelligence: Tool naming convention `mcp__serena_backend__<tool>`

All required sections present. Proceed.

## Cross-Section Reference Consistency Check

Before implementation, checked for path consistency across task sections:

| Entity | Files to Modify | Implementation Notes | Consistent? |
|---|---|---|---|
| AdvisoryService | `modules/fundamental/src/advisory/service/advisory.rs` | `modules/fundamental/src/advisory/service/advisory.rs` | Yes |
| Endpoint pattern | `modules/fundamental/src/advisory/endpoints/mod.rs` | `modules/fundamental/src/advisory/endpoints/get.rs` (reference) | Yes (different files, complementary roles) |
| AdvisorySummary | — | `modules/fundamental/src/advisory/model/summary.rs` | Yes (read-only reference) |
| Model module | `modules/fundamental/src/advisory/model/mod.rs` | — | Yes |
| Join table | — | `entity/src/sbom_advisory.rs` | Yes (read-only reference) |
| Error handling | — | `common/src/error.rs` | Yes (read-only reference) |

No cross-section reference inconsistencies detected.

## Files to Create

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- SeveritySummary response struct
   - See: `outputs/file-1-description.md`

2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- GET handler for /api/v2/sbom/{id}/advisory-summary
   - See: `outputs/file-2-description.md`

3. **`tests/api/advisory_summary.rs`** -- Integration tests for the new endpoint
   - See: `outputs/file-3-description.md`

## Files to Modify

4. **`modules/fundamental/src/advisory/model/mod.rs`** -- Register the new model module
   - See: `outputs/file-4-description.md`

5. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Register the new route
   - See: `outputs/file-5-description.md`

6. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Add `severity_summary` method
   - See: `outputs/file-6-description.md`

## Files NOT Modified (confirmed)

- **`server/src/main.rs`** -- No changes needed; routes auto-mount via module registration as stated in the task description.

## API Changes

- `GET /api/v2/sbom/{id}/advisory-summary` -- **NEW**
  - Returns: `{ critical: u64, high: u64, medium: u64, low: u64, total: u64 }`
  - 404 when SBOM ID does not exist
  - Deduplicates advisories by advisory ID
  - All severity levels default to 0

## Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary`
  - Input: HTTP GET request with SBOM ID path parameter -> **COMPLETE** (extracted via `Path<Id>`)
  - Processing: `AdvisoryService::severity_summary()` queries `sbom_advisory` join table, joins to advisory for severity, deduplicates by advisory ID, counts per severity level -> **COMPLETE**
  - Output: JSON response with `SeveritySummary` struct -> **COMPLETE** (Axum `Json` extractor handles serialization)
  - Error path: SBOM not found -> 404 `AppError` -> **COMPLETE**

**All data-flow paths are complete.**

## Scope Containment

All files in the plan are within the scope defined by the task's "Files to Modify" and "Files to Create" sections. No out-of-scope files are modified.

## Duplication Check

- No existing severity aggregation logic found in the codebase (the task is creating new functionality)
- The `AdvisorySummary` struct in `model/summary.rs` has a `severity` field that will be reused for counting -- no duplication
- The join table `entity/src/sbom_advisory.rs` is an existing entity being queried, not duplicated

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for all
advisories linked to a given SBOM. Includes deduplication by
advisory ID and proper 404 handling for non-existent SBOMs.

Implements TC-9201
```

The commit would include `--trailer="Assisted-by: Claude Code"`.

## Branch and PR

- **Branch name**: `TC-9201`
- **PR title**: `feat(advisory): add severity aggregation endpoint for SBOM advisories`
- **PR description** would include:
  - Summary of changes
  - `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)` (clickable Jira link)
  - Reference to acceptance criteria

## Jira Updates (Step 11)

After merge-ready state:
1. Update `customfield_10875` (Git Pull Request) with PR URL in ADF format
2. Add comment summarizing changes with PR link
3. Transition TC-9201 to "In Review"

## Documentation Impact

- No existing API documentation files were identified as directly describing advisory endpoints at the file level
- The `docs/api.md` file referenced in CLAUDE.md would need to be checked and updated if it contains an endpoint catalog, to add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- No `CONVENTIONS.md` changes needed (the implementation follows all existing conventions)

## CI Verification Plan

Since no specific CI commands were extracted from CONVENTIONS.md, the fallback approach would be:
1. `cargo build` -- verify compilation
2. `cargo test` -- run all tests including new integration tests
3. `cargo clippy` -- check for lint warnings
4. `cargo fmt --check` -- verify formatting
