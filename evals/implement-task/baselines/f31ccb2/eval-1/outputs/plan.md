# Implementation Plan — TC-9201

## Summary

Add an advisory severity aggregation service method and REST endpoint that returns vulnerability severity counts (Critical, High, Medium, Low, total) for a given SBOM. This enables dashboard widgets to render severity breakdowns without client-side counting.

## Branch Information

- **Base branch**: `main`
- **Feature branch**: `feat/TC-9201-advisory-severity-summary`
- **Commit trailer**: `--trailer='Assisted-by: Claude Code'`

## Files to Create

| # | File Path | Purpose |
|---|-----------|---------|
| 1 | `modules/fundamental/src/advisory/model/severity_summary.rs` | `SeveritySummary` response struct |
| 2 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | GET handler for `/api/v2/sbom/{id}/advisory-summary` |
| 3 | `tests/api/advisory_summary.rs` | Integration tests for the new endpoint |

## Files to Modify

| # | File Path | Purpose |
|---|-----------|---------|
| 4 | `modules/fundamental/src/advisory/model/mod.rs` | Register the new `severity_summary` model module |
| 5 | `modules/fundamental/src/advisory/service/advisory.rs` | Add `severity_summary` method to `AdvisoryService` |
| 6 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Register the new route |

## Files Unchanged

- `server/src/main.rs` — No changes needed; routes auto-mount via module registration.

## Detailed Change Plan

### File 1: `modules/fundamental/src/advisory/model/severity_summary.rs` (CREATE)

Create a new response struct `SeveritySummary` with fields for each severity level count and a total. The struct derives `Serialize`, `Deserialize`, `Clone`, `Debug`, and `ToSchema` (for OpenAPI docs), following the pattern established by `advisory/model/summary.rs`. Includes a `Default` implementation so all counts start at zero, and a constructor/builder method for convenience.

### File 2: `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (CREATE)

Create a GET handler function following the pattern in `advisory/endpoints/get.rs`. The handler extracts the SBOM ID from the path via `Path<Id>`, calls `AdvisoryService::severity_summary()`, and returns the result as `Json<SeveritySummary>`. Returns 404 via `AppError` if the SBOM does not exist.

### File 3: `tests/api/advisory_summary.rs` (CREATE)

Create integration tests covering:
1. Valid SBOM with known advisories returns correct severity counts
2. Non-existent SBOM ID returns 404
3. SBOM with no advisories returns all zeros
4. Duplicate advisory links are deduplicated in the count

### File 4: `modules/fundamental/src/advisory/model/mod.rs` (MODIFY)

Add `pub mod severity_summary;` line to register the new model submodule, following the existing pattern of `pub mod summary;` and `pub mod details;`.

### File 5: `modules/fundamental/src/advisory/service/advisory.rs` (MODIFY)

Add a `severity_summary` method to `AdvisoryService` that:
1. Takes `&self, sbom_id: Id, tx: &Transactional<'_>`
2. Verifies the SBOM exists (returns 404 AppError if not)
3. Queries the `sbom_advisory` join table for advisories linked to the SBOM
4. Fetches `AdvisorySummary` for each linked advisory to access the `severity` field
5. Deduplicates by advisory ID
6. Counts advisories by severity level (Critical, High, Medium, Low)
7. Returns `Result<SeveritySummary, AppError>`

### File 6: `modules/fundamental/src/advisory/endpoints/mod.rs` (MODIFY)

Add a `mod severity_summary;` declaration and register the new route:
```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary that returns aggregated
vulnerability severity counts (critical, high, medium, low, total)
for a given SBOM. Includes SeveritySummary model, AdvisoryService
method with deduplication, and integration tests.

TC-9201
```

Note: Commit with `--trailer='Assisted-by: Claude Code'`

## Implementation Order

1. Create `severity_summary.rs` model (no dependencies)
2. Modify `model/mod.rs` to register the module
3. Add `severity_summary` method to `AdvisoryService`
4. Create endpoint handler
5. Register route in `endpoints/mod.rs`
6. Create integration tests
7. Run `cargo check` and `cargo test` to verify

## Verification

- `cargo check` — ensures compilation
- `cargo test` — runs all tests including new integration tests
- Manual test: `curl http://localhost:8080/api/v2/sbom/{id}/advisory-summary` against a running instance with test data
