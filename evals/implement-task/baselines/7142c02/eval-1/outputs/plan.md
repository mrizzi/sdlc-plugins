# Implementation Plan for TC-9201

## Task Summary

**Jira Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main (extracted from the Target Branch section of the task description)
**Status**: To Do
**Parent**: is incorporated by TC-9001

---

## Full Workflow Lifecycle

### Step 0 -- Validate Project Configuration

Verify the project's CLAUDE.md contains the required sections under `# Project Configuration`:

1. **Repository Registry** -- Present. Contains `trustify-backend` with Serena instance `serena_backend` at path `./`.
2. **Jira Configuration** -- Present. Contains Project key: TC, Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432, Feature issue type ID: 10142, Git Pull Request custom field: customfield_10875, GitHub Issue custom field: customfield_10747.
3. **Code Intelligence** -- Present. Tool naming convention documented; serena_backend instance configured with rust-analyzer.

All sections present and valid. Proceed.

### Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all JIRA operations. If MCP fails, prompt the user with the three options (REST API fallback, skip, retry) as specified in the skill definition.

### Step 1 -- Fetch and Parse Jira Task

Use `jira.get_issue(TC-9201)` to fetch the task.

**Parsed sections:**

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | **main** (extracted from the Target Branch section -- this is the branch the PR will target and the branch to checkout before creating the task branch) |
| Description | Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM |
| Files to Modify | 4 files (advisory.rs, endpoints/mod.rs, model/mod.rs, server/main.rs) |
| Files to Create | 3 files (severity_summary.rs model, severity_summary.rs endpoint, advisory_summary.rs test) |
| API Changes | GET /api/v2/sbom/{id}/advisory-summary (NEW) |
| Implementation Notes | Follow existing endpoint patterns, use sbom_advisory join table, etc. |
| Acceptance Criteria | 5 criteria |
| Test Requirements | 4 test cases |
| Target PR | Not present (default flow) |
| Review Context | Not present |
| Bookend Type | Not present (default flow) |
| Dependencies | None |

**Target Branch extraction**: The Target Branch section contains the value `main`. This is stored for use in Steps 5 and 10 -- the task branch will be created from `main`, and the PR will target `main` via `--base main`.

**Bookend Type extraction**: No Bookend Type section present. This is a standard implementation task (not a bookend).

**GitHub Issue extraction**: The Jira Configuration lists `GitHub Issue custom field: customfield_10747`. Read this field from the fetched issue's fields. If it contains a URL like `https://github.com/owner/repo/issues/N`, parse it as `owner/repo#N` for use in the PR description's `Closes` line. If empty or not set, skip silently.

**webUrl**: Capture the issue's webUrl (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for use in the PR description.

### Step 1.5 -- Verify Description Integrity

1. **Retrieve issue comments**: Call `jira.get_issue_comments(TC-9201)` to fetch all comments.

2. **Locate the digest comment**: Search for comments whose body starts with `[sdlc-workflow] Description digest:`. If multiple match, select the most recent by `created` timestamp.

3. **If no digest comment found**: Log a warning and proceed normally -- do not block execution:

   > "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced."

   This maintains backward compatibility with tasks created before digest tracking was introduced.

4. **If digest comment found**: Follow the full verification flow:
   - Check for comment editing (compare `created` vs `updated` timestamps)
   - Extract the stored digest (tagged format like `sha256-md:a1b2...` or `sha256-adf:a1b2...`)
   - Handle legacy untagged format (`sha256:<hex>`) by logging a warning and skipping
   - Compute the current digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
   - Compare format tags; if mismatched, log a warning and skip
   - Compare hex digests; if matched, proceed silently; if mismatched, alert user and stop for confirmation

### Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

### Step 3 -- Transition to In Progress and Assign

1. `jira.user_info()` -- get current user's account ID
2. `jira.edit_issue(TC-9201, assignee=<current-user-account-id>)` -- assign to self
3. `jira.transition_issue(TC-9201)` -> In Progress

### Step 4 -- Understand the Code

**Serena instance**: `serena_backend` (from Repository Registry)

1. **Overview of files to modify**:
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/service/advisory.rs` -- understand AdvisoryService structure (fetch, list, search methods)
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand route registration pattern
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/mod.rs` -- understand model module registration
   - Read `server/src/main.rs` to confirm routes auto-mount (task says no changes needed)

2. **Read specific symbols**:
   - `mcp__serena_backend__find_symbol` on `AdvisoryService.fetch` (include_body=true) to understand the method signature and pattern
   - `mcp__serena_backend__find_symbol` on `AdvisoryService.list` (include_body=true) for the same reason
   - `mcp__serena_backend__find_symbol` on `AdvisorySummary` (include_body=true) to understand the severity field structure

3. **Check backward compatibility**:
   - `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to ensure adding a method won't break callers

4. **Non-symbolic search**:
   - `mcp__serena_backend__search_for_pattern` for `sbom_advisory` to understand the join table structure
   - `mcp__serena_backend__search_for_pattern` for `AppError` and `.context()` patterns

5. **Convention conformance analysis** (sibling inspection):
   - Inspect `modules/fundamental/src/advisory/endpoints/get.rs` as a sibling endpoint handler
   - Inspect `modules/fundamental/src/advisory/endpoints/list.rs` as another sibling
   - Inspect `modules/fundamental/src/sbom/endpoints/get.rs` for cross-module endpoint patterns
   - Inspect `modules/fundamental/src/advisory/model/summary.rs` and `details.rs` as sibling model files

6. **CONVENTIONS.md lookup**:
   - Repository root path is `./` (from Repository Registry)
   - CONVENTIONS.md exists at root (per repo structure) -- read it
   - Extract CI check commands (formatting, linting, compilation) for use in Step 9
   - Extract any code generation commands

7. **Test convention analysis**:
   - Inspect `tests/api/advisory.rs` as a sibling test file
   - Inspect `tests/api/sbom.rs` as another sibling test file
   - Document assertion patterns, test naming, setup/teardown, etc.

8. **Documentation file identification**:
   - `README.md` at root
   - `docs/architecture.md`
   - `docs/api.md` (REST API reference -- likely needs updating for the new endpoint)

### Step 5 -- Create Branch

This is the **default flow** (no Target PR, no Bookend Type).

Extract the Target Branch value from the task description: **main**.

Execute:
```
git checkout main && git pull && git checkout -b TC-9201
```

This checks out `main` (the target branch), pulls latest changes, and creates a new branch named `TC-9201` for the task.

### Step 6 -- Implement Changes

#### Files to Create

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- SeveritySummary response struct
2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- GET handler
3. **`tests/api/advisory_summary.rs`** -- integration tests (handled in Step 7)

#### Files to Modify

1. **`modules/fundamental/src/advisory/model/mod.rs`** -- add `pub mod severity_summary;`
2. **`modules/fundamental/src/advisory/service/advisory.rs`** -- add `severity_summary` method
3. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- register the new route
4. **`server/src/main.rs`** -- no changes needed (confirmed routes auto-mount)

See file-N-description.md files for detailed changes per file.

#### Cross-repo API contract verification

Not applicable -- this task is a backend-only change, not a frontend consuming a backend API.

#### Code quality practices

- Every new struct (`SeveritySummary`) gets a doc comment
- Every new public function (`severity_summary` method, `get_advisory_summary` handler) gets a doc comment
- Follow naming conventions from siblings

#### Documentation impact

- No `Documentation Updates` section in the task
- `docs/api.md` likely needs a new entry for `GET /api/v2/sbom/{id}/advisory-summary`
- Keep the update lightweight -- add the endpoint, parameters, and response shape

### Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with 4 test functions (see file-6-description.md for details).

Follow test conventions discovered in Step 4 from sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`).

Run `cargo test` to verify all tests pass. Fix any failures before proceeding.

### Step 8 -- Verify Acceptance Criteria

| # | Criterion | Verification |
|---|---|---|
| 1 | GET /api/v2/sbom/{id}/advisory-summary returns correct JSON shape | Verified by test 1 (known advisories return correct counts) and code review of response struct |
| 2 | Returns 404 when SBOM ID does not exist | Verified by test 2 (non-existent SBOM returns 404) |
| 3 | Counts only unique advisories (deduplicates by advisory ID) | Verified by test 4 (duplicate advisory links deduplicated) and code review of SQL/query logic |
| 4 | All severity levels default to 0 when no advisories exist | Verified by test 3 (SBOM with no advisories returns all zeros) |
| 5 | Response time under 200ms for SBOMs with up to 500 advisories | Architecture review: single query with GROUP BY should be efficient; verified by running test with representative data |

### Step 9 -- Self-Verification

1. **Scope containment**: Run `git diff --name-only` and compare against Files to Modify and Files to Create. Flag any out-of-scope files.

2. **Untracked file check**: Run `git status --short` and check for `??` entries in directories where implementation occurred. Flag any referenced untracked files.

3. **Sensitive-pattern check**: `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- ensure no secrets in the diff.

4. **Documentation currency**: Verify `docs/api.md` is updated with the new endpoint if the implementation changed public APIs.

5. **Documentation scope preservation**: If `docs/api.md` was modified, verify the replacement text still covers all previously documented use cases.

6. **Eval coverage currency**: No SKILL.md files modified -- skip.

7. **Example consistency**: If documentation with examples was updated, verify internal consistency between narrative and data structures.

8. **Cross-section reference consistency**: Verify that file paths for entities are consistent across Files to Modify, Files to Create, and Implementation Notes. (Note: the task description uses `advisory.rs` consistently for AdvisoryService.)

9. **Duplication check**: Search for existing severity aggregation logic or similar counting patterns. Ensure no duplication.

10. **CI checks from CONVENTIONS.md**: Run all CI check commands extracted in Step 4. Hard stop on any failure.

11. **Data-flow trace**:
    - `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param (sbom_id) -> call `AdvisoryService.severity_summary(sbom_id, tx)` -> query sbom_advisory join + advisory table -> aggregate by severity -> return SeveritySummary JSON -- **COMPLETE**

12. **Contract & sibling parity**:
    - SeveritySummary implements Serialize (for JSON response) -- verified
    - Sibling parity with `get.rs`, `list.rs` endpoints: error handling pattern, Path extraction, service call pattern -- verified
    - Caller-site parity: N/A (new endpoint, no existing callers)

### Step 10 -- Commit and Push

**Commit message** (Conventional Commits format with Jira issue ID in footer):

```
git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, AdvisoryService
method, endpoint handler, and integration tests.

Implements TC-9201"
```

The `--trailer='Assisted-by: Claude Code'` flag is included to attribute AI assistance.

**Push and create PR** (default flow -- no Target PR, no Bookend Type):

```
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "$(cat <<'EOF'
## Summary

Add a new endpoint `GET /api/v2/sbom/{id}/advisory-summary` that aggregates
vulnerability advisory severity counts for a given SBOM, returning counts per
severity level (Critical, High, Medium, Low) and a total.

### Changes
- New `SeveritySummary` response model
- New `severity_summary` method on `AdvisoryService`
- New endpoint handler with route registration
- Integration tests covering happy path, 404, empty, and deduplication cases
- Updated API documentation

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
EOF
)"
```

The `--base main` flag explicitly targets the branch extracted from the Target Branch section.

If a GitHub issue reference was extracted in Step 1 (from `customfield_10747`), append a `Closes owner/repo#N` line to the PR body.

### Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (`customfield_10875`) with the PR URL in ADF format:

```
jira.update_issue(TC-9201, fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
```

2. **Add comment** to TC-9201 with:
   - PR link
   - Summary of changes made
   - Any deviations from the plan
   - Comment ends with the plugin footnote (sdlc-workflow/implement-task v0.11.0)

3. **Transition** the issue: `jira.transition_issue(TC-9201)` -> In Review

---

## Files to Create

| # | File | Description File |
|---|---|---|
| 1 | `modules/fundamental/src/advisory/model/severity_summary.rs` | file-1-description.md |
| 2 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | file-2-description.md |
| 3 | `tests/api/advisory_summary.rs` | file-6-description.md |

## Files to Modify

| # | File | Description File |
|---|---|---|
| 4 | `modules/fundamental/src/advisory/model/mod.rs` | file-3-description.md |
| 5 | `modules/fundamental/src/advisory/service/advisory.rs` | file-4-description.md |
| 6 | `modules/fundamental/src/advisory/endpoints/mod.rs` | file-5-description.md |

## Files Not Modified

- `server/src/main.rs` -- confirmed no changes needed (routes auto-mount via module registration)

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, AdvisoryService
method, endpoint handler, and integration tests.

Implements TC-9201
Assisted-by: Claude Code
```

The commit uses `--trailer='Assisted-by: Claude Code'` to add the trailer automatically.
