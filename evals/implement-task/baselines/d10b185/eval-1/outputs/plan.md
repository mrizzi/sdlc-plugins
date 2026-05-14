# Implementation Plan: TC-9201 -- Advisory Severity Aggregation

## Task Summary

Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM, returning counts per severity level (Critical, High, Medium, Low) and a total.

## Target Branch

`main`

## Branch Name

`TC-9201`

## Files to Create

| # | File Path | Purpose |
|---|-----------|---------|
| 1 | `modules/fundamental/src/advisory/model/severity_summary.rs` | `SeveritySummary` response struct |
| 2 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | GET handler for `/api/v2/sbom/{id}/advisory-summary` |
| 3 | `tests/api/advisory_summary.rs` | Integration tests for the new endpoint |

## Files to Modify

| # | File Path | Change Description |
|---|-----------|-------------------|
| 4 | `modules/fundamental/src/advisory/service/advisory.rs` | Add `severity_summary` method to `AdvisoryService` |
| 5 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Register the new `/api/v2/sbom/{id}/advisory-summary` route |
| 6 | `modules/fundamental/src/advisory/model/mod.rs` | Add `pub mod severity_summary;` to expose the new model module |

## Files NOT Modified

- `server/src/main.rs` -- No changes needed. Routes auto-mount via module registration as stated in the task description.

## Implementation Order

1. **Model first** -- Create `SeveritySummary` struct (file 1) and register it in model `mod.rs` (file 6). This establishes the response type before anything depends on it.
2. **Service method** -- Add `severity_summary` to `AdvisoryService` (file 4). This implements the data aggregation logic.
3. **Endpoint handler** -- Create the GET handler (file 2) and register the route (file 5). This wires the service to HTTP.
4. **Tests** -- Create integration tests (file 3) covering all acceptance criteria.

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to a given
SBOM. Includes SeveritySummary model, AdvisoryService.severity_summary
method, endpoint handler, and integration tests.

Refs: TC-9201
Assisted-by: Claude Code
```

## Git Commands

```bash
git checkout main
git pull origin main
git checkout -b TC-9201
# ... make changes ...
git add modules/fundamental/src/advisory/model/severity_summary.rs \
       modules/fundamental/src/advisory/model/mod.rs \
       modules/fundamental/src/advisory/service/advisory.rs \
       modules/fundamental/src/advisory/endpoints/severity_summary.rs \
       modules/fundamental/src/advisory/endpoints/mod.rs \
       tests/api/advisory_summary.rs
git commit --trailer='Assisted-by: Claude Code' -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to a given
SBOM. Includes SeveritySummary model, AdvisoryService.severity_summary
method, endpoint handler, and integration tests.

Refs: TC-9201"
```

## Verification Plan

1. `cargo check` -- Ensure the project compiles without errors.
2. `cargo test --test advisory_summary` -- Run the new integration tests.
3. `cargo clippy` -- Verify no linting warnings on new code.
4. Manual curl test against local dev server: `curl http://localhost:8080/api/v2/sbom/{test-id}/advisory-summary` to verify JSON shape and 404 behavior.
