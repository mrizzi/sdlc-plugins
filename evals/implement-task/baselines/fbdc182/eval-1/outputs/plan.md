# Implementation Plan — TC-9201

**Summary**: Add advisory severity aggregation service and endpoint  
**Branch**: `TC-9201`  
**Repository**: trustify-backend

---

## Pre-Implementation Inspection (Step 4)

Before writing any code, the following files would be read to understand existing patterns:

### Files to read for understanding (sibling analysis)

1. `modules/fundamental/src/advisory/endpoints/get.rs` — canonical handler pattern (Path extractor, service call, Json response)
2. `modules/fundamental/src/advisory/endpoints/mod.rs` — existing route registration to understand where and how to add the new route
3. `modules/fundamental/src/advisory/service/advisory.rs` — `fetch` and `list` method signatures to mirror with `severity_summary`
4. `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct, specifically the `severity` field shape
5. `modules/fundamental/src/advisory/model/mod.rs` — how existing model sub-modules are declared
6. `entity/src/sbom_advisory.rs` — join table entity definition (columns available for querying)
7. `entity/src/advisory.rs` — advisory entity (severity column name/type)
8. `common/src/error.rs` — `AppError` variants and `.context()` usage
9. `tests/api/advisory.rs` — test structure, assertion style, test setup helpers
10. `tests/api/sbom.rs` — additional test patterns (4xx case structure)
11. `CONVENTIONS.md` — CI check commands and project-level conventions

---

## Files to Modify

### 1. `modules/fundamental/src/advisory/model/mod.rs`
Add `pub mod severity_summary;` declaration to register the new model module.  
See: `outputs/file-1-model-mod.md`

### 2. `modules/fundamental/src/advisory/service/advisory.rs`
Add `severity_summary` async method to `AdvisoryService`.  
See: `outputs/file-2-service.md`

### 3. `modules/fundamental/src/advisory/endpoints/mod.rs`
Register the new route `/api/v2/sbom/{id}/advisory-summary` using the existing `Router::new().route(...)` pattern.  
See: `outputs/file-3-endpoints-mod.md`

---

## Files to Create

### 4. `modules/fundamental/src/advisory/model/severity_summary.rs`
New `SeveritySummary` response struct with `critical`, `high`, `medium`, `low`, `total` fields.  
See: `outputs/file-4-model-severity-summary.md`

### 5. `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
New Axum handler for `GET /api/v2/sbom/{id}/advisory-summary`.  
See: `outputs/file-5-endpoint-handler.md`

### 6. `tests/api/advisory_summary.rs`
Integration tests for the new endpoint covering: valid SBOM, non-existent SBOM (404), SBOM with no advisories (all zeros), duplicate advisory deduplication.  
See: `outputs/file-6-tests.md`

---

## Files NOT Modified

- `server/src/main.rs` — no changes needed; routes auto-mount via module registration (confirmed by task description)

---

## Data-Flow Verification

Request path: `GET /api/v2/sbom/{id}/advisory-summary`

1. Axum routes to `severity_summary` handler in `endpoints/severity_summary.rs` ✓
2. Handler extracts `Path<Id>` ✓
3. Handler calls `AdvisoryService::severity_summary(id, tx)` ✓
4. Service queries `sbom_advisory` join table, groups by severity, deduplicates on advisory ID ✓
5. Service constructs and returns `SeveritySummary` struct ✓
6. Handler wraps in `Json(result)` and returns ✓
7. `SeveritySummary` is registered in `model/mod.rs` so it is accessible from handler ✓
8. Route is registered in `endpoints/mod.rs` so Axum knows the path ✓

**Data flow: COMPLETE**

---

## Acceptance Criteria Mapping

| Criterion | Implementation |
|---|---|
| Returns `{ critical, high, medium, low, total }` | `SeveritySummary` struct with serde-serialized fields |
| Returns 404 when SBOM ID does not exist | Service checks SBOM existence first, returns `AppError::not_found()` |
| Counts only unique advisories | Query uses `DISTINCT` on advisory ID before aggregating |
| All severity levels default to 0 when no advisories | `SeveritySummary::default()` with all-zero fields |
| Response time < 200ms for ≤ 500 advisories | Single aggregation query with index on `sbom_id` in join table |

---

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
counts of unique advisories per severity level (Critical, High,
Medium, Low) and a total count. Enables dashboard widgets to render
severity breakdowns without client-side counting.

Implements TC-9201
```

Commit command:
```sh
git commit \
  --trailer="Assisted-by: Claude Code" \
  -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
counts of unique advisories per severity level (Critical, High,
Medium, Low) and a total count. Enables dashboard widgets to render
severity breakdowns without client-side counting.

Implements TC-9201"
```

---

## PR Description

```markdown
## Summary

- Add `SeveritySummary` response model with per-severity counts and total
- Add `AdvisoryService::severity_summary` method querying the `sbom_advisory` join table
- Add `GET /api/v2/sbom/{id}/advisory-summary` handler and route registration
- Add integration tests covering valid, 404, empty, and deduplication scenarios

## Test plan

- [ ] `cargo test` passes with all new tests in `tests/api/advisory_summary.rs` green
- [ ] `GET /api/v2/sbom/{known-id}/advisory-summary` returns correct severity counts
- [ ] `GET /api/v2/sbom/nonexistent/advisory-summary` returns HTTP 404
- [ ] Response for SBOM with no advisories returns all zeros
- [ ] Duplicate advisory entries are deduplicated in the count

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
```
