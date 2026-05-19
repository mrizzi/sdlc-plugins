# Implementation Plan for TC-9201

## Task Summary

Add an advisory severity aggregation service method and REST endpoint that returns severity counts (Critical, High, Medium, Low, Total) for a given SBOM, enabling dashboard widgets to render severity breakdowns without client-side counting.

## Branch

- Branch name: `TC-9201`
- Base branch: `main`

## Files to Create

| # | File | Purpose |
|---|---|---|
| 1 | `modules/fundamental/src/advisory/model/severity_summary.rs` | New `SeveritySummary` response struct with fields for critical, high, medium, low, and total counts |
| 2 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | GET handler for `/api/v2/sbom/{id}/advisory-summary` |
| 3 | `tests/api/advisory_summary.rs` | Integration tests for the new endpoint |

## Files to Modify

| # | File | Changes |
|---|---|---|
| 4 | `modules/fundamental/src/advisory/service/advisory.rs` | Add `severity_summary` method to `AdvisoryService` |
| 5 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Register the new `/api/v2/sbom/{id}/advisory-summary` route |
| 6 | `modules/fundamental/src/advisory/model/mod.rs` | Add `pub mod severity_summary;` to register the new model module |

## Files Not Modified

- `server/src/main.rs` -- routes auto-mount via module registration, no changes needed (as confirmed by the task description)

## Implementation Approach

### Step 1: Create the SeveritySummary model struct (File 1)
Define the response struct with derive macros for serialization. This is the data contract returned by the endpoint.

### Step 2: Add the service method (File 4)
Add `severity_summary` to `AdvisoryService` following the existing `fetch` and `list` method patterns. The method queries the `sbom_advisory` join table, joins to advisory to get severity, deduplicates by advisory ID, and counts by severity level.

### Step 3: Create the endpoint handler (File 2)
Implement the GET handler following the pattern in `endpoints/get.rs` -- extract path params via `Path<Id>`, call the service method, return JSON response.

### Step 4: Register the route (File 5)
Add the new route to `endpoints/mod.rs` following the existing `Router::new().route(...)` pattern.

### Step 5: Register the model module (File 6)
Add `pub mod severity_summary;` to `model/mod.rs`.

### Step 6: Write integration tests (File 3)
Write tests covering all four test requirements: valid SBOM with advisories, non-existent SBOM, SBOM with no advisories, and deduplication of advisory links.

## API Changes

- `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
  - Returns: `{ critical: u64, high: u64, medium: u64, low: u64, total: u64 }`
  - 404 when SBOM ID does not exist
  - Deduplicates advisories by advisory ID before counting

## Data-Flow Trace

- Input: HTTP GET request with SBOM ID path parameter
- Processing: `AdvisoryService::severity_summary` queries `sbom_advisory` join table, joins to advisory for severity, deduplicates by advisory ID, counts per severity level
- Output: JSON response with severity counts -- COMPLETE path

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to a given
SBOM. Enables dashboard widgets to render severity breakdowns without
client-side counting.

Implements TC-9201
```

With trailer: `--trailer="Assisted-by: Claude Code"`
