# Implementation Plan for TC-9201

## Task Summary

**Jira ID**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Status**: To Do
**Labels**: ai-generated-jira
**Linked Issues**: is incorporated by TC-9001

## Step 0 -- Validate Project Configuration

Verified that CLAUDE.md contains all required sections:
- **Repository Registry**: present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
- **Jira Configuration**: present, contains Project key (TC), Cloud ID, Feature issue type ID
- **Code Intelligence**: present, tool naming convention `mcp__<serena-instance>__<tool>` documented

All prerequisites satisfied. Proceeding.

## Step 1 -- Fetch and Parse Jira Task

Parsed structured description sections:

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM |
| Files to Modify | 3 files (see below) |
| Files to Create | 3 files (see below) |
| API Changes | `GET /api/v2/sbom/{id}/advisory-summary` -- NEW |
| Implementation Notes | Present -- references existing endpoint patterns, service patterns, entity join tables |
| Acceptance Criteria | 5 criteria |
| Test Requirements | 4 test cases |
| Target PR | Not present (default flow) |
| Bookend Type | Not present (default flow) |
| Dependencies | None |

**Target Branch extraction**: `main` -- stored for use in branch creation (Step 5) and PR base (Step 10).

**GitHub Issue extraction**: GitHub Issue custom field is `customfield_10747` per Jira Configuration. Would read this field from the fetched issue response. If a URL is present, parse `owner/repo#number` for use in the PR description.

**Issue webUrl**: Would capture from API response (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for clickable PR link.

### Files to Modify

1. `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method to AdvisoryService
2. `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
3. `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;` to register the new model module

### Files to Create

1. `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
2. `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler for /api/v2/sbom/{id}/advisory-summary
3. `tests/api/advisory_summary.rs` -- integration tests for the new endpoint

### Cross-Section Reference Consistency Check

- Entity `AdvisoryService`: Files to Modify says `modules/fundamental/src/advisory/service/advisory.rs`, Implementation Notes also reference `modules/fundamental/src/advisory/service/advisory.rs` -- CONSISTENT
- Entity `AdvisorySummary`: Implementation Notes reference `modules/fundamental/src/advisory/model/summary.rs` for the existing severity field -- this is a separate entity from our new `SeveritySummary`, no conflict
- Entity route registration: Files to Modify says `modules/fundamental/src/advisory/endpoints/mod.rs`, Implementation Notes say the same -- CONSISTENT

## Step 1.5 -- Verify Description Integrity

Would fetch all comments on TC-9201 via `jira.get_issue_comments("TC-9201")`.

1. Search for comments starting with `[sdlc-workflow] Description digest:`.
2. If multiple digest comments exist, select the most recent by `created` timestamp.
3. If no digest comment found: log warning "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced." and proceed.
4. If found:
   - Check if `updated` > `created` (comment was edited after posting) -- warn if so.
   - Extract the tagged digest value (e.g., `sha256-md:a1b2...`).
   - Compute current digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`.
   - Compare format tags; if mismatch, log warning and proceed.
   - Compare hex digests; if mismatch, alert user and ask whether to proceed or stop.
   - If match, proceed silently.

## Step 2 -- Verify Dependencies

Task has no dependencies. Proceeding.

## Step 3 -- Transition to In Progress and Assign

Would execute:
1. `jira.user_info()` -- get current user's account ID
2. `jira.edit_issue("TC-9201", assignee=<account-id>)` -- assign task
3. `jira.transition_issue("TC-9201")` -- transition to In Progress

## Step 4 -- Understand the Code

### Code Inspection Plan

Using Serena instance `serena_backend` (from Repository Registry):

1. **Overview of files to modify:**
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/service/advisory.rs` -- understand AdvisoryService structure, see `fetch` and `list` method signatures
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand route registration pattern
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/mod.rs` -- understand module registration pattern

2. **Read specific symbols:**
   - `mcp__serena_backend__find_symbol("fetch")` with `include_body=true` in `advisory.rs` to see full method pattern
   - `mcp__serena_backend__find_symbol("list")` with `include_body=true` in `advisory.rs` to see query pattern

3. **Check backward compatibility:**
   - `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to ensure adding a method won't break anything

4. **Pattern references:**
   - Read `modules/fundamental/src/advisory/endpoints/get.rs` to understand endpoint handler pattern (Path extraction, service call, JSON return)
   - Read `modules/fundamental/src/advisory/model/summary.rs` to see `AdvisorySummary` struct and its `severity` field
   - Read `entity/src/sbom_advisory.rs` to understand the join table structure
   - Read `common/src/error.rs` to understand `AppError` pattern

5. **CONVENTIONS.md lookup:**
   - Check for `./CONVENTIONS.md` at the repository root (per repo-backend.md, it exists)
   - Read it for naming rules, directory structure, code patterns, test conventions
   - Extract any CI check commands for use in Step 9

6. **Documentation file identification:**
   - `docs/api.md` -- may need updating with new endpoint
   - `docs/architecture.md` -- likely no changes needed
   - `README.md` -- likely no changes needed

### Convention Conformance Analysis (Sibling Analysis)

**Siblings inspected for production code:**

For `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (file to create):
- Sibling: `modules/fundamental/src/advisory/endpoints/get.rs`
- Sibling: `modules/fundamental/src/advisory/endpoints/list.rs`
- Sibling: `modules/fundamental/src/sbom/endpoints/get.rs`

For `modules/fundamental/src/advisory/model/severity_summary.rs` (file to create):
- Sibling: `modules/fundamental/src/advisory/model/summary.rs`
- Sibling: `modules/fundamental/src/advisory/model/details.rs`
- Sibling: `modules/fundamental/src/sbom/model/summary.rs`

For `modules/fundamental/src/advisory/service/advisory.rs` (file to modify):
- Already inspected for `fetch` and `list` methods

**Siblings inspected for test code:**

For `tests/api/advisory_summary.rs` (file to create):
- Sibling: `tests/api/advisory.rs`
- Sibling: `tests/api/sbom.rs`
- Sibling: `tests/api/search.rs`

See `outputs/conventions.md` for the full list of discovered conventions.

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type). Target Branch is `main`.

```
git checkout main
git pull
git checkout -b TC-9201
```

Branch name: `TC-9201` (matches Jira issue ID).

## Step 6 -- Implement Changes

See individual file descriptions in `outputs/file-N-description.md` for detailed changes.

### Files to Create

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** (file-1-description.md)
   - `SeveritySummary` response struct with `critical`, `high`, `medium`, `low`, `total` fields
   - Derives: `Serialize`, `Deserialize`, `Default`, `Debug`, `Clone`
   - Doc comment on the struct

2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** (file-2-description.md)
   - GET handler function following `get.rs` pattern
   - Extracts `Path<Id>` for SBOM ID
   - Calls `AdvisoryService::severity_summary()`
   - Returns `Json<SeveritySummary>`
   - Error handling with `AppError` and `.context()`

3. **`tests/api/advisory_summary.rs`** (file-3-description.md)
   - Integration tests for the new endpoint
   - 4 test cases per Test Requirements

### Files to Modify

4. **`modules/fundamental/src/advisory/service/advisory.rs`** (file-4-description.md)
   - Add `severity_summary` method to `AdvisoryService`
   - Queries `sbom_advisory` join table, joins to advisory to get severity
   - Groups by severity level, counts unique advisory IDs
   - Returns `SeveritySummary`

5. **`modules/fundamental/src/advisory/endpoints/mod.rs`** (file-5-description.md)
   - Add `mod severity_summary;` declaration
   - Register new route: `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::handler))`

6. **`modules/fundamental/src/advisory/model/mod.rs`** (file-6-description.md)
   - Add `pub mod severity_summary;` to register the new model module

### No Changes Needed

- `server/src/main.rs` -- confirmed no changes needed (routes auto-mount via module registration per task description)

### Documentation Impact

- `docs/api.md` -- would check if it lists endpoints; if so, add entry for `GET /api/v2/sbom/{id}/advisory-summary` with request/response documentation

## Step 7 -- Write Tests

Tests written in `tests/api/advisory_summary.rs` (see file-3-description.md). Would run:

```
cargo test
```

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET endpoint returns severity counts | Implemented in handler, verified by test |
| Returns 404 for non-existent SBOM | Error handling in service returns AppError, verified by test |
| Counts only unique advisories | Service uses DISTINCT on advisory ID, verified by test |
| Severity levels default to 0 | SeveritySummary uses Default derive, verified by test |
| Response time under 200ms for 500 advisories | Single query with GROUP BY, no N+1; would verify with test timing |

## Step 9 -- Self-Verification

### Scope Containment
Would run `git diff --name-only` and compare against Files to Modify and Files to Create. Expected files:
- `modules/fundamental/src/advisory/model/severity_summary.rs` (create)
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (create)
- `tests/api/advisory_summary.rs` (create)
- `modules/fundamental/src/advisory/service/advisory.rs` (modify)
- `modules/fundamental/src/advisory/endpoints/mod.rs` (modify)
- `modules/fundamental/src/advisory/model/mod.rs` (modify)
- Possibly `docs/api.md` (documentation update -- would flag as out-of-scope and ask user to approve)

### Untracked File Check
Would run `git status --short` and look for `??` entries in directories where implementation work occurred. Flag any referenced untracked files.

### Sensitive-Pattern Check
Would run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` to ensure no secrets are staged.

### CI Checks from CONVENTIONS.md
Would run any CI check commands extracted from CONVENTIONS.md.

### Data-Flow Trace
- `GET /api/v2/sbom/{id}/advisory-summary` -> extract Path<Id> -> call AdvisoryService::severity_summary() -> query sbom_advisory join table -> aggregate by severity -> return SeveritySummary as JSON -- **COMPLETE**

### Contract & Sibling Parity
- SeveritySummary struct: standalone, no trait/interface to implement
- Sibling parity with `get.rs` handler: same error handling pattern, same Path extraction, same Json return -- CONSISTENT
- Sibling parity with `fetch`/`list` service methods: same signature pattern (`&self, id, tx`), same error wrapping -- CONSISTENT

## Step 10 -- Commit and Push

### Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add SeveritySummary model, AdvisoryService::severity_summary() method,
and GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated severity counts (critical, high, medium, low, total) for
advisories linked to a given SBOM.

Implements TC-9201
```

With trailer: `--trailer='Assisted-by: Claude Code'`

### Full Commit Command

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      tests/api/advisory_summary.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      modules/fundamental/src/advisory/model/mod.rs
git commit --trailer='Assisted-by: Claude Code' -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add SeveritySummary model, AdvisoryService::severity_summary() method,
and GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated severity counts (critical, high, medium, low, total) for
advisories linked to a given SBOM.

Implements TC-9201"
```

### Push and Create PR

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" --body "## Summary

Add a service method and REST endpoint that aggregates vulnerability advisory severity
counts for a given SBOM. The endpoint returns a summary with counts per severity level
(Critical, High, Medium, Low) and a total.

- Add \`SeveritySummary\` response struct in \`advisory/model/severity_summary.rs\`
- Add \`severity_summary()\` method to \`AdvisoryService\`
- Add \`GET /api/v2/sbom/{id}/advisory-summary\` endpoint
- Add integration tests for the new endpoint

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
"
```

If a GitHub issue reference was found in `customfield_10747`, would append `Closes <owner>/<repo>#<number>` to the PR body.

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field** (`customfield_10875`) on TC-9201 with PR URL in ADF format (inlineCard)
2. **Add comment** to TC-9201 with:
   - PR link
   - Summary: Added SeveritySummary model, severity_summary service method, GET endpoint, and integration tests
   - No deviations from plan
   - Comment ends with sdlc-workflow footer
3. **Transition** TC-9201 to In Review
