# Implementation Plan: TC-9201

## Task Summary

**Jira Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Dependencies**: None
**Bookend Type**: None
**Target PR**: None

## Step 1.5 -- Description Integrity

> No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced.

## Step 2 -- Dependency Verification

No dependencies declared. Proceeding.

## Step 3 -- Transition and Assign

- Retrieve current user's Jira account ID via `jira.user_info()`
- Assign TC-9201 to current user via `jira.edit_issue(TC-9201, assignee=<accountId>)`
- Transition TC-9201 to "In Progress" via `jira.transition_issue`

## Step 4 -- Code Understanding

### Sibling Analysis

Analyzed the following sibling files to understand patterns:

**Endpoints (siblings of new `severity_summary.rs`):**
- `modules/fundamental/src/advisory/endpoints/get.rs` -- GET handler pattern: `Path<Id>` extraction, service call, JSON return
- `modules/fundamental/src/advisory/endpoints/list.rs` -- list handler pattern with `PaginatedResults<T>`
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- route registration with `Router::new().route()`

**Models (siblings of new `severity_summary.rs`):**
- `modules/fundamental/src/advisory/model/summary.rs` -- `AdvisorySummary` struct with `severity` field
- `modules/fundamental/src/advisory/model/details.rs` -- `AdvisoryDetails` struct

**Service (file to modify: `advisory.rs`):**
- `modules/fundamental/src/advisory/service/advisory.rs` -- `AdvisoryService` with `fetch`, `list`, `search` methods following `(&self, id, tx: &Transactional<'_>)` signature

**Tests (siblings of new `advisory_summary.rs`):**
- `tests/api/advisory.rs` -- advisory endpoint integration tests
- `tests/api/sbom.rs` -- SBOM endpoint integration tests

**Entity (referenced in Implementation Notes):**
- `entity/src/sbom_advisory.rs` -- SBOM-Advisory join table for linking advisories to SBOMs

### CONVENTIONS.md Lookup

`CONVENTIONS.md` exists at repository root. Would read for CI check commands and project-specific conventions. Verification commands extracted for use in Step 9.

### Documentation Files Identified

- `docs/api.md` -- REST API reference (may need update for new endpoint)
- `docs/architecture.md` -- System architecture overview
- `README.md` -- Repository readme

### Cross-Section Reference Consistency

Verified all entity-to-file-path references across the task description sections:

- Entity `AdvisoryService` -- consistent: both Files to Modify and Implementation Notes reference `modules/fundamental/src/advisory/service/advisory.rs`
- Entity `SeveritySummary` -- consistent: Files to Create references `modules/fundamental/src/advisory/model/severity_summary.rs`
- Entity route registration -- consistent: Files to Modify and Implementation Notes both reference `modules/fundamental/src/advisory/endpoints/mod.rs`
- Entity `AdvisorySummary.severity` -- consistent: Implementation Notes correctly references `modules/fundamental/src/advisory/model/summary.rs`
- Entity `sbom_advisory` -- consistent: Implementation Notes correctly references `entity/src/sbom_advisory.rs`

No mismatches detected.

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9201
```

Branch named after the Jira issue ID, based on the target branch `main`.

## Step 6-7 -- Files to Create and Modify

### Files to Create

| # | File | Description |
|---|---|---|
| 1 | `modules/fundamental/src/advisory/model/severity_summary.rs` | SeveritySummary response struct |
| 2 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | GET handler for `/api/v2/sbom/{id}/advisory-summary` |
| 3 | `tests/api/advisory_summary.rs` | Integration tests for the new endpoint |

### Files to Modify

| # | File | Change |
|---|---|---|
| 4 | `modules/fundamental/src/advisory/model/mod.rs` | Add `pub mod severity_summary;` to register new model module |
| 5 | `modules/fundamental/src/advisory/service/advisory.rs` | Add `severity_summary` method to `AdvisoryService` |
| 6 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Register the new route for the severity summary endpoint |

### Files NOT Modified

- `server/src/main.rs` -- No changes needed (routes auto-mount via module registration)

## Step 8 -- Acceptance Criteria Verification

Each acceptance criterion would be verified:

1. GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }` -- verified by endpoint implementation and test
2. Returns 404 when SBOM ID does not exist -- verified by service method returning `AppError` and dedicated test
3. Counts only unique advisories (deduplicates by advisory ID) -- verified by using `DISTINCT` or `HashSet` in service method and dedicated test
4. All severity levels default to 0 when no advisories exist -- verified by struct defaults and dedicated test
5. Response time under 200ms for SBOMs with up to 500 advisories -- verified by efficient SQL query using join table

## Step 9 -- Self-Verification

### Scope Containment
`git diff --name-only` would list exactly the 6 files above. All are within the declared Files to Modify and Files to Create sections.

### Data-Flow Trace
- `GET /api/v2/sbom/{id}/advisory-summary` --> extract `Path<Id>` --> call `AdvisoryService::severity_summary(sbom_id, tx)` --> query `sbom_advisory` join table --> aggregate by severity from `AdvisorySummary.severity` --> construct `SeveritySummary` struct --> return `Json(summary)` -- **COMPLETE**

### Contract & Sibling Parity
- `SeveritySummary` does not implement a trait/interface (it is a standalone response struct with `Serialize`/`Deserialize`) -- no contract gap
- Sibling parity with `get.rs` endpoint: error handling via `Result<T, AppError>` with `.context()` -- matches
- Sibling parity with `fetch`/`list` service methods: signature pattern `(&self, id, tx)` -- matches

### Sensitive-Pattern Check
No passwords, API keys, private keys, or .env files in the diff.

### Documentation Currency
`docs/api.md` would need an entry added for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

### CI Checks
Run verification commands extracted from CONVENTIONS.md (e.g., `cargo fmt --check`, `cargo clippy`, `cargo build`, `cargo test`).

## Step 10 -- Commit and Push

### Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to an SBOM. Includes SeveritySummary model, AdvisoryService
method, endpoint handler, and integration tests.

Implements TC-9201
```

With trailer: `--trailer='Assisted-by: Claude Code'`

### Push and PR

```
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "## Summary
- Add SeveritySummary response model for severity count aggregation
- Add severity_summary method to AdvisoryService querying sbom_advisory join table
- Add GET /api/v2/sbom/{id}/advisory-summary endpoint handler
- Add integration tests for valid SBOM, non-existent SBOM, empty advisories, and deduplication

## Jira
Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)"
```

## Step 11 -- Update Jira

1. Set Git Pull Request custom field (`customfield_10875`) on TC-9201 with the PR URL in ADF format
2. Add comment to TC-9201 with:
   - PR link
   - Summary of changes: added SeveritySummary model, severity_summary service method, GET endpoint, and 4 integration tests
   - No deviations from plan
3. Transition TC-9201 to "In Review"
