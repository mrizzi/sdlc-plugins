# Implementation Plan for TC-9201

## Task Summary

**Jira Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Status**: To Do
**Parent**: is incorporated by TC-9001
**Repository**: trustify-backend
**Target Branch**: main
**Bookend Type**: none
**Target PR**: none
**Web URL**: https://redhat.atlassian.net/browse/TC-9201

## Step 0 -- Validate Project Configuration

The project CLAUDE.md contains all required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena Instance `serena_backend` at path `./`
2. **Jira Configuration** -- present with Project key: TC, Cloud ID, Feature issue type ID: 10142, Git Pull Request custom field: `customfield_10875`, GitHub Issue custom field: `customfield_10747`
3. **Code Intelligence** -- present, tool naming convention: `mcp__<serena-instance>__<tool>`, configured instance: `serena_backend` with `rust-analyzer`

Validation passes. Proceed.

## Step 0.5 -- JIRA Access Initialization

Would attempt MCP first for all JIRA operations. If MCP fails, prompt user for REST API fallback.

## Step 1 -- Fetch and Parse Jira Task

Parsed sections from task description:

- **Repository**: trustify-backend
- **Target Branch**: main (extracted and stored for Steps 5 and 10)
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns summary with counts per severity level (Critical, High, Medium, Low) and total.
- **Files to Modify**: 3 files (advisory.rs service, endpoints/mod.rs, model/mod.rs)
- **Files to Create**: 3 files (severity_summary.rs model, severity_summary.rs endpoint, advisory_summary.rs test)
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` (NEW)
- **Implementation Notes**: present with patterns for endpoint, service, entity, error handling
- **Acceptance Criteria**: 5 criteria
- **Test Requirements**: 4 test cases
- **Target PR**: not present
- **Review Context**: not present
- **Bookend Type**: not present
- **Dependencies**: None

### Target Branch extraction

Extracted: `main`. Stored for use in Steps 5 and 10.

### GitHub Issue extraction

GitHub Issue custom field (`customfield_10747`) is configured in CLAUDE.md. Would read this field from the fetched issue. If present, parse the GitHub issue URL and store as `<owner>/<repo>#<number>` for use in the PR description's `Closes` line. If empty, skip silently.

## Step 1.5 -- Verify Description Integrity

1. **Retrieve issue comments**: call `jira.get_issue_comments(TC-9201)` to fetch all comments.
2. **Locate digest comment**: search for comments whose body starts with `[sdlc-workflow] Description digest:`. If multiple match, select the most recent by `created` timestamp.
3. **If no digest comment found**: log warning: "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced." Proceed normally.
4. **If digest comment found**:
   a. Check `created` vs `updated` timestamps -- if `updated` is later than `created`, warn: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed."
   b. Extract the tagged digest value (e.g., `sha256-md:<hex>` or `sha256-adf:<hex>`). Parse the format tag and hex digest. If legacy untagged format (`sha256:<hex>`), log warning and proceed.
   c. Write the current description to `/tmp/desc-TC-9201.txt` and compute digest via: `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
   d. Compare format tags -- if tags differ, log warning ("Digest format mismatch") and proceed.
   e. If tags match, compare hex digests -- on match proceed silently; on mismatch alert user with expected vs actual and ask whether to proceed or stop.

## Step 2 -- Verify Dependencies

Task has no dependencies ("Depends on: None"). Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Call `jira.user_info()` to get current user's account ID.
2. Call `jira.edit_issue(TC-9201, assignee=<account-id>)` to assign task.
3. Call `jira.transition_issue(TC-9201, "In Progress")` to transition status.

## Step 4 -- Understand the Code

### Code Inspection Plan

Using Serena instance `serena_backend` (from Repository Registry):

1. **Overview of files to modify**:
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/service/advisory.rs` -- understand `AdvisoryService` struct and existing methods (`fetch`, `list`, `search`)
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand current route registrations
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/mod.rs` -- understand existing model module declarations

2. **Deep reads of specific symbols**:
   - `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::fetch` -- understand method signature, parameters, return type, error handling pattern
   - `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::list` -- understand list pattern for query building
   - `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisorySummary` -- inspect `severity` field and its type
   - `mcp__serena_backend__find_symbol` with `include_body=true` on `AppError` in `common/src/error.rs` -- understand error handling pattern and `.context()` usage

3. **Backward compatibility check**:
   - `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` -- identify all callers to ensure new method doesn't conflict

4. **Non-symbolic search**:
   - `mcp__serena_backend__search_for_pattern` for `sbom_advisory` -- understand the join table structure and how SBOM-advisory relationships are queried
   - `mcp__serena_backend__search_for_pattern` for `Router::new().route` in `endpoints/mod.rs` -- confirm route registration pattern

5. **Convention conformance analysis** (sibling analysis):
   - Inspect `modules/fundamental/src/advisory/endpoints/get.rs` -- sibling endpoint handler
   - Inspect `modules/fundamental/src/advisory/endpoints/list.rs` -- sibling endpoint handler
   - Inspect `modules/fundamental/src/sbom/endpoints/get.rs` -- cross-module sibling endpoint
   - Inspect `modules/fundamental/src/advisory/model/summary.rs` -- sibling model struct
   - Inspect `modules/fundamental/src/advisory/model/details.rs` -- sibling model struct

### Documentation file identification

- `README.md` at repository root
- `CONVENTIONS.md` at repository root -- would read and extract CI check commands and code generation commands
- `docs/api.md` -- API documentation that may need updating for the new endpoint
- `docs/architecture.md` -- architecture overview

### CONVENTIONS.md lookup

Would read `CONVENTIONS.md` at repository root (`./CONVENTIONS.md` per Repository Registry path). Extract:
- CI check commands (formatting, linting, compilation)
- Code generation commands (if any)
- Naming rules, directory structure, code patterns, test conventions

### Test convention analysis

Sibling test files to inspect:
- `tests/api/advisory.rs` -- advisory endpoint integration tests
- `tests/api/sbom.rs` -- SBOM endpoint integration tests
- `tests/api/search.rs` -- search endpoint integration tests

## Step 5 -- Create Branch

Standard flow (no Target PR, no Bookend Type):

```
git checkout main
git pull
git checkout -b TC-9201
```

Branch name: `TC-9201`
Base branch: `main`

## Step 6 -- Implement Changes

### Files to Modify

1. **`modules/fundamental/src/advisory/model/mod.rs`** -- add module declaration
2. **`modules/fundamental/src/advisory/service/advisory.rs`** -- add `severity_summary` method
3. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- register new route

### Files to Create

4. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- SeveritySummary struct
5. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- GET handler
6. **`tests/api/advisory_summary.rs`** -- integration tests

Detailed changes for each file are in `file-1-description.md` through `file-6-description.md`.

### Cross-repo API contract verification

Not applicable -- this task creates a new endpoint in the same backend repository. No cross-repo REST calls.

### Code quality practices

- Every new struct, enum, and public function will have a `///` doc comment
- SeveritySummary struct: doc comment explaining it represents aggregated severity counts
- severity_summary service method: doc comment explaining parameters, return type, and behavior
- GET handler: doc comment explaining the endpoint path and expected response

### Documentation impact

- No **Documentation Updates** section in the task description.
- `docs/api.md` should be checked -- if it lists endpoints, add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint.
- Keep the update lightweight: add one entry for the new endpoint.

## Step 7 -- Write Tests

Test file: `tests/api/advisory_summary.rs`

Four test functions following sibling test conventions (details in `file-6-description.md`):
1. `test_advisory_summary_valid_sbom` -- valid SBOM with known advisories returns correct severity counts
2. `test_advisory_summary_nonexistent_sbom` -- non-existent SBOM ID returns 404
3. `test_advisory_summary_empty_sbom` -- SBOM with no advisories returns all zeros
4. `test_advisory_summary_deduplicated` -- duplicate advisory links are deduplicated in count

All tests will have `///` doc comments and given-when-then section comments.

Would run: `cargo test` and fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|-------------|
| 1 | GET /api/v2/sbom/{id}/advisory-summary returns correct JSON shape | Verified by endpoint handler returning `SeveritySummary` struct with `critical`, `high`, `medium`, `low`, `total` fields |
| 2 | Returns 404 when SBOM ID does not exist | Verified by service method returning `AppError::NotFound` with `.context()` wrapping, tested by `test_advisory_summary_nonexistent_sbom` |
| 3 | Counts only unique advisories (deduplicates by advisory ID) | Verified by using `DISTINCT` or `HashSet` deduplication in service method, tested by `test_advisory_summary_deduplicated` |
| 4 | All severity levels default to 0 when no advisories exist | Verified by `SeveritySummary::default()` or explicit zero initialization, tested by `test_advisory_summary_empty_sbom` |
| 5 | Response time under 200ms for SBOMs with up to 500 advisories | Verified by using a single aggregation query instead of N+1 fetches |

## Step 9 -- Self-Verification

### Scope containment

Run `git diff --name-only` and compare against task's Files to Modify and Files to Create:

**Expected modified files:**
- `modules/fundamental/src/advisory/service/advisory.rs`
- `modules/fundamental/src/advisory/endpoints/mod.rs`
- `modules/fundamental/src/advisory/model/mod.rs`

**Expected created files:**
- `modules/fundamental/src/advisory/model/severity_summary.rs`
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- `tests/api/advisory_summary.rs`

**Potential out-of-scope files:**
- `docs/api.md` -- if updated for documentation currency, would ask user to approve
- `tests/Cargo.toml` -- if test module registration is needed, would ask user to approve

### Untracked file check

Run `git status --short`, extract `??` entries, filter by proximity to modified directories, search for code references (e.g., `mod severity_summary;` referencing the new model file).

### Sensitive-pattern check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- expect no matches.

### Documentation currency

Check `docs/api.md` -- if it lists endpoints, add the new one. CONVENTIONS.md and README.md unlikely to need changes.

### CI checks from CONVENTIONS.md

Run all CI check commands extracted from CONVENTIONS.md. Hard stop on any failure.

### Data-flow trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param `id` via `Path<Id>` -> call `AdvisoryService::severity_summary(sbom_id, tx)` -> query `sbom_advisory` join table -> count by severity -> return `SeveritySummary` as JSON -- **COMPLETE**

### Contract & sibling parity

- `SeveritySummary` is a standalone response struct (no trait to implement) -- no contract gaps
- Sibling parity with `get.rs` handler: error handling (Result<T, AppError> with .context()), path param extraction (Path<Id>), JSON response -- all matched
- No cross-module shared entity anomalies -- query is read-only (SELECT), not modifying shared entities

### Duplication check

Search for existing severity aggregation logic in the codebase. If found, refactor to reuse.

### Cross-section reference consistency

- Entity `AdvisoryService`: Files to Modify lists `service/advisory.rs`, Implementation Notes references `service/advisory.rs` -- consistent
- Entity `SeveritySummary`: Files to Create lists `model/severity_summary.rs`, no conflicting reference -- consistent
- Entity `AdvisorySummary`: Implementation Notes references `model/summary.rs` for severity field -- consistent with model directory structure

## Step 10 -- Commit and Push

### Commit message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated vulnerability advisory severity counts (critical, high,
medium, low, total) for a given SBOM. Includes SeveritySummary
response model, AdvisoryService.severity_summary method, and
integration tests.

Implements TC-9201
```

Flag: `--trailer="Assisted-by: Claude Code"`

### Push and PR

```
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" --body "$(cat <<'EOF'
## Summary

Add a service method and REST endpoint that aggregates vulnerability advisory severity
counts for a given SBOM, enabling dashboard widgets to render severity breakdowns
without client-side counting.

- Add `GET /api/v2/sbom/{id}/advisory-summary` returning `{ critical, high, medium, low, total }`
- Add `SeveritySummary` response struct in advisory model
- Add `severity_summary` method to `AdvisoryService`
- Add integration tests for valid SBOM, non-existent SBOM (404), empty SBOM, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
EOF
)"
```

If a GitHub issue reference was extracted from `customfield_10747`, append `Closes <owner>/<repo>#<number>` to the PR body.

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (`customfield_10875`) with the PR URL in ADF format (inlineCard).
2. **Add comment** to TC-9201 with:
   - PR link
   - Summary: Added severity aggregation endpoint with SeveritySummary model, AdvisoryService.severity_summary method, route registration, and integration tests
   - Deviations: none anticipated
   - Comment ends with sdlc-workflow footnote (version read from plugin.json)
3. **Transition** TC-9201 to **In Review**.
