# Implementation Plan for TC-9201

## Task Summary

**Jira Issue**: TC-9201 -- Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Branch Name**: TC-9201
**Dependencies**: None
**Linked Issues**: is incorporated by TC-9001

## Step 0 -- Validate Project Configuration

Verified CLAUDE.md contains all required sections:
- **Repository Registry**: present, lists `trustify-backend` with Serena Instance `serena_backend` at path `./`
- **Jira Configuration**: present, contains Project key (TC), Cloud ID, Feature issue type ID, Git Pull Request custom field (customfield_10875), GitHub Issue custom field (customfield_10747)
- **Code Intelligence**: present, documents tool naming convention `mcp__<serena-instance>__<tool>` and lists `serena_backend` instance with rust-analyzer

Configuration is valid. Proceeding.

## Step 0.5 -- JIRA Access Initialization

Would attempt MCP first for all JIRA operations. If MCP fails, prompt user for REST API fallback.

## Step 1 -- Fetch and Parse Jira Task

Parsed structured description from TC-9201:

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM |
| Files to Modify | 3 files (see below) |
| Files to Create | 3 files (see below) |
| API Changes | GET /api/v2/sbom/{id}/advisory-summary (NEW) |
| Target PR | not present |
| Review Context | not present |
| Bookend Type | not present |
| Dependencies | None |

### Target Branch Extraction

Target Branch is **main**. This will be used as the base for branch creation (Step 5) and as the `--base` argument for `gh pr create` (Step 10).

### GitHub Issue Extraction

GitHub Issue custom field (customfield_10747) is configured in CLAUDE.md. Would read the field value from the fetched issue. If empty, skip silently.

## Step 1.5 -- Verify Description Integrity

Would retrieve issue comments via `jira.get_issue_comments(TC-9201)` and search for comments starting with `[sdlc-workflow] Description digest:`.

**Result**: No description digest comment found. Logging warning and proceeding normally:

> "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced."

This is backward-compatible behavior -- execution is not blocked when no digest exists.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceeding.

## Step 3 -- Transition to In Progress and Assign

Would execute:
1. `jira.user_info()` -- retrieve current user's account ID
2. `jira.edit_issue(TC-9201, assignee=<account-id>)` -- assign task
3. `jira.transition_issue(TC-9201)` -- transition to In Progress

## Step 4 -- Understand the Code

### Code Inspection Plan

Using Serena instance `serena_backend` (from Repository Registry), inspect all files before modifying them:

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- use `mcp__serena_backend__get_symbols_overview` to see the AdvisoryService struct and its existing methods (`fetch`, `list`, `search`). Then use `mcp__serena_backend__find_symbol` with `include_body=true` on the `fetch` method to understand the pattern for the new `severity_summary` method (parameter types, return type, error handling, transaction usage).

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- use `mcp__serena_backend__get_symbols_overview` to see route registration pattern. Understand how `Router::new().route("/path", get(handler))` registrations are structured.

3. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- use `mcp__serena_backend__get_symbols_overview` then `find_symbol` on the handler function to understand the endpoint pattern: Path parameter extraction, service invocation, JSON response return, error handling with `AppError` and `.context()`.

4. **`modules/fundamental/src/advisory/model/mod.rs`** -- use `mcp__serena_backend__get_symbols_overview` to see how model submodules are registered (`pub mod summary;`, `pub mod details;`).

5. **`modules/fundamental/src/advisory/model/summary.rs`** -- use `mcp__serena_backend__find_symbol` on `AdvisorySummary` to confirm it has a `severity` field for counting by severity level.

6. **`entity/src/sbom_advisory.rs`** -- inspect the join table structure to understand how to query advisories linked to an SBOM.

7. **`common/src/error.rs`** -- use `mcp__serena_backend__find_symbol` on `AppError` to confirm error handling patterns.

8. **Backward compatibility check**: use `mcp__serena_backend__find_referencing_symbols` on any symbols being modified (e.g., AdvisoryService) to ensure changes do not break existing callers.

### CONVENTIONS.md Lookup

Repository root is `./` (from Repository Registry Path column). Would check for `CONVENTIONS.md` at the repository root using `mcp__serena_backend__list_dir` or `Glob("./CONVENTIONS.md")`. The repo structure in repo-backend.md shows `CONVENTIONS.md` exists at the root. Would read it and extract:
- Naming rules, directory structure, code patterns, test conventions
- CI check commands (if a CI checks section exists)
- Code generation commands (if any)

### Convention Conformance Analysis (Sibling Analysis)

Sibling files identified for each target file -- see `outputs/conventions.md` for full results.

### Test Convention Analysis

Sibling test files identified: `tests/api/sbom.rs`, `tests/api/advisory.rs`, `tests/api/search.rs`. Would inspect 2-3 of these to understand test patterns -- see `outputs/conventions.md` for full results.

### Documentation File Identification

Documentation files related to modified code:
- `README.md` (repository root)
- `docs/api.md` (REST API reference, from CLAUDE.md documentation section)
- `docs/architecture.md` (system architecture overview)
- `CONVENTIONS.md` (repository root)

These will be checked for documentation currency in Step 9.

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```
git checkout main
git pull
git checkout -b TC-9201
```

Branch `TC-9201` created from target branch `main`.

## Step 6 -- Implement Changes

### Files to Modify

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Add `severity_summary` method to AdvisoryService (see `outputs/file-4-description.md`)
2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Register new route for severity summary endpoint (see `outputs/file-5-description.md`)
3. **`modules/fundamental/src/advisory/model/mod.rs`** -- Add `pub mod severity_summary;` to register the new model module (see `outputs/file-6-description.md`)

### Files to Create

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- SeveritySummary response struct (see `outputs/file-1-description.md`)
2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- GET handler for /api/v2/sbom/{id}/advisory-summary (see `outputs/file-2-description.md`)
3. **`tests/api/advisory_summary.rs`** -- Integration tests for the new endpoint (see `outputs/file-3-description.md`)

### Cross-repo API Contract Verification

Not applicable -- this task creates a backend endpoint, not a frontend consumer of one. No manual REST calls to verify.

## Step 7 -- Write Tests

Tests described in `outputs/file-3-description.md`. Would run `cargo test` after implementation and fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` | Endpoint handler returns `Json<SeveritySummary>` with all five fields |
| Returns 404 when SBOM ID does not exist | Service method checks SBOM existence first, returns `AppError` with 404 if not found |
| Counts only unique advisories (deduplicates by advisory ID) | Service method uses `distinct()` or `HashSet` on advisory ID before counting |
| All severity levels default to 0 when no advisories exist | SeveritySummary struct fields default to 0 via `Default` derive |
| Response time under 200ms for SBOMs with up to 500 advisories | Single database query with join and group-by avoids N+1; would verify with test data |

## Step 9 -- Self-Verification Plan

### Scope Containment
Would run `git diff --name-only` and compare against the 6 files listed in Files to Modify and Files to Create.

### Untracked File Check
Would run `git status --short` and check for `??` entries in directories containing modified files.

### Sensitive-pattern Check
Would run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` to ensure no secrets are staged.

### Documentation Currency
Would check `docs/api.md` to verify it documents the new endpoint. Since a new API endpoint is added, `docs/api.md` may need updating to include `GET /api/v2/sbom/{id}/advisory-summary`.

### Data-flow Trace
- `GET /api/v2/sbom/{id}/advisory-summary` request -> extract path param `id` -> call `AdvisoryService::severity_summary(sbom_id, tx)` -> query `sbom_advisory` join table -> aggregate by severity -> return `Json<SeveritySummary>` -- **COMPLETE**

### Contract & Sibling Parity
- SeveritySummary implements `Serialize` (required for Axum `Json` response) -- verified
- Endpoint handler follows same pattern as `get.rs` (Path extraction, service call, Json response, AppError) -- verified
- Service method follows same signature pattern as `fetch`/`list` (`&self, id, tx`) -- verified

### Duplication Check
Would search for existing severity counting logic to avoid duplication.

## Step 10 -- Commit and Push

### Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, service method
with deduplication, and integration tests.

Implements TC-9201
```

With trailer: `--trailer='Assisted-by: Claude Code'`

### Push and PR Creation

```
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "..."
```

The PR description would include:
- `Implements [TC-9201](<webUrl>)` as a clickable Jira link
- Summary of changes
- If GitHub Issue custom field had a value, a `Closes <owner>/<repo>#<number>` line

## Step 11 -- Update Jira

Would execute:
1. Update Git Pull Request custom field (customfield_10875) with PR URL in ADF format
2. Add comment to TC-9201 with PR link, summary of changes, and any deviations
3. Transition TC-9201 to In Review
