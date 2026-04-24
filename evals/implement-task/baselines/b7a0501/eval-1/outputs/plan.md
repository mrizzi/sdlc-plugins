# Implementation Plan for TC-9201

## Task Summary

**Jira Issue**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Branch**: `TC-9201`

Add a `GET /api/v2/sbom/{id}/advisory-summary` endpoint that returns aggregated
vulnerability advisory severity counts (critical, high, medium, low, total) for a
given SBOM. This enables dashboard widgets to render severity breakdowns without
client-side counting.

---

## Project Configuration Validation

- Repository Registry: trustify-backend found with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID all present
- Code Intelligence: Serena instance `serena_backend` configured with `rust-analyzer`
- Dependencies: None -- no blocking tasks

---

## Files Overview

### Files to Create

| # | File | Purpose |
|---|------|---------|
| 1 | `modules/fundamental/src/advisory/model/severity_summary.rs` | `SeveritySummary` response struct |
| 2 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | GET handler for `/api/v2/sbom/{id}/advisory-summary` |
| 3 | `tests/api/advisory_summary.rs` | Integration tests for the new endpoint |

### Files to Modify

| # | File | Purpose |
|---|------|---------|
| 4 | `modules/fundamental/src/advisory/service/advisory.rs` | Add `severity_summary` method to `AdvisoryService` |
| 5 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Register the new severity summary route |
| 6 | `modules/fundamental/src/advisory/model/mod.rs` | Add `pub mod severity_summary;` to register the model module |

### Files Confirmed Unchanged

- `server/src/main.rs` -- routes auto-mount via module registration; no changes needed

---

## Convention Conformance

All changes follow the conventions discovered from sibling analysis (see `conventions.md`):

- **Module structure**: New files placed in existing `model/`, `service/`, `endpoints/` directories
- **Endpoint pattern**: Handler extracts `Path<Id>`, calls service, returns `Json<T>`
- **Service pattern**: Method signature follows `(&self, sbom_id: Id, tx: &Transactional<'_>)` pattern
- **Error handling**: Returns `Result<T, AppError>` with `.context()` wrapping
- **Model pattern**: New struct in its own file, registered via `pub mod` in parent `mod.rs`
- **Test pattern**: Integration tests in `tests/api/`, using real PostgreSQL, `assert_eq!` assertions

No convention conflicts detected between the task description and discovered conventions.

---

## Cross-Section Reference Consistency

Verified that all file paths are consistent across task sections:

- `AdvisoryService` -- referenced in both "Files to Modify" and "Implementation Notes" as
  `modules/fundamental/src/advisory/service/advisory.rs` -- CONSISTENT
- `SeveritySummary` -- "Files to Create" lists `model/severity_summary.rs`, "Implementation Notes"
  references `AdvisorySummary` in `model/summary.rs` as the source of the `severity` field -- these
  are different entities, no conflict
- Route registration -- "Files to Modify" lists `endpoints/mod.rs`, "Implementation Notes"
  references the same file -- CONSISTENT

---

## Data-Flow Trace

```
GET /api/v2/sbom/{id}/advisory-summary
  -> severity_summary.rs handler extracts Path<Id>
  -> calls AdvisoryService::severity_summary(sbom_id, tx)
  -> service queries sbom_advisory join table for advisories linked to SBOM
  -> service loads AdvisorySummary for each advisory (has severity field)
  -> service deduplicates by advisory ID
  -> service counts by severity level (Critical, High, Medium, Low)
  -> service returns SeveritySummary { critical, high, medium, low, total }
  -> handler wraps in Json and returns 200 OK
  -> on SBOM not found: returns 404 via AppError
```

**Data-flow status**: COMPLETE -- all stages connected from input to output.

---

## Implementation Order

1. Create `SeveritySummary` model struct (file 1)
2. Register model module in `model/mod.rs` (file 6)
3. Add `severity_summary` method to `AdvisoryService` (file 4)
4. Create endpoint handler (file 2)
5. Register route in `endpoints/mod.rs` (file 5)
6. Write integration tests (file 3)
7. Run `cargo test` and fix any failures
8. Verify acceptance criteria
9. Self-verification checks (scope, secrets, duplication, CI)

---

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary that returns aggregated
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. The endpoint deduplicates advisories by ID
and defaults all severity levels to 0 when no advisories exist.

Implements TC-9201
```

## Git Commands

```bash
git checkout -b TC-9201

# ... implement changes ...

git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      tests/api/advisory_summary.rs

git commit --trailer='Assisted-by: Claude Code' -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary that returns aggregated
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. The endpoint deduplicates advisories by ID
and defaults all severity levels to 0 when no advisories exist.

Implements TC-9201"

git push -u origin TC-9201
```

## Pull Request

**Title**: feat(advisory): add severity aggregation endpoint for SBOM advisories

**Description**:
```
## Summary

- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint returning severity counts (critical, high, medium, low, total)
- Add `SeveritySummary` response model and `severity_summary` service method to `AdvisoryService`
- Add integration tests covering valid SBOM, non-existent SBOM (404), empty advisories, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
```
