# Implementation Plan: TC-9201 -- Add Advisory Severity Aggregation Service and Endpoint

## Task Summary

Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. The endpoint `GET /api/v2/sbom/{id}/advisory-summary` returns a JSON object with counts per severity level (Critical, High, Medium, Low) and a total.

## Project Configuration Validation

- **Repository Registry**: `trustify-backend` found in Registry with Serena instance `serena_backend` at path `./`.
- **Jira Configuration**: Project key `TC` matches task key `TC-9201`. Cloud ID, issue type, and custom fields are configured.
- **Code Intelligence**: Serena instance `serena_backend` configured with `rust-analyzer` language server. Available for code analysis.

## Branch

```
TC-9201-advisory-severity-summary
```

## Scope Analysis

### Files to Modify (3 files)

| # | File | Change |
|---|---|---|
| 1 | `modules/fundamental/src/advisory/model/mod.rs` | Add `pub mod severity_summary;` to register new model module |
| 2 | `modules/fundamental/src/advisory/service/advisory.rs` | Add `severity_summary` method to `AdvisoryService` |
| 3 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Register new route and module declaration |

### Files to Create (3 files)

| # | File | Purpose |
|---|---|---|
| 4 | `modules/fundamental/src/advisory/model/severity_summary.rs` | `SeveritySummary` response struct |
| 5 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | GET handler for `/api/v2/sbom/{id}/advisory-summary` |
| 6 | `tests/api/advisory_summary.rs` | Integration tests (4 test cases) |

### Files Explicitly NOT Modified

- `server/src/main.rs` -- Task states "no changes needed (routes auto-mount via module registration)"

## Implementation Order

1. **Create the model** (`severity_summary.rs`) -- Define the `SeveritySummary` struct with `critical`, `high`, `medium`, `low`, `total` fields. Derive `Serialize`, `Deserialize`, `Debug`, `Clone`, `Default`.

2. **Register the model** (`model/mod.rs`) -- Add `pub mod severity_summary;` declaration.

3. **Add the service method** (`service/advisory.rs`) -- Implement `severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<SeveritySummary, anyhow::Error>` that:
   - Queries `sbom_advisory` join table for advisory IDs linked to the SBOM
   - Deduplicates by advisory ID using `HashSet`
   - Fetches each unique advisory's severity via the existing `fetch` method
   - Counts by severity level, defaults to 0 for missing levels
   - Computes `total` as sum of all severity counts

4. **Create the endpoint handler** (`endpoints/severity_summary.rs`) -- Async handler that extracts `Path(id)`, calls `service.severity_summary(id, &tx)`, returns `Json(summary)` or `AppError`.

5. **Register the route** (`endpoints/mod.rs`) -- Add `mod severity_summary;` and `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_advisory_summary))`.

6. **Write integration tests** (`tests/api/advisory_summary.rs`) -- Four test cases:
   - Valid SBOM with known advisories returns correct counts
   - Non-existent SBOM returns 404
   - SBOM with no advisories returns all zeros
   - Duplicate advisory links are deduplicated

## Convention Conformance Summary

- Model: single struct per file, standard derives, registered in `mod.rs`
- Service: method signature matches `fetch`/`list` pattern (`&self`, ID, transactional ref)
- Endpoint: one handler per file, Axum extractors, `Result<Json<T>, AppError>` return type
- Error handling: `.context()` wrapping throughout, `AppError` for HTTP error mapping
- Testing: `#[tokio::test]`, real PostgreSQL database, `StatusCode` assertions
- Naming: snake_case files, PascalCase structs, kebab-case URL paths

## Scope Containment Verification

All changes are confined to the files listed in the task's "Files to Modify" and "Files to Create" sections. No out-of-scope files are touched. Specifically:

- No changes to `server/src/main.rs` (confirmed by task)
- No changes to `entity/` (using existing `sbom_advisory` entity as-is)
- No changes to `common/` (using existing `AppError` as-is)
- No changes to any other module (`sbom`, `package`, `ingestor`, `search`)

## Acceptance Criteria Traceability

| Criterion | Addressed By |
|---|---|
| GET endpoint returns `{ critical, high, medium, low, total }` | Endpoint handler + SeveritySummary struct |
| Returns 404 for non-existent SBOM | AppError propagation from service layer |
| Counts only unique advisories | HashSet deduplication in service method |
| Severity levels default to 0 | `SeveritySummary::default()` (all fields are `u32`, default 0) |
| Response time under 200ms for 500 advisories | Addressed by design; single query for join table, batch processing |

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated severity counts (critical, high, medium, low, total) for
advisories linked to a given SBOM. Includes SeveritySummary model,
AdvisoryService.severity_summary method, and integration tests.

Refs: TC-9201
Assisted-by: Claude Code
```

## Detailed File Descriptions

See individual file description documents:

- `file-1-description.md` -- `model/severity_summary.rs` (CREATE)
- `file-2-description.md` -- `model/mod.rs` (MODIFY)
- `file-3-description.md` -- `service/advisory.rs` (MODIFY)
- `file-4-description.md` -- `endpoints/severity_summary.rs` (CREATE)
- `file-5-description.md` -- `endpoints/mod.rs` (MODIFY)
- `file-6-description.md` -- `tests/api/advisory_summary.rs` (CREATE)
