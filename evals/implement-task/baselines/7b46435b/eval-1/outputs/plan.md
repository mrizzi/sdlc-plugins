# Implementation Plan for TC-9201

## Task Summary

Add an advisory severity aggregation service method and REST endpoint that returns
severity counts (Critical, High, Medium, Low, total) for a given SBOM. The endpoint
is `GET /api/v2/sbom/{id}/advisory-summary`.

## Pre-Implementation Validation

### Project Configuration (Step 0)
- Repository Registry: trustify-backend with Serena instance `serena_backend` -- valid
- Jira Configuration: Project key TC, Cloud ID, custom fields -- valid
- Code Intelligence: Serena with rust-analyzer, tool naming convention -- valid

### Task Parsing (Step 1)
- Repository: trustify-backend
- Target Branch: main
- No Target PR (standard flow)
- No Bookend Type (standard flow)
- No Dependencies
- GitHub Issue custom field: customfield_10747 (check for linked GitHub issue)
- Git Pull Request custom field: customfield_10875

### Description Integrity (Step 1.5)
- Would fetch comments to verify description digest. Skipped per eval constraints.

### Dependencies (Step 2)
- No dependencies listed. Proceeding.

### Jira Transition (Step 3)
- Would assign to current user and transition to In Progress. Skipped per eval constraints.

### Cross-Section Reference Consistency Check
- Entity `AdvisoryService`: Files to Modify says `modules/fundamental/src/advisory/service/advisory.rs`, Implementation Notes also references `modules/fundamental/src/advisory/service/advisory.rs` -- CONSISTENT
- Entity `AdvisorySummary`: Implementation Notes references `modules/fundamental/src/advisory/model/summary.rs` (existing struct with severity field) -- this is the existing struct, not the new one. The new struct is `SeveritySummary` in Files to Create. No conflict.
- Route registration: Both Files to Modify and Implementation Notes reference `modules/fundamental/src/advisory/endpoints/mod.rs` -- CONSISTENT

## Branch

```
git checkout main
git pull
git checkout -b TC-9201
```

## Files to Create (3 files)

### File 1: `modules/fundamental/src/advisory/model/severity_summary.rs`
- New model struct `SeveritySummary` with fields: critical, high, medium, low, total (all u64 or i64)
- Derives: Serialize, Deserialize, Debug, Clone
- Default implementation with all zeros
- See outputs/file-1-description.md for details

### File 2: `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- GET handler for `/api/v2/sbom/{id}/advisory-summary`
- Extracts SBOM ID from path via `Path<Id>`
- Calls `AdvisoryService::severity_summary()`
- Returns `Result<Json<SeveritySummary>, AppError>`
- See outputs/file-2-description.md for details

### File 3: `tests/api/advisory_summary.rs`
- Integration tests for the new endpoint
- 4 test functions covering acceptance criteria and test requirements
- See outputs/file-3-description.md for details

## Files to Modify (3 files)

### File 4: `modules/fundamental/src/advisory/service/advisory.rs`
- Add `severity_summary` method to `AdvisoryService`
- See outputs/file-4-description.md for details

### File 5: `modules/fundamental/src/advisory/endpoints/mod.rs`
- Register the new route for the severity summary endpoint
- See outputs/file-5-description.md for details

### File 6: `modules/fundamental/src/advisory/model/mod.rs`
- Add `pub mod severity_summary;` to register the new model module
- See outputs/file-6-description.md for details

## Files NOT Modified
- `server/src/main.rs` -- no changes needed (routes auto-mount via module registration), as stated in the task

## Acceptance Criteria Verification

1. GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }` -- Satisfied by the endpoint handler returning `SeveritySummary` struct serialized as JSON
2. Returns 404 when SBOM ID does not exist -- Satisfied by checking SBOM existence before querying advisories, returning AppError with NOT_FOUND
3. Counts only unique advisories (deduplicates by advisory ID) -- Satisfied by using a HashSet or DISTINCT in the query to deduplicate advisory IDs
4. All severity levels default to 0 when no advisories exist at that level -- Satisfied by Default implementation on SeveritySummary initializing all counts to 0
5. Response time under 200ms for SBOMs with up to 500 advisories -- Satisfied by using a single aggregation query rather than fetching all advisories and counting in application code

## Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract Path(id) -> call `AdvisoryService::severity_summary(id, tx)` -> query `sbom_advisory` join table for SBOM -> join with advisory table to get severity -> aggregate counts by severity level -> return `SeveritySummary` struct -> serialize to JSON response -- COMPLETE

## Self-Verification Notes

### Scope containment
- All 6 files are listed in either "Files to Modify" or "Files to Create" in the task description. No out-of-scope changes.

### Duplication check
- The `SeveritySummary` struct is distinct from the existing `AdvisorySummary` struct in `model/summary.rs`. `AdvisorySummary` represents a single advisory's summary (including its severity field), while `SeveritySummary` aggregates counts across multiple advisories. No duplication.
- The `severity_summary` service method performs aggregation logic not present in existing `fetch` or `list` methods. No duplication.

### Documentation impact
- The new endpoint should be documented in `docs/api.md` if it exists and covers the REST API reference. This is a lightweight addition (one new endpoint entry).

## Commit Message

```
feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to an SBOM.
Includes SeveritySummary model, AdvisoryService.severity_summary() method,
endpoint handler, and integration tests.

Implements TC-9201
```

## PR Description

```
## Summary

Add advisory severity aggregation service and REST endpoint for dashboard
severity breakdown widgets.

- Add `SeveritySummary` response model with critical/high/medium/low/total counts
- Add `AdvisoryService::severity_summary()` method that aggregates advisory severities for an SBOM
- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- Add integration tests covering valid SBOM, non-existent SBOM (404), empty advisories, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)

## Test plan

- [ ] Test that a valid SBOM with known advisories returns correct severity counts
- [ ] Test that a non-existent SBOM ID returns 404
- [ ] Test that an SBOM with no advisories returns all zeros
- [ ] Test that duplicate advisory links are deduplicated in the count
```
