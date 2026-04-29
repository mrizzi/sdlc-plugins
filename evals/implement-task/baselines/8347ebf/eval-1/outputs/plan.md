# Implementation Plan for TC-9201

## Task Summary

Add an advisory severity aggregation service method and REST endpoint that returns severity counts (Critical, High, Medium, Low, total) for a given SBOM. This enables dashboard widgets to render severity breakdowns without client-side counting.

## Project Configuration Validation

- Repository Registry: present (trustify-backend with serena_backend instance)
- Jira Configuration: present (Project key TC, Cloud ID, Feature issue type ID, custom fields)
- Code Intelligence: present (serena_backend with rust-analyzer)

All required sections are present. Proceeding.

## Task Description Validation

All required sections are present in the task description:
- Repository: trustify-backend
- Description: present
- Files to Modify: 3 files listed
- Files to Create: 3 files listed
- API Changes: 1 new endpoint
- Implementation Notes: present with pattern references
- Acceptance Criteria: 5 criteria
- Test Requirements: 4 tests
- Dependencies: None

No Target PR section -- this is a new implementation (default flow).
No GitHub Issue custom field value to extract.

## Cross-section Reference Consistency Check

Checking entities referenced across multiple sections:

- **AdvisoryService**: 
  - Files to Modify: `modules/fundamental/src/advisory/service/advisory.rs`
  - Implementation Notes: `modules/fundamental/src/advisory/service/advisory.rs`
  - Consistent.

- **Endpoint route registration (mod.rs)**:
  - Files to Modify: `modules/fundamental/src/advisory/endpoints/mod.rs`
  - Implementation Notes: `modules/fundamental/src/advisory/endpoints/mod.rs`
  - Consistent.

- **Model module registration**:
  - Files to Modify: `modules/fundamental/src/advisory/model/mod.rs`
  - Implementation Notes: references `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` (different file, different entity)
  - No conflict -- `model/mod.rs` is for module registration, `model/summary.rs` is an existing sibling being referenced for its `severity` field.

- **Endpoint handler pattern**:
  - Files to Create: `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
  - Implementation Notes: references `modules/fundamental/src/advisory/endpoints/get.rs` as the pattern to follow
  - Consistent -- different files, same directory, get.rs is the sibling pattern reference.

- **sbom_advisory join table**:
  - Implementation Notes: `entity/src/sbom_advisory.rs`
  - Repository structure confirms this file exists.
  - Consistent.

All cross-section references are consistent.

## Code Inspection Plan (Step 4)

Using the serena_backend Serena instance, I would inspect the following:

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- `get_symbols_overview` to see `AdvisoryService` structure and existing methods (`fetch`, `list`, `search`). Then `find_symbol` with `include_body=true` on `fetch` or `list` to understand the method signature pattern (parameters, return type, error handling).

2. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- `get_symbols_overview` to see the handler function structure. Then `find_symbol` to read the handler body and understand path param extraction, service invocation, and response return pattern.

3. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- `get_symbols_overview` to see current route registrations and understand where to add the new route.

4. **`modules/fundamental/src/advisory/model/mod.rs`** -- read to see existing `pub mod` declarations and add `pub mod severity_summary;`.

5. **`modules/fundamental/src/advisory/model/summary.rs`** -- `find_symbol` on `AdvisorySummary` to see the struct definition and confirm the `severity` field exists and understand its type.

6. **`entity/src/sbom_advisory.rs`** -- `get_symbols_overview` to understand the join table schema for linking SBOMs to advisories.

7. **Sibling analysis**:
   - `modules/fundamental/src/sbom/endpoints/get.rs` -- sibling endpoint handler for comparison
   - `modules/fundamental/src/sbom/service/sbom.rs` -- sibling service for comparison
   - `modules/fundamental/src/sbom/model/summary.rs` -- sibling model struct for comparison

8. **Test sibling analysis**:
   - `tests/api/advisory.rs` -- existing advisory integration tests
   - `tests/api/sbom.rs` -- existing SBOM integration tests

9. **Backward compatibility check**: `find_referencing_symbols` on `AdvisoryService` to ensure adding a new method won't break existing callers.

10. **Documentation files**: Check for `CONVENTIONS.md` at repo root, `docs/api.md` for API documentation, `README.md` at repo root.

## Dependencies Check (Step 2)

Dependencies: None. No blocking dependencies to verify.

## Files Overview

### Files to Modify

| # | File | Change Description |
|---|------|--------------------|
| 1 | `modules/fundamental/src/advisory/service/advisory.rs` | Add `severity_summary` method to `AdvisoryService` |
| 2 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Register the new `/api/v2/sbom/{id}/advisory-summary` route |
| 3 | `modules/fundamental/src/advisory/model/mod.rs` | Add `pub mod severity_summary;` to register the new model module |

### Files to Create

| # | File | Description |
|---|------|--------------------|
| 4 | `modules/fundamental/src/advisory/model/severity_summary.rs` | `SeveritySummary` response struct |
| 5 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | GET handler for `/api/v2/sbom/{id}/advisory-summary` |
| 6 | `tests/api/advisory_summary.rs` | Integration tests for the new endpoint |

### Files NOT modified

- `server/src/main.rs` -- no changes needed (routes auto-mount via module registration, confirmed by task description)

## API Changes

- `GET /api/v2/sbom/{id}/advisory-summary` -- NEW endpoint
  - Returns: `{ critical: N, high: N, medium: N, low: N, total: N }`
  - 404 when SBOM ID does not exist
  - Deduplicates advisories by advisory ID
  - All severity levels default to 0

## Data-flow Trace

- **Input**: HTTP GET request with SBOM ID as path parameter
- **Processing**: 
  1. Extract SBOM ID from path via `Path<Id>` extractor
  2. Call `AdvisoryService::severity_summary(sbom_id, tx)` 
  3. Service queries `sbom_advisory` join table to find advisories linked to the SBOM
  4. Service fetches `AdvisorySummary` for each advisory to get severity field
  5. Service deduplicates by advisory ID
  6. Service counts severities into Critical/High/Medium/Low buckets
  7. Service constructs and returns `SeveritySummary` struct
- **Output**: JSON response with `{ critical, high, medium, low, total }` or 404 error

Data flow is **COMPLETE** -- request enters via endpoint, is processed by service with database query, and result is returned as JSON response.

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to an SBOM. Includes SeveritySummary model, AdvisoryService
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

- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint returning advisory severity counts per SBOM
- Implement `SeveritySummary` response model and `AdvisoryService::severity_summary` method
- Add integration tests covering valid SBOM, non-existent SBOM (404), empty advisories, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
```
