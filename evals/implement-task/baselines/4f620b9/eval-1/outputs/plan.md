# Implementation Plan for TC-9201

## Task Summary

Add an advisory severity aggregation service method and REST endpoint that returns severity counts (Critical, High, Medium, Low, total) for a given SBOM. The endpoint is `GET /api/v2/sbom/{id}/advisory-summary`.

## Step-by-step Skill Execution

### Step 0 -- Validate Project Configuration

The mock CLAUDE.md contains all required sections:
- Repository Registry: present with `trustify-backend` entry
- Jira Configuration: present with Project key (TC), Cloud ID, Feature issue type ID
- Code Intelligence: present with `serena_backend` instance and tool naming convention

Validation passes. Proceed.

### Step 1 -- Fetch and Parse Jira Task

Parsed sections from TC-9201:
- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add service method + REST endpoint for advisory severity aggregation per SBOM
- **Files to Modify**: 3 files (advisory service, endpoints mod, model mod)
- **Files to Create**: 3 files (severity summary model, severity summary endpoint, integration tests)
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` (NEW)
- **Implementation Notes**: follow existing endpoint/service patterns, use sbom_advisory join table, AdvisorySummary.severity field for counting
- **Acceptance Criteria**: 5 criteria
- **Test Requirements**: 4 test cases
- **Target PR**: not present (default flow)
- **Bookend Type**: not present (default flow)
- **Dependencies**: None
- **webUrl**: would be captured from Jira API response (e.g., `https://redhat.atlassian.net/browse/TC-9201`)
- **GitHub Issue custom field**: `customfield_10747` -- would check for value

All required sections present. No gaps detected. Proceed.

### Step 1.5 -- Verify Description Integrity

Would fetch comments from TC-9201 and look for `[sdlc-workflow] Description digest:` marker. Compare digest if found. (Simulated -- skip in eval.)

### Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

### Step 3 -- Transition to In Progress and Assign

Would:
1. Call `jira.user_info()` to get current user account ID
2. Call `jira.edit_issue(TC-9201, assignee=<account-id>)` to assign
3. Call `jira.transition_issue(TC-9201, "In Progress")` to update status

### Step 4 -- Understand the Code

Would use `mcp__serena_backend__get_symbols_overview` on:
- `modules/fundamental/src/advisory/service/advisory.rs` -- understand existing `fetch`, `list` methods
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand route registration pattern
- `modules/fundamental/src/advisory/endpoints/get.rs` -- sibling endpoint handler pattern
- `modules/fundamental/src/advisory/endpoints/list.rs` -- sibling endpoint handler pattern
- `modules/fundamental/src/advisory/model/mod.rs` -- understand model module registration
- `modules/fundamental/src/advisory/model/summary.rs` -- understand `AdvisorySummary` struct and its `severity` field
- `entity/src/sbom_advisory.rs` -- understand the join table structure
- `common/src/error.rs` -- understand `AppError` pattern

Sibling analysis:
- `modules/fundamental/src/sbom/endpoints/get.rs` and `list.rs` -- sibling endpoint patterns
- `modules/fundamental/src/sbom/model/summary.rs` -- sibling model struct
- `tests/api/sbom.rs` and `tests/api/advisory.rs` -- sibling test files

Documentation files identified:
- `docs/api.md` -- API reference (may need updating with new endpoint)
- `CONVENTIONS.md` -- repository root conventions
- `README.md` -- project readme

CONVENTIONS.md: would read and extract CI check commands and code generation commands.

Convention conformance analysis results documented in `outputs/conventions.md`.

### Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):
```
git checkout main
git pull
git checkout -b TC-9201
```

### Step 6 -- Implement Changes

See file descriptions below (outputs/file-1 through file-6).

### Step 7 -- Write Tests

See file-7-description.md for test implementation details.

Would run `cargo test` after writing tests and fix any failures.

### Step 8 -- Verify Acceptance Criteria

1. GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }` -- satisfied by the endpoint returning `SeveritySummary` struct serialized as JSON
2. Returns 404 when SBOM ID does not exist -- satisfied by checking SBOM existence first and returning `AppError` not-found
3. Counts only unique advisories (deduplicates by advisory ID) -- satisfied by collecting into a HashSet or using DISTINCT in the query
4. All severity levels default to 0 when no advisories exist -- satisfied by initializing all counts to 0 in `SeveritySummary::default()`
5. Response time under 200ms for SBOMs with up to 500 advisories -- satisfied by a single database query with JOIN and GROUP BY

### Step 9 -- Self-Verification

Would perform:
- **Scope containment**: `git diff --name-only` and verify all files are in the Files to Modify / Files to Create lists
- **Untracked file check**: `git status --short` for `??` entries in modified directories
- **Sensitive-pattern check**: `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'`
- **Documentation currency**: check if `docs/api.md` needs updating with the new endpoint
- **Duplication check**: search for existing severity aggregation logic
- **CI checks from CONVENTIONS.md**: run extracted CI commands
- **Data-flow trace**:
  - `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param `id` -> call `AdvisoryService::severity_summary(sbom_id, tx)` -> query sbom_advisory join table -> count by severity -> return `SeveritySummary` as JSON -- **COMPLETE**
- **Contract & sibling parity**: verify SeveritySummary endpoint follows same patterns as sibling get.rs handler
- **Cross-section reference consistency**: verify file paths in Files to Modify vs Implementation Notes are consistent

**Cross-section reference consistency results:**
- Entity `AdvisoryService` -- Files to Modify: `modules/fundamental/src/advisory/service/advisory.rs`, Implementation Notes: `modules/fundamental/src/advisory/service/advisory.rs` -- consistent
- Entity `AdvisorySummary` -- Implementation Notes: `modules/fundamental/src/advisory/model/summary.rs` -- consistent (referenced for reading, not in Files to Modify)
- All other entities -- consistent

### Step 10 -- Commit and Push

**Commit message:**
```
feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to a given SBOM.

Includes SeveritySummary response model, AdvisoryService::severity_summary
method, endpoint handler, route registration, and integration tests.

Implements TC-9201
```

With `--trailer="Assisted-by: Claude Code"`.

Then:
```
git push -u origin TC-9201
gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "..."
```

PR description would include:
- Summary of changes
- `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)`
- GitHub issue `Closes` line if GitHub Issue custom field was populated

### Step 11 -- Update Jira

Would:
1. Update `customfield_10875` (Git Pull Request custom field) with PR URL in ADF format
2. Add comment to TC-9201 with PR link, summary of changes, no deviations from plan
3. Transition TC-9201 to "In Review"

---

## Files Overview

| # | File | Action | Description |
|---|------|--------|-------------|
| 1 | `modules/fundamental/src/advisory/model/severity_summary.rs` | CREATE | SeveritySummary response struct |
| 2 | `modules/fundamental/src/advisory/model/mod.rs` | MODIFY | Register new severity_summary module |
| 3 | `modules/fundamental/src/advisory/service/advisory.rs` | MODIFY | Add severity_summary method to AdvisoryService |
| 4 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | CREATE | GET handler for advisory-summary endpoint |
| 5 | `modules/fundamental/src/advisory/endpoints/mod.rs` | MODIFY | Register the new route |
| 6 | `docs/api.md` | MODIFY | Add new endpoint to API documentation (if exists and covers advisory endpoints) |
| 7 | `tests/api/advisory_summary.rs` | CREATE | Integration tests for the new endpoint |
