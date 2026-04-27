# Implementation Plan -- TC-9201

## Summary

Add an advisory severity aggregation service method and REST endpoint that returns
severity counts (Critical, High, Medium, Low, total) for a given SBOM, enabling
dashboard widgets to render severity breakdowns without client-side counting.

## Branch

```
git checkout -b TC-9201
```

## Files to Modify

### 1. `modules/fundamental/src/advisory/service/advisory.rs`

**What**: Add a `severity_summary` method to `AdvisoryService`.

**Why**: The new endpoint needs a service-layer method that queries the `sbom_advisory`
join table, joins to advisories, groups by severity, deduplicates by advisory ID, and
returns counts per severity level.

**Details**: See `outputs/file-1-description.md`.

### 2. `modules/fundamental/src/advisory/endpoints/mod.rs`

**What**: Register the new `/api/v2/sbom/{id}/advisory-summary` route pointing to the
`severity_summary` handler.

**Why**: The module's route registration file must include the new route so it is
mounted by the server.

**Details**: See `outputs/file-2-description.md`.

### 3. `modules/fundamental/src/advisory/model/mod.rs`

**What**: Add `pub mod severity_summary;` to register the new model module.

**Why**: Rust module system requires explicit registration of new sub-modules.

**Details**: See `outputs/file-3-description.md`.

## Files to Create

### 4. `modules/fundamental/src/advisory/model/severity_summary.rs`

**What**: Define the `SeveritySummary` response struct with fields for each severity
level and total.

**Details**: See `outputs/file-4-description.md`.

### 5. `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

**What**: Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary`.

**Details**: See `outputs/file-5-description.md`.

### 6. `tests/api/advisory_summary.rs`

**What**: Integration tests for the new endpoint covering success, 404, empty SBOM,
and deduplication scenarios.

**Details**: See `outputs/file-6-description.md`.

## Files NOT Modified

- `server/src/main.rs` -- no changes needed; routes auto-mount via module registration.
- `entity/src/sbom_advisory.rs` -- read-only usage; no schema changes needed.

## Cross-Section Reference Consistency

- Entity `AdvisoryService` -- Files to Modify references `advisory/service/advisory.rs`,
  Implementation Notes also references `advisory/service/advisory.rs`. **Consistent.**
- Entity `AdvisorySummary` -- Implementation Notes references `advisory/model/summary.rs`.
  This is a read-only reference (to access the `severity` field), not a file being modified. **Consistent.**
- Entity route registration -- Files to Modify references `advisory/endpoints/mod.rs`,
  Implementation Notes also references `advisory/endpoints/mod.rs`. **Consistent.**

## Data-Flow Trace

```
GET /api/v2/sbom/{id}/advisory-summary
  -> severity_summary handler (endpoints/severity_summary.rs)
     -> extract Path<Id> from URL
     -> call AdvisoryService::severity_summary(sbom_id, &tx)
        -> query sbom_advisory join table for given sbom_id
        -> join advisory table to get severity field
        -> deduplicate by advisory ID
        -> group by severity, count each level
        -> return SeveritySummary struct
     -> return Json(SeveritySummary) to client
```

**Status**: COMPLETE -- all stages (input, processing, output) are connected.

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to an SBOM.
Includes service method, response model, and integration tests.

Implements TC-9201
```

```
git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to an SBOM.
Includes service method, response model, and integration tests.

Implements TC-9201"
```

## Post-Commit

```
git push -u origin TC-9201
gh pr create --title "feat(advisory): add severity aggregation endpoint" \
  --body "## Summary

- Add GET /api/v2/sbom/{id}/advisory-summary endpoint returning severity counts per SBOM
- New SeveritySummary response model with critical/high/medium/low/total fields
- AdvisoryService::severity_summary method with deduplication by advisory ID
- Integration tests covering success, 404, empty SBOM, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)"
```
