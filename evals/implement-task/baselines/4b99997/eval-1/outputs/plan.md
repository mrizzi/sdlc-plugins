# Implementation Plan for TC-9201

## Task Summary

**Jira ID**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Status**: To Do
**Dependencies**: None
**Target PR**: None (default flow -- new branch and PR)

## Description

Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. The endpoint returns a summary with counts per severity level (Critical, High, Medium, Low) and a total, enabling dashboard widgets to render severity breakdowns without client-side counting.

## Pre-Implementation Checks

### Project Configuration Validation
- Repository Registry: trustify-backend with Serena instance serena_backend -- VALID
- Jira Configuration: Project key TC, Cloud ID present, Feature issue type ID present -- VALID
- Code Intelligence: serena_backend with rust-analyzer -- VALID

### Dependency Verification
- No dependencies -- PASS

### Cross-Section Reference Consistency
- All entity-to-file-path references are consistent across task sections -- PASS

## Files to Create

| # | File Path | Description |
|---|-----------|-------------|
| 1 | `modules/fundamental/src/advisory/model/severity_summary.rs` | SeveritySummary response struct |
| 2 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | GET handler for `/api/v2/sbom/{id}/advisory-summary` |
| 3 | `tests/api/advisory_summary.rs` | Integration tests for the new endpoint |

## Files to Modify

| # | File Path | Description |
|---|-----------|-------------|
| 4 | `modules/fundamental/src/advisory/service/advisory.rs` | Add `severity_summary` method to AdvisoryService |
| 5 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Register the new `/api/v2/sbom/{id}/advisory-summary` route |
| 6 | `modules/fundamental/src/advisory/model/mod.rs` | Add `pub mod severity_summary;` to register the new model module |

## Files NOT Modified

- `server/src/main.rs` -- No changes needed (routes auto-mount via module registration, as confirmed by task description)

## API Changes

- **NEW**: `GET /api/v2/sbom/{id}/advisory-summary`
  - Response body: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
  - Returns 404 when SBOM ID does not exist
  - Deduplicates advisories by advisory ID
  - All severity levels default to 0

## Implementation Order

1. Create the `SeveritySummary` model struct (file-1)
2. Register the model module in `model/mod.rs` (file-6)
3. Add the `severity_summary` service method (file-4)
4. Create the endpoint handler (file-2)
5. Register the route in `endpoints/mod.rs` (file-5)
6. Write integration tests (file-3)
7. Run tests (`cargo test`)
8. Verify acceptance criteria
9. Self-verification (scope, sensitive patterns, data-flow, contract parity)

## Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary`
  - **Input**: HTTP GET request with SBOM ID path parameter
  - **Extract**: Axum `Path<Id>` extracts `sbom_id`
  - **Process**: Handler calls `AdvisoryService::severity_summary(sbom_id, tx)`
  - **Query**: Service queries `sbom_advisory` join table to find advisories linked to the SBOM
  - **Aggregate**: Service loads `AdvisorySummary` records, extracts `severity` field, deduplicates by advisory ID, counts per severity level
  - **Build response**: Constructs `SeveritySummary { critical, high, medium, low, total }`
  - **Output**: Returns `Json<SeveritySummary>` with HTTP 200, or `AppError` 404 if SBOM not found
  - **Status**: COMPLETE -- all stages connected

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, service
method, endpoint handler, and integration tests.

Implements TC-9201
```

The commit would include `--trailer="Assisted-by: Claude Code"`.

## Branch

```
git checkout -b TC-9201
```

## PR Description

```
## Summary

Add advisory severity aggregation service and REST endpoint for SBOM
dashboard widgets.

- New `GET /api/v2/sbom/{id}/advisory-summary` endpoint returning
  severity counts (critical, high, medium, low, total)
- SeveritySummary response model
- AdvisoryService.severity_summary() method with deduplication
- Integration tests covering happy path, 404, empty, and dedup cases

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
```

## Jira Updates

1. Transition TC-9201 to "In Progress" at start
2. Assign to current user
3. After PR creation: update Git Pull Request custom field (`customfield_10875`) with PR URL
4. Add comment with PR link, summary of changes, and confirmation of no deviations
5. Transition TC-9201 to "In Review"
