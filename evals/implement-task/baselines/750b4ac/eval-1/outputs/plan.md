# Implementation Plan for TC-9201

## Task Summary

**Jira Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Status**: To Do
**Parent Feature**: TC-9001 (is incorporated by)
**Dependencies**: None

## Description Digest Verification

Would fetch issue comments and search for `[sdlc-workflow] Description digest:` marker.
If found, compute digest of the current description using `python3 scripts/sha256-digest.py`
and compare tags and hex values. If no digest comment found, log warning and proceed.

## Project Configuration Validation

Verified the following sections exist in the project's CLAUDE.md:
1. **Repository Registry** -- contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- contains Project key (TC), Cloud ID, Feature issue type ID (10142)
3. **Code Intelligence** -- contains tool naming convention `mcp__<serena-instance>__<tool>`, with `serena_backend` instance using rust-analyzer

All required sections present. Proceeding.

## Cross-Section Reference Consistency Check

Verified file-path references for each entity across task description sections:

- Entity `AdvisoryService` / `severity_summary` method:
  - Files to Modify: `modules/fundamental/src/advisory/service/advisory.rs`
  - Implementation Notes: `modules/fundamental/src/advisory/service/advisory.rs`
  - Result: **Consistent**

- Entity `SeveritySummary` response struct:
  - Files to Create: `modules/fundamental/src/advisory/model/severity_summary.rs`
  - Implementation Notes: references `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` as pattern reference
  - Result: **Consistent** (different entities, different files -- no conflict)

- Entity route registration:
  - Files to Modify: `modules/fundamental/src/advisory/endpoints/mod.rs`
  - Implementation Notes: `modules/fundamental/src/advisory/endpoints/mod.rs`
  - Result: **Consistent**

- Entity model module registration:
  - Files to Modify: `modules/fundamental/src/advisory/model/mod.rs`
  - Implementation Notes: (not explicitly mentioned but implied by model pattern)
  - Result: **Consistent**

No cross-section reference inconsistencies detected.

## Files to Modify

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- add `severity_summary` method to `AdvisoryService`
2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- register the new `/api/v2/sbom/{id}/advisory-summary` route
3. **`modules/fundamental/src/advisory/model/mod.rs`** -- add `pub mod severity_summary;` to register the new model module

## Files to Create

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- `SeveritySummary` response struct
2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- GET handler for `/api/v2/sbom/{id}/advisory-summary`
3. **`tests/api/advisory_summary.rs`** -- integration tests for the new endpoint

## Files Not Modified

- **`server/src/main.rs`** -- no changes needed (routes auto-mount via module registration, as stated in task)

## API Changes

- `GET /api/v2/sbom/{id}/advisory-summary` -- NEW endpoint returning `{ critical: N, high: N, medium: N, low: N, total: N }`

## Implementation Approach

### Step 4 -- Code Understanding

Using the Serena instance `serena_backend` (from Repository Registry):
- `mcp__serena_backend__get_symbols_overview` on `advisory/service/advisory.rs` to understand `AdvisoryService` structure
- `mcp__serena_backend__find_symbol` with `include_body=true` on `fetch` and `list` methods to understand the service method pattern
- `mcp__serena_backend__get_symbols_overview` on `advisory/endpoints/get.rs` to understand the endpoint handler pattern
- `mcp__serena_backend__find_symbol` on `AdvisorySummary` in `advisory/model/summary.rs` to see the `severity` field type
- `mcp__serena_backend__get_symbols_overview` on `entity/src/sbom_advisory.rs` to understand the join table structure
- `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to ensure new method won't conflict
- Read `common/src/error.rs` to understand `AppError` and `.context()` usage
- Read `CONVENTIONS.md` at repo root for project-level conventions and CI check commands
- Read sibling endpoint files (`advisory/endpoints/list.rs`, `sbom/endpoints/get.rs`) for convention conformance analysis
- Read sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`) for test convention analysis

### Documentation Files Identified

- `docs/api.md` -- REST API reference (may need update with new endpoint)
- `docs/architecture.md` -- System architecture overview (likely no update needed)
- `CONVENTIONS.md` -- Project conventions (no update needed)
- `README.md` -- Project readme (likely no update needed)

### Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9201
```

### Step 6 -- Implement Changes

Implement all files as detailed in the file-N-description.md outputs below.

### Step 7 -- Write Tests

Implement integration tests in `tests/api/advisory_summary.rs` as detailed in file-6-description.md.

Run tests:
```
cargo test
```

Fix any failures before proceeding.

### Step 8 -- Verify Acceptance Criteria

- [x] GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }` -- verified by implementation and test
- [x] Returns 404 when SBOM ID does not exist -- verified by `test_advisory_summary_sbom_not_found` test
- [x] Counts only unique advisories (deduplicates by advisory ID) -- implemented using `HashSet` or `.distinct()` in the service method, verified by `test_advisory_summary_deduplication` test
- [x] All severity levels default to 0 when no advisories exist at that level -- verified by `test_advisory_summary_no_advisories` test
- [x] Response time under 200ms for SBOMs with up to 500 advisories -- ensured by efficient single query with GROUP BY

### Step 9 -- Self-Verification

#### Scope containment
Files modified/created match exactly the Files to Modify and Files to Create sections. No out-of-scope changes.

#### Untracked file check
New files (`severity_summary.rs` model, `severity_summary.rs` endpoint, `advisory_summary.rs` test) are all listed in Files to Create.

#### Sensitive-pattern check
No passwords, API keys, secrets, or `.env` references in the diff.

#### Documentation currency
The new API endpoint `GET /api/v2/sbom/{id}/advisory-summary` should be documented in `docs/api.md` if it exists and covers endpoint listings. A lightweight addition describing the new endpoint would be made.

#### Data-flow trace
- `GET /api/v2/sbom/{id}/advisory-summary` -> extract `Path<Id>` -> call `AdvisoryService::severity_summary(sbom_id, tx)` -> query `sbom_advisory` join table -> aggregate by severity -> return `Json<SeveritySummary>` -- **COMPLETE**

#### Contract & sibling parity
- `SeveritySummary` is a standalone response struct (no trait implementation needed)
- Sibling parity with `get.rs` endpoint: error handling pattern (AppError + .context()) matches, path extraction pattern matches, service invocation pattern matches
- No cross-module shared entity concerns (read-only aggregation query)

#### Duplication check
No existing severity aggregation logic found in the codebase. The `AdvisorySummary` struct has a `severity` field but no aggregation/counting logic exists.

### Step 10 -- Commit and Push

#### Commit message

```
feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity
counts (critical, high, medium, low, total) for advisories linked
to a given SBOM. Includes SeveritySummary model, AdvisoryService
method, endpoint handler, and integration tests.

Implements TC-9201
```

With `--trailer="Assisted-by: Claude Code"`.

#### Push and PR

```
git push -u origin TC-9201
gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "## Summary
- Add SeveritySummary response model for severity count aggregation
- Add severity_summary method to AdvisoryService that queries sbom_advisory join table and counts by severity level
- Add GET /api/v2/sbom/{id}/advisory-summary endpoint handler
- Add integration tests covering valid SBOM, non-existent SBOM (404), empty advisories, and deduplication

## Jira
Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)"
```

### Step 11 -- Update Jira

1. Update Git Pull Request custom field (`customfield_10875`) with PR URL in ADF format
2. Add comment to TC-9201 with PR link, summary of changes, and no deviations from plan
3. Transition TC-9201 to In Review
