# Implementation Plan for TC-9201

## Task Summary

**Jira Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Parent Feature**: TC-9001 (linked via "is incorporated by")
**Dependencies**: None
**Bookend Type**: None (standard implementation task)
**Target PR**: None (new branch and PR)
**webUrl**: https://redhat.atlassian.net/browse/TC-9201

## Step-by-Step Execution Trace

### Step 0 -- Validate Project Configuration

The project CLAUDE.md contains all required sections:
- **Repository Registry**: present, contains `trustify-backend` mapped to Serena instance `serena_backend` at path `./`
- **Jira Configuration**: present, contains Project key (TC), Cloud ID, Feature issue type ID (10142), Git Pull Request custom field (customfield_10875), GitHub Issue custom field (customfield_10747)
- **Code Intelligence**: present, with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend` using `rust-analyzer`

Validation passes. Proceed.

### Step 0.5 -- JIRA Access Initialization

Would attempt MCP first for all JIRA operations. If MCP fails, prompt user for REST API fallback.

### Step 1 -- Fetch and Parse Jira Task

Parsed sections from TC-9201 description:
- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns summary with counts per severity level (Critical, High, Medium, Low) and total.
- **Files to Modify**: 4 files (advisory.rs service, endpoints/mod.rs, model/mod.rs, server main.rs -- no changes)
- **Files to Create**: 3 files (severity_summary.rs model, severity_summary.rs endpoint, advisory_summary.rs test)
- **API Changes**: GET /api/v2/sbom/{id}/advisory-summary (NEW)
- **Implementation Notes**: Follow existing endpoint pattern in get.rs, add severity_summary method to AdvisoryService, use sbom_advisory join table, use AdvisorySummary severity field, register route in endpoints/mod.rs, error handling with AppError, return struct directly with Json extractor
- **Acceptance Criteria**: 5 items
- **Test Requirements**: 4 items
- **Target PR**: not present
- **Review Context**: not present
- **Bookend Type**: not present
- **Dependencies**: None

**Target Branch extraction**: `main` -- stored for use in Steps 5 and 10.

**GitHub Issue extraction**: Would look up `customfield_10747` from the fetched issue fields. If present, parse the GitHub issue URL to extract owner/repo/number for use in PR description's `Closes` line.

### Step 1.5 -- Verify Description Integrity

Would:
1. Fetch all comments on TC-9201 via `jira.get_issue_comments("TC-9201")`
2. Search for comments starting with `[sdlc-workflow] Description digest:`
3. If multiple matches, select most recent by `created` timestamp
4. If no digest comment found, log warning and proceed: "No description digest found -- skipping integrity check."
5. If digest comment found:
   - Check `created` vs `updated` timestamps for edit detection
   - Extract tagged digest (e.g., `sha256-md:<hex>` or `sha256-adf:<hex>`)
   - If legacy untagged format (`sha256:<hex>`), log warning and skip
   - Write current description to `/tmp/desc-TC-9201.txt`
   - Run `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt` to compute current digest
   - Compare format tags; if mismatch, log warning and skip
   - If tags match, compare hex digests; if mismatch, alert user and ask to proceed or stop

### Step 2 -- Verify Dependencies

No dependencies listed. Skip.

### Step 3 -- Transition to In Progress and Assign

1. Call `jira.user_info()` to get current user's account ID
2. Call `jira.edit_issue("TC-9201", assignee=<account-id>)` to assign
3. Call `jira.transition_issue("TC-9201")` to transition to In Progress

### Step 4 -- Understand the Code

Using Serena instance `serena_backend` (from Repository Registry), tools called as `mcp__serena_backend__<tool>`.

**Code inspection plan:**

1. **Files to Modify -- symbol overview:**
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/service/advisory.rs` -- understand AdvisoryService struct, its `fetch`, `list`, `search` methods
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand route registration pattern
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/mod.rs` -- understand module declarations

2. **Read specific symbols:**
   - `mcp__serena_backend__find_symbol` on `AdvisoryService::fetch` with `include_body=true` -- understand method signature and pattern to follow
   - `mcp__serena_backend__find_symbol` on `AdvisoryService::list` with `include_body=true` -- understand list method pattern
   - `mcp__serena_backend__find_symbol` on `AdvisorySummary` with `include_body=true` in `model/summary.rs` -- understand the `severity` field
   - `mcp__serena_backend__find_symbol` on the get handler in `endpoints/get.rs` with `include_body=true` -- understand endpoint handler pattern (Path extraction, service call, JSON response)

3. **Check backward compatibility:**
   - `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` -- ensure adding a method won't break existing code
   - `mcp__serena_backend__find_referencing_symbols` on `endpoints/mod.rs` route registration -- understand mount pattern

4. **Non-symbolic search:**
   - `mcp__serena_backend__search_for_pattern` for `sbom_advisory` in entity/src/ -- understand the join table structure
   - `mcp__serena_backend__search_for_pattern` for `AppError` in common/src/error.rs -- understand error handling
   - `mcp__serena_backend__search_for_pattern` for `Router::new()` in advisory endpoints -- understand route registration

5. **CONVENTIONS.md lookup:**
   - Read `CONVENTIONS.md` at repo root (exists per repo structure)
   - Extract CI check commands (e.g., `cargo fmt --check`, `cargo clippy`, `cargo test`)
   - Extract code generation commands if any
   - Record verification commands for Step 9

6. **Convention conformance analysis** (see outputs/conventions.md for full results):
   - Sibling analysis on endpoint files (list.rs, get.rs)
   - Sibling analysis on model files (summary.rs, details.rs)
   - Sibling analysis on service files (sbom.rs, advisory.rs)
   - Sibling analysis on test files (sbom.rs, advisory.rs, search.rs in tests/api/)

7. **Documentation file identification:**
   - `README.md` at repo root
   - `docs/api.md` (REST API reference from CLAUDE.md)
   - `docs/architecture.md` (system architecture)
   - `CONVENTIONS.md` at repo root

### Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type). Target Branch is `main`.

```
git checkout main
git pull
git checkout -b TC-9201
```

### Step 6 -- Implement Changes

See file-1 through file-6 description files for detailed changes to each file.

Files to modify:
1. `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
2. `modules/fundamental/src/advisory/endpoints/mod.rs` -- register new route
3. `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`

Files to create:
4. `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
5. `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
6. `tests/api/advisory_summary.rs` -- integration tests

File confirmed as no changes needed:
- `server/src/main.rs` -- routes auto-mount via module registration

**Cross-repo API contract verification**: Not applicable -- this task implements a backend endpoint, not a frontend calling an API.

### Step 7 -- Write Tests

See file-6-description.md for detailed test implementation. Tests follow sibling patterns from `tests/api/sbom.rs` and `tests/api/advisory.rs`.

### Step 8 -- Verify Acceptance Criteria

1. GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }` -- verified by endpoint handler returning SeveritySummary struct with Json extractor
2. Returns 404 when SBOM ID does not exist -- verified by service method returning AppError with 404 when SBOM not found
3. Counts only unique advisories (deduplicates by advisory ID) -- verified by using `.distinct()` or HashSet deduplication in service method
4. All severity levels default to 0 when no advisories exist -- verified by SeveritySummary::default() initializing all counts to 0
5. Response time under 200ms for SBOMs with up to 500 advisories -- verified by single query with join (no N+1)

### Step 9 -- Self-Verification

1. **Scope containment**: `git diff --name-only` should show only the 6 files listed above (3 modified, 3 created). If any out-of-scope file appears, flag and ask user.
2. **Untracked file check**: Run `git status --short`, check for `??` entries in directories where implementation occurred (modules/fundamental/src/advisory/, tests/api/).
3. **Sensitive-pattern check**: `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- expect no matches.
4. **Documentation currency**: Check if `docs/api.md` needs updating for the new endpoint. Update if so.
5. **Duplication check**: Search for existing severity aggregation logic in the codebase to avoid duplication.
6. **CI checks from CONVENTIONS.md**: Run extracted CI commands (cargo fmt --check, cargo clippy, cargo test). Hard stop on any failure.
7. **Data-flow trace**: GET request -> extract path param (sbom_id) -> call AdvisoryService::severity_summary -> query sbom_advisory join table -> count by severity -> return SeveritySummary as JSON. All stages connected. COMPLETE.
8. **Contract & sibling parity**: Verify SeveritySummary implements Serialize. Verify handler follows same error handling pattern as get.rs. Verify service method follows same pattern as fetch/list.
9. **Cross-section reference consistency**: Verify that all references to AdvisoryService point to `modules/fundamental/src/advisory/service/advisory.rs` consistently across Files to Modify and Implementation Notes. (Both agree on this path.)

### Step 10 -- Commit and Push

**Commit message:**

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, service method,
endpoint handler, and integration tests.

Implements TC-9201
```

With `--trailer="Assisted-by: Claude Code"`.

**Fork detection**: Run `git remote get-url upstream 2>/dev/null`. If succeeds, parse upstream owner/repo and fork owner for PR creation flags.

**Push and PR creation** (assuming no fork):

```
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" --body "..."
```

PR description includes:
- Summary of changes
- `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)`
- If GitHub issue was extracted from customfield_10747: `Closes <owner>/<repo>#<number>`

### Step 11 -- Update Jira

1. **Git Pull Request custom field** (`customfield_10875`): Update with PR URL in ADF format (inlineCard)
2. **Add comment**: Include PR link, summary of changes, any deviations. Append comment footnote with plugin version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`.
3. **Transition**: Move TC-9201 to In Review

## Files Summary

| # | File Path | Action | Description |
|---|-----------|--------|-------------|
| 1 | `modules/fundamental/src/advisory/service/advisory.rs` | Modify | Add `severity_summary` method to AdvisoryService |
| 2 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Modify | Register the new GET route |
| 3 | `modules/fundamental/src/advisory/model/mod.rs` | Modify | Add `pub mod severity_summary;` declaration |
| 4 | `modules/fundamental/src/advisory/model/severity_summary.rs` | Create | SeveritySummary response struct |
| 5 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | Create | GET handler for /api/v2/sbom/{id}/advisory-summary |
| 6 | `tests/api/advisory_summary.rs` | Create | Integration tests for the new endpoint |
