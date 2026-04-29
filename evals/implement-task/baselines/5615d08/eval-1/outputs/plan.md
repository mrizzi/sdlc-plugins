# Implementation Plan for TC-9201

## Task Summary

**Jira Issue**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Branch**: `TC-9201`

## Overview

Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. The endpoint returns a summary with counts per severity level (Critical, High, Medium, Low) and a total, enabling dashboard widgets to render severity breakdowns without client-side counting.

## Files to Modify

| # | File | Change Description |
|---|---|---|
| 1 | `modules/fundamental/src/advisory/service/advisory.rs` | Add `severity_summary` method to `AdvisoryService` |
| 2 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Register the new `/api/v2/sbom/{id}/advisory-summary` route |
| 3 | `modules/fundamental/src/advisory/model/mod.rs` | Add `pub mod severity_summary;` to register the new model module |

## Files to Create

| # | File | Description |
|---|---|---|
| 4 | `modules/fundamental/src/advisory/model/severity_summary.rs` | `SeveritySummary` response struct |
| 5 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | GET handler for `/api/v2/sbom/{id}/advisory-summary` |
| 6 | `tests/api/advisory_summary.rs` | Integration tests for the new endpoint |

## API Changes

- `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
  - Returns: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
  - 404 when SBOM ID does not exist
  - Deduplicates advisories by advisory ID
  - All severity levels default to 0

## Implementation Sequence

1. **Create the model** (`severity_summary.rs`) -- defines the response shape with no dependencies on new code.
2. **Register the model module** (`model/mod.rs`) -- add `pub mod severity_summary;`.
3. **Add the service method** (`advisory.rs`) -- implement `severity_summary` using the `sbom_advisory` join table and `AdvisorySummary.severity` field.
4. **Create the endpoint handler** (`endpoints/severity_summary.rs`) -- extract `Path<Id>`, call service, return `Json<SeveritySummary>`.
5. **Register the route** (`endpoints/mod.rs`) -- add `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary))`.
6. **Write integration tests** (`tests/api/advisory_summary.rs`) -- four test cases covering all acceptance criteria.

## Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary` (input)
  -> extract `Path<Id>` (parse)
  -> call `AdvisoryService::severity_summary(sbom_id, tx)` (processing)
  -> query `sbom_advisory` join table for advisories linked to SBOM (database)
  -> load `AdvisorySummary` for each advisory, read `severity` field (data access)
  -> deduplicate by advisory ID (processing)
  -> count by severity level (aggregation)
  -> return `Json<SeveritySummary>` with `{ critical, high, medium, low, total }` (output)
  -> **COMPLETE**

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary that returns advisory
severity counts (critical, high, medium, low, total) for a given SBOM.
Uses the sbom_advisory join table to find linked advisories and
deduplicates by advisory ID before counting.

Implements TC-9201
```

The commit would use `--trailer="Assisted-by: Claude Code"`.

## Branch Naming

Branch: `TC-9201` (named after the Jira issue ID per workflow conventions).

## PR Description

```markdown
## Summary
- Add `SeveritySummary` response struct for advisory severity counts
- Add `severity_summary` method to `AdvisoryService` that aggregates advisory severities per SBOM
- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint returning `{ critical, high, medium, low, total }`
- Add integration tests covering valid SBOM, non-existent SBOM (404), empty advisories, and deduplication

## Jira
Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
```

## Self-Verification Checklist

- [ ] Scope containment: all modified/created files match Files to Modify and Files to Create
- [ ] No sensitive patterns in diff (no passwords, API keys, secrets)
- [ ] Documentation currency: no public-facing docs describe the modified behavior (new endpoint, no existing docs to update)
- [ ] Duplication check: no existing severity aggregation logic found in codebase
- [ ] Contract verification: `SeveritySummary` struct derives required traits (`Serialize`, `Deserialize`)
- [ ] Sibling parity: endpoint follows same error handling, path extraction, and JSON response pattern as `get.rs`
- [ ] Data-flow trace: complete path from HTTP request to JSON response
- [ ] Cross-section reference consistency: `AdvisoryService` referenced in both `service/advisory.rs` (Files to Modify) and Implementation Notes -- paths consistent
