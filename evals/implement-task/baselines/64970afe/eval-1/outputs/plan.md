# Implementation Plan for TC-9201

## Task Summary

**Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Status**: To Do
**Repository**: trustify-backend
**Target Branch**: main
**Branch Name**: TC-9201
**Labels**: ai-generated-jira
**Linked Issues**: is incorporated by TC-9001
**Dependencies**: None

## Step 0 -- Validate Project Configuration

The project CLAUDE.md contains all required sections under `# Project Configuration`:
1. **Repository Registry** -- present with `trustify-backend` entry (Serena Instance: `serena_backend`, Path: `./`)
2. **Jira Configuration** -- present with Project key (`TC`), Cloud ID (`2b9e35e3-6bd3-4cec-b838-f4249ee02432`), Feature issue type ID (`10142`)
3. **Code Intelligence** -- present with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend`

Validation passed. Proceeding.

## Step 1 -- Fetch and Parse Jira Task

Parsed sections from TC-9201:

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Description | Add severity aggregation service and REST endpoint |
| Files to Modify | 3 files (advisory.rs, endpoints/mod.rs, model/mod.rs) |
| Files to Create | 3 files (severity_summary.rs model, severity_summary.rs endpoint, advisory_summary.rs test) |
| API Changes | `GET /api/v2/sbom/{id}/advisory-summary` (NEW) |
| Implementation Notes | Present -- references get.rs pattern, AdvisoryService, sbom_advisory join table, AdvisorySummary.severity field |
| Acceptance Criteria | 5 criteria |
| Test Requirements | 4 test cases |
| Target PR | Not present (default flow) |
| Bookend Type | Not present (default flow) |
| Review Context | Not present |
| Dependencies | None |

### Target Branch Extraction

Target Branch: `main`. This will be used as the base for branch creation in Step 5 and as the `--base` argument for `gh pr create` in Step 10.

### GitHub Issue Extraction

The Jira Configuration in CLAUDE.md lists `GitHub Issue custom field: customfield_10747`. In a real execution, the field value would be read from the fetched issue's fields. If present, the GitHub issue URL would be parsed and a `Closes <owner>/<repo>#<number>` line would be appended to the PR description.

## Step 1.5 -- Verify Description Integrity

In a real execution, we would:

1. **Retrieve issue comments**: Call `jira.get_issue_comments("TC-9201")` to fetch all comments.
2. **Locate digest comment**: Search for comments starting with `[sdlc-workflow] Description digest:`.
3. **If no digest comment found**: Since this is a synthetic task and no comments exist, we would log the following warning and proceed normally:

   > "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced."

4. **Backward compatibility**: The absence of a digest comment does NOT block execution. This is the backward-compatible path for tasks created before digest tracking was introduced by the description-digest-protocol.

## Step 2 -- Verify Dependencies

The task lists "Dependencies: None". No dependency verification needed. Proceeding.

## Step 3 -- Transition to In Progress and Assign

In a real execution:
1. Call `jira.user_info()` to get current user's account ID.
2. Call `jira.edit_issue("TC-9201", assignee=<account-id>)` to assign the task.
3. Call `jira.transition_issue("TC-9201")` to transition to "In Progress".

## Step 4 -- Understand the Code

### Files to inspect before modifying

Using Serena instance `serena_backend` (from Repository Registry):

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Use `mcp__serena_backend__get_symbols_overview` to see existing methods (`fetch`, `list`, `search`). Then use `mcp__serena_backend__find_symbol` with `include_body=true` on one method (e.g., `fetch`) to understand the exact signature pattern, transaction handling, and error wrapping.

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Use `mcp__serena_backend__get_symbols_overview` to see existing route registrations and how `Router::new().route()` chains are structured.

3. **`modules/fundamental/src/advisory/model/mod.rs`** -- Read this file to see existing `pub mod` declarations for sibling models (`summary`, `details`).

4. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- Use `mcp__serena_backend__find_symbol` on the handler function to understand the exact handler pattern (Path extraction, service call, JSON response).

5. **`modules/fundamental/src/advisory/model/summary.rs`** -- Use `mcp__serena_backend__find_symbol` on `AdvisorySummary` to confirm the `severity` field exists and understand its type.

6. **`entity/src/sbom_advisory.rs`** -- Use `mcp__serena_backend__get_symbols_overview` to understand the join table entity structure for linking SBOMs to advisories.

7. **`common/src/error.rs`** -- Use `mcp__serena_backend__find_symbol` on `AppError` to understand the error enum and `.context()` usage.

### Sibling analysis targets

- **Service siblings**: `modules/fundamental/src/sbom/service/sbom.rs` -- compare `SbomService` method patterns.
- **Endpoint siblings**: `modules/fundamental/src/advisory/endpoints/list.rs`, `modules/fundamental/src/sbom/endpoints/get.rs` -- compare handler patterns.
- **Model siblings**: `modules/fundamental/src/advisory/model/details.rs`, `modules/fundamental/src/sbom/model/summary.rs` -- compare struct derive macros and field types.
- **Test siblings**: `tests/api/advisory.rs`, `tests/api/sbom.rs` -- compare assertion patterns, test naming, setup/teardown.

### CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md` per Repository Registry Path). The repository structure confirms this file exists. Read it for naming rules, directory structure, code patterns, test conventions, and CI check commands.

### Documentation file identification

- `README.md` at repository root
- `docs/api.md` -- API reference documentation (may need updating with new endpoint)
- `docs/architecture.md` -- System architecture overview

### Backward compatibility check

Use `mcp__serena_backend__find_referencing_symbols` on any symbols being modified (e.g., the route registration in `endpoints/mod.rs`) to ensure changes do not break existing callers. Since we are only adding new methods and routes (not modifying existing ones), backward compatibility risk is low.

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

This creates a branch named `TC-9201` from the target branch `main`.

## Step 6 + 7 -- Implementation and Tests

### Files to Modify (3 files)

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Add `severity_summary` method to `AdvisoryService`
2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Register the new route for the severity summary endpoint
3. **`modules/fundamental/src/advisory/model/mod.rs`** -- Add `pub mod severity_summary;` to register the new model module

### Files to Create (3 files)

4. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- Define `SeveritySummary` response struct
5. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- Implement GET handler for `/api/v2/sbom/{id}/advisory-summary`
6. **`tests/api/advisory_summary.rs`** -- Integration tests for the new endpoint

See `file-1-description.md` through `file-6-description.md` for detailed changes to each file.

## Step 8 -- Verify Acceptance Criteria

| # | Criterion | How Verified |
|---|---|---|
| 1 | GET /api/v2/sbom/{id}/advisory-summary returns correct shape | Endpoint returns `SeveritySummary` struct with `critical`, `high`, `medium`, `low`, `total` fields |
| 2 | Returns 404 when SBOM ID does not exist | Handler queries SBOM first; if not found, returns `AppError` with 404 status |
| 3 | Counts only unique advisories | Query uses DISTINCT or deduplication by advisory ID before counting |
| 4 | All severity levels default to 0 | `SeveritySummary::default()` initializes all counts to 0; counting only increments matched levels |
| 5 | Response time under 200ms for up to 500 advisories | Single SQL query with GROUP BY -- no N+1; verified via integration test timing |

## Step 9 -- Self-Verification

### Scope containment
Run `git diff --name-only` and compare against Files to Modify + Files to Create. Only these 6 files should appear. `server/src/main.rs` is explicitly noted as "no changes needed" -- confirm it is not modified.

### Untracked file check
Run `git status --short` and check for `??` entries in directories where implementation occurred. Flag any untracked files for review.

### Sensitive-pattern check
Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- expect no matches.

### Documentation currency
Check if `docs/api.md` needs updating with the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. If so, add the endpoint documentation.

### Duplication check
Search for existing severity aggregation or counting logic in the repository to avoid duplicating functionality.

### Data-flow trace
- Input: `GET /api/v2/sbom/{id}/advisory-summary` with SBOM ID path parameter
- Processing: Endpoint handler extracts ID -> calls `AdvisoryService::severity_summary(id, tx)` -> service queries `sbom_advisory` join table -> joins to advisory table -> groups by severity -> counts per level -> deduplicates by advisory ID
- Output: Returns `Json<SeveritySummary>` with `{ critical, high, medium, low, total }` -- **COMPLETE**

### Contract & sibling parity
- `SeveritySummary` is a standalone struct (no trait/interface to implement)
- Sibling parity with `get.rs` endpoint: error handling (Result<T, AppError>) -- match; Path extraction -- match; JSON response -- match
- No cross-module shared entity concerns (read-only query, no inserts/updates/deletes)

### Cross-section reference consistency
- Entity `AdvisoryService` -- Files to Modify: `modules/fundamental/src/advisory/service/advisory.rs`; Implementation Notes: `modules/fundamental/src/advisory/service/advisory.rs` -- consistent
- Entity `AdvisorySummary` (existing) -- Implementation Notes reference: `modules/fundamental/src/advisory/model/summary.rs` -- consistent with repo structure
- Entity severity_summary endpoint -- Files to Create: `modules/fundamental/src/advisory/endpoints/severity_summary.rs`; Implementation Notes reference get.rs pattern at `modules/fundamental/src/advisory/endpoints/get.rs` -- consistent (pattern reference, not same file)

All cross-section references are consistent.

## Step 10 -- Commit and Push

### Commit message

```
feat(advisory): add severity aggregation service and endpoint

Add a service method and REST endpoint that aggregates vulnerability
advisory severity counts for a given SBOM. The endpoint GET
/api/v2/sbom/{id}/advisory-summary returns counts per severity level
(Critical, High, Medium, Low) and a total.

Implements TC-9201
```

With flag: `--trailer='Assisted-by: Claude Code'`

Full command:
```bash
git add modules/fundamental/src/advisory/service/advisory.rs \
       modules/fundamental/src/advisory/endpoints/mod.rs \
       modules/fundamental/src/advisory/model/mod.rs \
       modules/fundamental/src/advisory/model/severity_summary.rs \
       modules/fundamental/src/advisory/endpoints/severity_summary.rs \
       tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation service and endpoint

Add a service method and REST endpoint that aggregates vulnerability
advisory severity counts for a given SBOM. The endpoint GET
/api/v2/sbom/{id}/advisory-summary returns counts per severity level
(Critical, High, Medium, Low) and a total.

Implements TC-9201"
```

### Push and PR creation

```bash
git push -u origin TC-9201

gh pr create --base main --title "feat(advisory): add severity aggregation service and endpoint" --body "## Summary

Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM.

- New endpoint: \`GET /api/v2/sbom/{id}/advisory-summary\`
- Returns \`{ critical, high, medium, low, total }\` counts
- Deduplicates advisory counts by advisory ID
- Returns 404 for non-existent SBOM IDs
- Includes integration tests for all acceptance criteria

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
"
```

Note: If a GitHub issue reference was found in `customfield_10747`, a `Closes <owner>/<repo>#<number>` line would be appended to the PR body.

## Step 11 -- Update Jira

### Git Pull Request custom field

From CLAUDE.md Jira Configuration: `Git Pull Request custom field: customfield_10875`.

```
jira.update_issue("TC-9201", fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
```

### Jira comment

Post a comment to TC-9201 with:
- PR link
- Summary of changes made
- No deviations from the plan

The comment would end with the plugin footer (reading version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`).

### Transition

```
jira.transition_issue("TC-9201") -> In Review
```
