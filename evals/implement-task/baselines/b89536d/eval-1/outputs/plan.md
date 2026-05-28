# Implementation Plan for TC-9201

## Task Summary

Add an advisory severity aggregation service method and REST endpoint that returns
severity counts (Critical, High, Medium, Low, total) for a given SBOM, enabling
dashboard widgets to render severity breakdowns without client-side counting.

## Step 0 -- Validate Project Configuration

The mock CLAUDE.md contains all required sections:
- Repository Registry: present, lists `trustify-backend` with Serena instance `serena_backend`
- Jira Configuration: present with Project key (TC), Cloud ID, Feature issue type ID
- Code Intelligence: present with tool naming convention and `serena_backend` instance

Validation passes. Proceed.

## Step 1 -- Fetch and Parse Jira Task

Parsed sections from TC-9201:
- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add severity aggregation service + endpoint
- **Files to Modify**: 3 files (advisory service, endpoints mod, model mod)
- **Files to Create**: 3 files (severity summary model, endpoint handler, integration tests)
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` (NEW)
- **Implementation Notes**: Follow existing endpoint/service patterns
- **Acceptance Criteria**: 5 criteria
- **Test Requirements**: 4 tests
- **Dependencies**: None
- **Target PR**: None (default flow)
- **Bookend Type**: None (default flow)
- **GitHub Issue**: Would check `customfield_10747` on the Jira issue (skipped in eval)

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

## Step 3 -- Transition to In Progress and Assign

Would execute (skipped in eval):
1. `jira.user_info()` to get current user account ID
2. `jira.edit_issue(TC-9201, assignee=<account-id>)`
3. `jira.transition_issue(TC-9201)` to In Progress

## Step 4 -- Understand the Code

### Code inspection plan

Would use `mcp__serena_backend__get_symbols_overview` on:
- `modules/fundamental/src/advisory/service/advisory.rs` -- understand AdvisoryService methods
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand route registration
- `modules/fundamental/src/advisory/endpoints/get.rs` -- reference pattern for new endpoint
- `modules/fundamental/src/advisory/model/mod.rs` -- understand module registration
- `modules/fundamental/src/advisory/model/summary.rs` -- understand AdvisorySummary struct (severity field)
- `entity/src/sbom_advisory.rs` -- understand join table for SBOM-Advisory relationship
- `common/src/error.rs` -- understand AppError pattern

Would use `mcp__serena_backend__find_symbol` with `include_body=true` on:
- `AdvisoryService::fetch` -- reference for new `severity_summary` method signature
- `AdvisoryService::list` -- reference for query patterns
- `AdvisorySummary` struct -- understand the `severity` field type and values

Would use `mcp__serena_backend__find_referencing_symbols` on:
- `AdvisoryService` -- ensure new method does not conflict with existing callers

### Convention conformance analysis

Siblings analyzed (see outputs/conventions.md for full details):
- Endpoint siblings: `get.rs`, `list.rs` in `advisory/endpoints/`
- Service siblings: `sbom.rs` in `sbom/service/`
- Model siblings: `summary.rs`, `details.rs` in `advisory/model/`
- Test siblings: `sbom.rs`, `advisory.rs` in `tests/api/`

### CONVENTIONS.md lookup

Would read `CONVENTIONS.md` at repository root. Extract CI check commands if present.

### Documentation files identified

- `README.md` at repository root
- `docs/api.md` -- REST API reference (may need new endpoint documented)
- `docs/architecture.md` -- system architecture overview

### Cross-section reference consistency check

Verified file paths across task sections:
- `AdvisoryService` -- referenced in Files to Modify as `modules/fundamental/src/advisory/service/advisory.rs`
  and in Implementation Notes as the same path. Consistent.
- `AdvisorySummary` -- referenced in Implementation Notes at `modules/fundamental/src/advisory/model/summary.rs`.
  This is a read-only reference (not modified). Consistent.
- Route registration -- `modules/fundamental/src/advisory/endpoints/mod.rs` in both Files to Modify
  and Implementation Notes. Consistent.

## Step 5 -- Create Branch

Would execute (default flow, no Target PR, no Bookend Type):
```
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### Files to Create

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** (NEW)
   - Define `SeveritySummary` response struct with fields: `critical`, `high`, `medium`, `low`, `total` (all `u64` or `usize`)
   - Derive `Serialize`, `Deserialize`, `Debug`, `Clone`
   - Add doc comment explaining the struct's purpose
   - See: outputs/file-1-description.md

2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** (NEW)
   - GET handler function `get_advisory_summary` for `/api/v2/sbom/{id}/advisory-summary`
   - Extract `Path<Id>` for the SBOM ID
   - Call `AdvisoryService::severity_summary` method
   - Return `Json<SeveritySummary>` or `AppError`
   - See: outputs/file-2-description.md

3. **`tests/api/advisory_summary.rs`** (NEW)
   - Integration tests for the new endpoint
   - Four test functions matching Test Requirements
   - See: outputs/file-3-description.md

### Files to Modify

4. **`modules/fundamental/src/advisory/service/advisory.rs`** (MODIFY)
   - Add `severity_summary` method to `AdvisoryService`
   - Query `sbom_advisory` join table, load advisories, count by severity
   - Deduplicate by advisory ID
   - Return `SeveritySummary` struct
   - See: outputs/file-4-description.md

5. **`modules/fundamental/src/advisory/endpoints/mod.rs`** (MODIFY)
   - Add `mod severity_summary;` declaration
   - Register new route: `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_advisory_summary))`
   - See: outputs/file-5-description.md

6. **`modules/fundamental/src/advisory/model/mod.rs`** (MODIFY)
   - Add `pub mod severity_summary;` to register the new model module
   - See: outputs/file-6-description.md

### Files NOT modified

- `server/src/main.rs` -- no changes needed (routes auto-mount via module registration, confirmed by task description)

## Step 7 -- Write Tests

See outputs/file-3-description.md for detailed test implementation.

Four tests matching Test Requirements:
1. `test_advisory_summary_valid_sbom` -- valid SBOM with known advisories returns correct counts
2. `test_advisory_summary_not_found` -- non-existent SBOM ID returns 404
3. `test_advisory_summary_no_advisories` -- SBOM with no advisories returns all zeros
4. `test_advisory_summary_deduplication` -- duplicate advisory links are deduplicated

Would run: `cargo test` to verify all tests pass.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns correct shape | Endpoint returns `SeveritySummary` with all 5 fields |
| Returns 404 for non-existent SBOM | Service checks SBOM existence first, returns AppError |
| Counts only unique advisories | Deduplication by advisory ID using HashSet or DISTINCT |
| Severity levels default to 0 | `SeveritySummary::default()` initializes all to 0, then increments |
| Response time under 200ms for 500 advisories | Single JOIN query with GROUP BY, no N+1 |

## Step 9 -- Self-Verification

### Scope containment
All files match Files to Modify and Files to Create lists.

### Sensitive-pattern check
No passwords, API keys, secrets, or .env files in the changes.

### Documentation currency
`docs/api.md` should be checked for whether it documents REST endpoints. If it does,
the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint should be added.

### Data-flow trace
- Input: `GET /api/v2/sbom/{id}/advisory-summary` request with SBOM ID path param
- Processing: endpoint handler extracts ID -> calls `AdvisoryService::severity_summary` -> queries `sbom_advisory` join table -> loads advisory severity values -> counts by severity level -> deduplicates by advisory ID
- Output: `Json<SeveritySummary>` response with `{ critical, high, medium, low, total }`
- Path is COMPLETE: request -> service -> database -> response.

### Contract and sibling parity
- `SeveritySummary` is a standalone response struct, no trait to implement
- Sibling parity with `get.rs` handler: both use `Path<Id>`, both return `Result<Json<T>, AppError>`, both call service with `tx` parameter
- Sibling parity with `fetch`/`list` service methods: all accept `(&self, id, tx)`, all return `Result<T, AppError>`

### Duplication check
No existing severity aggregation logic found in the codebase. The new code is unique.

## Step 10 -- Commit and Push

### Commit message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Enables dashboard severity breakdown widgets
without client-side counting.

Implements TC-9201
```

With `--trailer="Assisted-by: Claude Code"`.

### PR creation

```
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "..."
```

PR description would include:
- Summary of changes
- Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
- Closes reference if GitHub Issue custom field was populated

## Step 11 -- Update Jira

Would execute (skipped in eval):
1. Update `customfield_10875` (Git Pull Request) with PR URL in ADF format
2. Add comment with PR link, summary of changes, and no deviations
3. Transition TC-9201 to In Review
