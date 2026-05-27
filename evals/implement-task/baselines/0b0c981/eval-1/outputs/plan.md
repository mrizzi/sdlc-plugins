# Implementation Plan: TC-9201

## Summary
Add a severity aggregation service method and REST endpoint that returns advisory severity counts (Critical, High, Medium, Low, total) for a given SBOM. This enables dashboard widgets to render severity breakdowns without client-side counting.

## Branch
- Base: `main`
- Branch name: `TC-9201`

## Files to Create

### 1. `modules/fundamental/src/advisory/model/severity_summary.rs`
New model struct `SeveritySummary` representing the aggregated severity counts response.

### 2. `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
New Axum GET handler for `GET /api/v2/sbom/{id}/advisory-summary` that extracts the SBOM ID from the path, calls the service, and returns JSON.

### 3. `tests/api/advisory_summary.rs`
Integration tests covering:
- Valid SBOM with known advisories returns correct severity counts
- Non-existent SBOM ID returns 404
- SBOM with no advisories returns all zeros
- Duplicate advisory links are deduplicated in the count

## Files to Modify

### 4. `modules/fundamental/src/advisory/model/mod.rs`
Add `pub mod severity_summary;` to register the new model module.

### 5. `modules/fundamental/src/advisory/service/advisory.rs`
Add `severity_summary` method to `AdvisoryService` that queries the `sbom_advisory` join table, fetches linked advisories, deduplicates by advisory ID, counts by severity level, and returns a `SeveritySummary`.

### 6. `modules/fundamental/src/advisory/endpoints/mod.rs`
Register the new route: `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get))`.

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary that returns aggregated
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes deduplication by advisory ID and
404 handling for missing SBOMs.

Ref: TC-9201
Assisted-by: Claude Code
```

## Acceptance Criteria Verification

| Criterion | How Verified |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns correct shape | Response struct enforces `{ critical, high, medium, low, total }` fields |
| Returns 404 for non-existent SBOM ID | Service checks SBOM existence first, returns AppError 404 |
| Counts only unique advisories | Deduplication by advisory ID using HashSet or DISTINCT in query |
| Severity levels default to 0 | SeveritySummary fields initialized to 0, incremented per match |
| Response time under 200ms for 500 advisories | Single SQL query with JOIN and GROUP BY avoids N+1; integration test validates |
