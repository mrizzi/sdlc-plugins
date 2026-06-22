# Implementation Plan for TC-9201

## Task Summary

**Jira Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Branch to Create**: TC-9201
**Status**: To Do
**Parent Feature**: TC-9001 (is incorporated by)
**Dependencies**: None

## Step 0 -- Validate Project Configuration

Verify CLAUDE.md contains the required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present, contains Project key (TC), Cloud ID, Feature issue type ID
3. **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend` using rust-analyzer

All sections verified. Proceed.

## Step 0.5 -- JIRA Access Initialization

Would attempt MCP first for all Jira operations. If MCP fails, prompt user for REST API fallback per the defined protocol. (Not executed in this eval -- documented only.)

## Step 1 -- Fetch and Parse Jira Task

Parsed sections from TC-9201:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns summary with counts per severity level (Critical, High, Medium, Low) and total.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`
  - `server/src/main.rs` -- no changes needed
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Implementation Notes**: Follow existing patterns in `get.rs`, `advisory.rs` service, use `sbom_advisory` join table, `AdvisorySummary.severity` field, `AppError` with `.context()`, direct struct return with Axum `Json`
- **Acceptance Criteria**: 5 criteria (correct response shape, 404 for missing SBOM, deduplication, zero defaults, performance)
- **Test Requirements**: 4 tests (valid SBOM, non-existent SBOM, empty SBOM, deduplication)
- **Target PR**: not present (default flow)
- **Bookend Type**: not present (default flow)
- **Review Context**: not present
- **Dependencies**: None

**GitHub Issue extraction**: GitHub Issue custom field is `customfield_10747`. Would read this field from the Jira API response. If present, parse the GitHub issue URL and store as `<owner>/<repo>#<number>` for PR description. (Not executed in eval.)

**webUrl**: Would capture from API response, e.g. `https://redhat.atlassian.net/browse/TC-9201`

## Step 1.5 -- Verify Description Integrity

1. Would fetch issue comments via `jira.get_issue_comments(TC-9201)`
2. Would search for comments starting with `[sdlc-workflow] Description digest:`
3. The `shared/description-digest-protocol.md` file does not exist in the current plugin structure. **No digest comment found**: log warning and proceed:

> "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced."

Proceed with implementation without blocking.

## Step 2 -- Verify Dependencies

Task has no dependencies. Proceed.

## Step 3 -- Transition to In Progress and Assign

Would execute:
1. `jira.user_info()` to get current user account ID
2. `jira.edit_issue(TC-9201, assignee=<account-id>)` to assign
3. `jira.transition_issue(TC-9201) -> In Progress`

(Not executed in eval.)

## Step 4 -- Understand the Code

### Code inspection plan

Using Serena instance `serena_backend` (from Repository Registry):

1. **Overview of files to modify**:
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/service/advisory.rs` -- understand AdvisoryService structure, existing methods (fetch, list, search)
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand route registration pattern
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/mod.rs` -- understand module registration

2. **Read specific symbols**:
   - `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::fetch` -- understand method signature and pattern for `severity_summary`
   - `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::list` -- understand list/query patterns
   - `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisorySummary` in `model/summary.rs` -- understand the severity field structure

3. **Check backward compatibility**:
   - `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` -- identify all callers to ensure new method does not break existing usage

4. **Non-symbolic search**:
   - `mcp__serena_backend__search_for_pattern` for `sbom_advisory` -- find the join table entity and how it is queried
   - `mcp__serena_backend__search_for_pattern` for `Router::new().route` in advisory endpoints -- understand route registration syntax

5. **Sibling analysis** (convention conformance -- see Step 4 conventions below)

### Documentation file identification

- `README.md` at repository root
- `CONVENTIONS.md` at repository root
- `docs/api.md` -- API reference (related to new endpoint)
- `docs/architecture.md` -- system architecture overview

### CONVENTIONS.md lookup

Would read `./CONVENTIONS.md` from repository root. Extract any CI check commands and code generation commands for use in Step 9.

### Convention conformance analysis

See `outputs/conventions.md` for full details.

### Test convention analysis

See `outputs/conventions.md` for test convention details.

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### Files to Create

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- SeveritySummary response struct
   - See `outputs/file-1-description.md`

2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- GET handler
   - See `outputs/file-2-description.md`

3. **`tests/api/advisory_summary.rs`** -- integration tests
   - See `outputs/file-5-description.md`

### Files to Modify

4. **`modules/fundamental/src/advisory/model/mod.rs`** -- register new model module
   - See `outputs/file-3-description.md`

5. **`modules/fundamental/src/advisory/service/advisory.rs`** -- add severity_summary method
   - See `outputs/file-4-description.md`

6. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- register new route
   - See `outputs/file-6-description.md`

### No changes needed

- `server/src/main.rs` -- routes auto-mount via module registration, no changes needed

## Step 7 -- Write Tests

Integration tests in `tests/api/advisory_summary.rs` -- see `outputs/file-5-description.md`.

Would run `cargo test` to verify all tests pass.

## Step 8 -- Verify Acceptance Criteria

1. GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }` -- verified by response struct shape and endpoint handler
2. Returns 404 when SBOM ID does not exist -- verified by SBOM existence check in service method
3. Counts only unique advisories -- verified by deduplication via HashSet in service method
4. All severity levels default to 0 -- verified by struct defaults (u32 defaults to 0)
5. Response time under 200ms for SBOMs with up to 500 advisories -- single query with join, no N+1

## Step 9 -- Self-Verification

### Scope containment
- Run `git diff --name-only` and compare against Files to Modify and Files to Create
- Expected modified/created files:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` (create)
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (create)
  - `tests/api/advisory_summary.rs` (create)
  - `modules/fundamental/src/advisory/model/mod.rs` (modify)
  - `modules/fundamental/src/advisory/service/advisory.rs` (modify)
  - `modules/fundamental/src/advisory/endpoints/mod.rs` (modify)
- If any out-of-scope file appears (e.g., `tests/Cargo.toml` may need a new test module), flag and ask user

### Untracked file check
- Run `git status --short`, look for `??` entries in directories with modified files
- Flag any untracked files in `modules/fundamental/src/advisory/` or `tests/api/` for review

### Sensitive-pattern check
- Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'`
- No sensitive patterns expected in this implementation

### Documentation currency
- If `docs/api.md` exists and documents advisory endpoints, it should be updated to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- If it does not cover individual endpoints, skip

### CI checks from CONVENTIONS.md
- Run any CI check commands extracted from CONVENTIONS.md
- If none found, fall back to `cargo build` and `cargo clippy` to check for warnings

### Data-flow trace
- `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param `id` -> call `AdvisoryService::severity_summary(id, tx)` -> query `sbom_advisory` join table -> count by severity level -> return `SeveritySummary` as JSON -- **COMPLETE**

### Contract & sibling parity
- `SeveritySummary` implements `Serialize` (required for JSON response) -- verified
- Sibling parity with `get.rs` endpoint: error handling (AppError with .context()), path extraction (Path<Id>), service invocation pattern -- all matched
- No cross-module shared entity concerns (read-only query, no inserts/updates)

### Cross-section reference consistency
- Entity `AdvisoryService` -- Files to Modify says `service/advisory.rs`, Implementation Notes says `service/advisory.rs` -- consistent
- Entity `AdvisorySummary` -- Implementation Notes references `model/summary.rs` for the existing struct; new struct `SeveritySummary` goes in `model/severity_summary.rs` -- consistent (different entities, different files)
- Entity route registration -- Files to Modify says `endpoints/mod.rs`, Implementation Notes says `endpoints/mod.rs` -- consistent

## Step 10 -- Commit and Push

### Commit message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated severity counts (critical, high, medium, low, total)
for advisories linked to a given SBOM. Includes SeveritySummary
model, AdvisoryService::severity_summary method, and integration
tests.

Implements TC-9201
```

### Commit command

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      tests/api/advisory_summary.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs

git commit --trailer='Assisted-by: Claude Code' -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated severity counts (critical, high, medium, low, total)
for advisories linked to a given SBOM. Includes SeveritySummary
model, AdvisoryService::severity_summary method, and integration
tests.

Implements TC-9201"
```

### Push and create PR

```bash
git push -u origin TC-9201

gh pr create --base main --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" --body "## Summary

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns aggregated severity counts (critical, high, medium, low, total) for advisories linked to a given SBOM.

- SeveritySummary response model with critical/high/medium/low/total fields
- AdvisoryService::severity_summary method using sbom_advisory join table with deduplication
- GET handler with Path<Id> extraction and AppError handling
- Integration tests covering valid SBOM, missing SBOM (404), empty advisories, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)"
```

(If GitHub Issue custom field contained a value, would append `Closes <owner>/<repo>#<number>` to PR body.)

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field** (`customfield_10875`) with PR URL in ADF format:
   ```
   jira.update_issue(TC-9201, fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
   ```

2. **Add comment** to TC-9201 with:
   - PR link
   - Summary: Added SeveritySummary model, severity_summary service method, GET endpoint at /api/v2/sbom/{id}/advisory-summary, and integration tests
   - No deviations from plan
   - Comment ends with the required footnote (horizontal rule + AI-generated attribution with plugin version)

3. **Transition**: `jira.transition_issue(TC-9201) -> In Review`
