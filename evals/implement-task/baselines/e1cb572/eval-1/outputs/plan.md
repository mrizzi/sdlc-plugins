# Implementation Plan for TC-9201

## Task Summary

**Jira Key:** TC-9201
**Summary:** Add advisory severity aggregation service and endpoint
**Repository:** trustify-backend
**Target Branch:** main
**Status:** To Do
**Parent Feature:** TC-9001 (is incorporated by)
**Dependencies:** None

## Step 0 -- Validate Project Configuration

Verify CLAUDE.md contains the required sections:

1. **Repository Registry** -- Present. Contains `trustify-backend` with Serena instance `serena_backend` and path `./`.
2. **Jira Configuration** -- Present. Project key: TC, Cloud ID: `2b9e35e3-6bd3-4cec-b838-f4249ee02432`, Feature issue type ID: 10142.
3. **Code Intelligence** -- Present. Tool naming convention: `mcp__<serena-instance>__<tool>`. Configured instance: `serena_backend` with `rust-analyzer`.

All sections present and valid. Proceed.

## Step 0.5 -- JIRA Access Initialization

Would attempt MCP first for all JIRA operations. If MCP fails, prompt user with REST API fallback options per the skill specification.

## Step 1 -- Fetch and Parse Jira Task

Parsed sections from TC-9201:

- **Repository:** trustify-backend
- **Target Branch:** main
- **Description:** Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM.
- **Files to Modify:** 3 files (advisory service, endpoints mod, model mod)
- **Files to Create:** 3 files (severity_summary model, severity_summary endpoint, integration tests)
- **API Changes:** `GET /api/v2/sbom/{id}/advisory-summary` (NEW)
- **Implementation Notes:** Follow existing endpoint patterns, use `sbom_advisory` join table, use `AdvisorySummary.severity` field
- **Acceptance Criteria:** 5 criteria covering response shape, 404 handling, deduplication, defaults, and performance
- **Test Requirements:** 4 test cases
- **Target PR:** Not present (default flow)
- **Bookend Type:** Not present (default flow)
- **Dependencies:** None
- **webUrl:** Would be captured from `jira.get_issue()` response (e.g., `https://redhat.atlassian.net/browse/TC-9201`)

### GitHub Issue Extraction

The Jira Configuration specifies `GitHub Issue custom field: customfield_10747`. Would read this field from the fetched issue. If present, parse the GitHub issue URL for use in the PR description's `Closes` line.

## Step 1.5 -- Verify Description Integrity

1. **Retrieve issue comments:** Call `jira.get_issue_comments(TC-9201)` to fetch all comments.
2. **Locate digest comment:** Search for comments starting with `[sdlc-workflow] Description digest:`. Select the most recent one by `created` timestamp if multiple exist.
3. **If no digest comment found:** Log warning and proceed normally:
   > "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced."
4. **If digest comment found:**
   - Check if `updated` > `created` (warn if edited after posting)
   - Extract tagged digest (e.g., `sha256-md:a1b2...`)
   - If legacy untagged format (`sha256:<hex>`), warn and skip
   - Compute current digest: `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
   - Compare format tags; if mismatched, warn and skip
   - Compare hex digests; if mismatched, alert user with both digests and ask whether to proceed or stop

Since this is an eval and we cannot call Jira, we note this step would be executed. If no digest is found, we proceed with the warning.

## Step 2 -- Verify Dependencies

Task specifies "Depends on: None". No dependency checks required. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Call `jira.user_info()` to get current user's account ID.
2. Call `jira.edit_issue(TC-9201, assignee=<account-id>)` to assign.
3. Call `jira.transition_issue(TC-9201, "In Progress")` to update status.

## Step 4 -- Understand the Code

### Code Inspection (using `serena_backend`)

1. **Inspect files to modify:**
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/service/advisory.rs` -- understand `AdvisoryService` struct and its `fetch`, `list` methods
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand route registration pattern
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/mod.rs` -- see existing module declarations

2. **Read specific symbols:**
   - `mcp__serena_backend__find_symbol("AdvisoryService", include_body=true)` -- read `fetch` method body to understand the service pattern
   - `mcp__serena_backend__find_symbol("AdvisorySummary", include_body=true)` -- read struct to understand the `severity` field type
   - `mcp__serena_backend__find_symbol("AppError", include_body=true)` -- understand error enum variants

3. **Check backward compatibility:**
   - `mcp__serena_backend__find_referencing_symbols("AdvisoryService")` -- verify no callers will break

4. **Non-symbolic search:**
   - `mcp__serena_backend__search_for_pattern("sbom_advisory")` -- locate the join table usage
   - `mcp__serena_backend__search_for_pattern("Router::new")` in endpoints directories -- confirm route registration pattern

5. **Convention conformance analysis:**
   - Analyze siblings: `get.rs` and `list.rs` in `advisory/endpoints/` for endpoint patterns
   - Analyze siblings: `summary.rs` and `details.rs` in `advisory/model/` for model struct patterns
   - Analyze siblings: `sbom.rs` and `advisory.rs` in `tests/api/` for test patterns

### CONVENTIONS.md Lookup

Repository root path from Registry: `./`. Check for `./CONVENTIONS.md`. The file exists per repo-backend.md. Would read it and extract:
- All CI check commands for Step 9 verification
- Any code generation commands
- Project-specific conventions

### Documentation File Identification

- `README.md` at repository root
- `docs/api.md` (API reference, per CLAUDE.md)
- `docs/architecture.md` (system architecture)

### Convention Conformance Analysis

See `outputs/conventions.md` for the full discovered conventions list.

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

This creates a task branch named `TC-9201` from the target branch `main`.

## Step 6 -- Implement Changes

### Files to Create

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- New file: `SeveritySummary` response struct
2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- New file: GET handler for `/api/v2/sbom/{id}/advisory-summary`
3. **`tests/api/advisory_summary.rs`** -- New file: Integration tests

### Files to Modify

4. **`modules/fundamental/src/advisory/model/mod.rs`** -- Add `pub mod severity_summary;`
5. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Add `severity_summary` method
6. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Register the new route

### No API Documentation Updates Needed

The task does not include a Documentation Updates section. Would check `docs/api.md` after implementation to see if it documents advisory endpoints and needs a new entry for the severity summary endpoint.

## Step 7 -- Write Tests

Write integration tests in `tests/api/advisory_summary.rs` covering all 4 test requirements. See `outputs/file-6-description.md` for details.

## Step 8 -- Verify Acceptance Criteria

| # | Criterion | Verification Method |
|---|-----------|-------------------|
| 1 | GET endpoint returns `{ critical, high, medium, low, total }` | Test: valid SBOM returns correct shape and counts |
| 2 | Returns 404 for non-existent SBOM | Test: non-existent ID returns 404 |
| 3 | Counts only unique advisories (dedup by advisory ID) | Test: duplicate advisory links produce correct count |
| 4 | All severity levels default to 0 | Test: SBOM with no advisories returns all zeros |
| 5 | Response time under 200ms for up to 500 advisories | Verified by query design (single aggregation query) |

## Step 9 -- Self-Verification

### Scope Containment
Run `git diff --name-only` and verify all changed files are within the Files to Modify and Files to Create lists:
- `modules/fundamental/src/advisory/model/severity_summary.rs` (create)
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (create)
- `tests/api/advisory_summary.rs` (create)
- `modules/fundamental/src/advisory/model/mod.rs` (modify)
- `modules/fundamental/src/advisory/service/advisory.rs` (modify)
- `modules/fundamental/src/advisory/endpoints/mod.rs` (modify)

### Untracked File Check
Run `git status --short`, filter `??` entries, check for proximity to modified directories, search for code references.

### Sensitive-Pattern Check
Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- expect no matches.

### Documentation Currency
Check if `docs/api.md` documents advisory endpoints. If so, add entry for `GET /api/v2/sbom/{id}/advisory-summary`.

### Data-Flow Trace
- `GET /api/v2/sbom/{id}/advisory-summary` -> extract `Path<Id>` -> call `AdvisoryService::severity_summary(sbom_id, tx)` -> query `sbom_advisory` join table -> aggregate by severity -> return `SeveritySummary` as JSON -- **COMPLETE**

### Contract & Sibling Parity
- `SeveritySummary` -- standalone struct, no trait implementation required
- Sibling parity with `get.rs` endpoint: error handling pattern (AppError + context), Path extraction, service call pattern -- all matched
- Cross-module: `sbom_advisory` entity used by ingestor module -- would verify transaction and query patterns match

### CI Checks from CONVENTIONS.md
Run all CI check commands extracted from CONVENTIONS.md. Hard stop on any failure.

### Duplication Check
Search for existing severity aggregation or summary counting logic in the codebase to avoid duplicating.

## Step 10 -- Commit and Push

### Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add SeveritySummary model, AdvisoryService.severity_summary() method,
and GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
per-severity counts (critical, high, medium, low) and total for a
given SBOM's linked advisories. Includes integration tests for valid
SBOM, non-existent SBOM (404), empty advisories, and deduplication.

Implements TC-9201
```

### Commit Command

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      tests/api/advisory_summary.rs
git commit --trailer='Assisted-by: Claude Code' -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add SeveritySummary model, AdvisoryService.severity_summary() method,
and GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
per-severity counts (critical, high, medium, low) and total for a
given SBOM's linked advisories. Includes integration tests for valid
SBOM, non-existent SBOM (404), empty advisories, and deduplication.

Implements TC-9201"
```

### Push and Create PR

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" --body "## Summary

Add a new REST endpoint \`GET /api/v2/sbom/{id}/advisory-summary\` that aggregates vulnerability advisory severity counts for a given SBOM, returning counts per severity level (Critical, High, Medium, Low) and a total.

### Changes
- New \`SeveritySummary\` response model struct
- New \`AdvisoryService::severity_summary()\` method using \`sbom_advisory\` join table
- New endpoint handler registered at \`/api/v2/sbom/{id}/advisory-summary\`
- Integration tests covering valid SBOM, 404, empty advisories, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)"
```

If a GitHub issue reference was extracted from `customfield_10747`, append `Closes <owner>/<repo>#<number>` to the PR body.

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (`customfield_10875`) with the PR URL in ADF format:
   ```
   jira.update_issue(TC-9201, fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
   ```

2. **Add Jira comment** with:
   - PR link
   - Summary: Added `GET /api/v2/sbom/{id}/advisory-summary` endpoint with `SeveritySummary` model, service method, and integration tests
   - No deviations from plan
   - Comment footer with plugin version and sdlc-workflow link (per Comment Footnote specification)

3. **Transition to In Review:**
   ```
   jira.transition_issue(TC-9201, "In Review")
   ```
