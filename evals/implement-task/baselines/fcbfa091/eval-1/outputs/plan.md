# Implementation Plan for TC-9201

## Task Summary

**Jira Issue**: TC-9201 -- Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Branch Name**: TC-9201
**Status**: To Do
**Parent**: is incorporated by TC-9001
**Dependencies**: None

## Step 0 -- Validate Project Configuration

CLAUDE.md validated. All required sections present:
- Repository Registry: trustify-backend with Serena instance `serena_backend` at path `./`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID all present
- Code Intelligence: Tool naming convention documented (`mcp__serena_backend__<tool>`)

## Step 1 -- Fetch and Parse Jira Task

Parsed sections from TC-9201 task description:
- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add service method and REST endpoint for advisory severity aggregation per SBOM
- **Files to Modify**: 3 files (advisory service, endpoints mod, model mod)
- **Files to Create**: 3 files (severity_summary model, severity_summary endpoint, integration tests)
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` (new)
- **Implementation Notes**: Follow existing endpoint/service patterns, use sbom_advisory join table
- **Acceptance Criteria**: 5 criteria
- **Test Requirements**: 4 test cases
- **Bookend Type**: not present (standard flow)
- **Target PR**: not present (standard flow)
- **Dependencies**: None

GitHub Issue custom field (`customfield_10747`): would check but not present in this mock.

## Step 1.5 -- Verify Description Integrity

Would retrieve issue comments via `jira.get_issue_comments(TC-9201)` and search for
comments starting with `[sdlc-workflow] Description digest:`.

**Result**: No description digest found -- skipping integrity check. This task may have
been created before digest tracking was introduced.

Proceeding with warning rather than blocking execution, per the digest protocol.

## Step 2 -- Verify Dependencies

Task has no dependencies. Proceeding.

## Step 3 -- Transition to In Progress and Assign

Would execute:
1. `jira.user_info()` to get current user's account ID
2. `jira.edit_issue(TC-9201, assignee=<account-id>)` to assign task
3. `jira.transition_issue(TC-9201)` to In Progress

## Step 4 -- Understand the Code

### Code inspection plan

Using Serena instance `serena_backend` (from Repository Registry):

1. **Overview of files to modify**:
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/service/advisory.rs` to see existing `AdvisoryService` methods (`fetch`, `list`, `search`)
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/mod.rs` to see route registration pattern
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/mod.rs` to see existing module declarations

2. **Read specific symbols**:
   - `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::fetch` to understand service method signature and pattern
   - `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisorySummary` to see the `severity` field used for counting

3. **Check backward compatibility**:
   - `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to ensure the new method does not break existing callers

4. **Non-symbolic search**:
   - `mcp__serena_backend__search_for_pattern` for `sbom_advisory` to understand the join table structure
   - `mcp__serena_backend__search_for_pattern` for `Router::new().route` in the advisory endpoints to see route registration pattern

5. **Sibling analysis** (convention conformance):
   - `mcp__serena_backend__get_symbols_overview` on `sbom/endpoints/get.rs` and `sbom/endpoints/list.rs` to compare handler patterns
   - `mcp__serena_backend__get_symbols_overview` on `sbom/service/sbom.rs` to compare service method patterns
   - `mcp__serena_backend__get_symbols_overview` on `advisory/model/summary.rs` to see existing model struct patterns

6. **Test sibling analysis**:
   - `mcp__serena_backend__get_symbols_overview` on `tests/api/sbom.rs` and `tests/api/advisory.rs` to see test structure, assertions, and naming

7. **CONVENTIONS.md lookup**: Read `CONVENTIONS.md` at repository root for explicit project conventions and CI check commands

8. **Documentation file identification**:
   - `docs/api.md` -- REST API reference, may need updating for new endpoint
   - `docs/architecture.md` -- System architecture, unlikely to need changes
   - `README.md` -- General overview, unlikely to need changes

### Cross-section reference consistency

Verified file path references across task description sections:
- `AdvisoryService` referenced in both Files to Modify (`service/advisory.rs`) and Implementation Notes (`service/advisory.rs`) -- **consistent**
- `AdvisorySummary` referenced in Implementation Notes (`model/summary.rs`) -- existing file, not being modified, used as reference -- **consistent**
- Endpoint registration referenced in both Files to Modify (`endpoints/mod.rs`) and Implementation Notes (`endpoints/mod.rs`) -- **consistent**

No cross-section reference mismatches detected.

## Step 5 -- Create Branch

Standard flow (no Target PR, no Bookend Type):

```
git checkout main
git pull
git checkout -b TC-9201
```

Branch name `TC-9201` derived from the Jira issue ID. Base branch is `main` (from Target Branch).

## Step 6 -- Implement Changes

### Files to Modify (3 files)

1. **`modules/fundamental/src/advisory/model/mod.rs`** -- Add module declaration
2. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Add `severity_summary` method
3. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Register new route

### Files to Create (3 files)

4. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- SeveritySummary response struct
5. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- GET handler
6. **`tests/api/advisory_summary.rs`** -- Integration tests

See `file-1-description.md` through `file-6-description.md` for detailed changes per file.

### Documentation impact

- `docs/api.md` may need updating to document the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- No changes to architecture docs or README needed

## Step 7 -- Write Tests

Tests implemented in `tests/api/advisory_summary.rs` (see `file-6-description.md`):
1. `test_advisory_summary_valid_sbom` -- valid SBOM with known advisories returns correct severity counts
2. `test_advisory_summary_not_found` -- non-existent SBOM ID returns 404
3. `test_advisory_summary_empty` -- SBOM with no advisories returns all zeros
4. `test_advisory_summary_deduplication` -- duplicate advisory links are deduplicated

All tests follow sibling conventions: `assert_eq!` on status codes, body deserialization, specific field validation.

Would run: `cargo test` and fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|-------------|
| 1 | GET /api/v2/sbom/{id}/advisory-summary returns severity counts | Endpoint implemented with correct response shape, verified by test_advisory_summary_valid_sbom |
| 2 | Returns 404 for non-existent SBOM ID | 404 handling implemented using existing pattern, verified by test_advisory_summary_not_found |
| 3 | Counts only unique advisories (deduplicates by advisory ID) | Query uses DISTINCT or HashSet deduplication, verified by test_advisory_summary_deduplication |
| 4 | All severity levels default to 0 | SeveritySummary struct initialized with all zeros, verified by test_advisory_summary_empty |
| 5 | Response time under 200ms for up to 500 advisories | Single query with join, no N+1; performance validated by database-level efficiency |

## Step 9 -- Self-Verification

### Scope containment
- `git diff --name-only` would show exactly the 6 files listed in Files to Modify and Files to Create
- No out-of-scope files modified

### Untracked file check
- Check `git status --short` for `??` entries in directories with modified files
- No unexpected untracked files expected

### Sensitive-pattern check
- `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'`
- No secrets expected in these changes

### Documentation currency
- `docs/api.md` should be updated with the new endpoint documentation if it lists endpoints

### Duplication check
- Search repository for existing severity aggregation or advisory counting logic
- Verify no existing utility provides this functionality before finalizing

### Data-flow trace
- `GET /api/v2/sbom/{id}/advisory-summary`:
  - Input: HTTP request with SBOM ID path parameter -- **connected**
  - Processing: `severity_summary` endpoint handler calls `AdvisoryService::severity_summary(sbom_id, tx)` -- **connected**
  - Database: service queries `sbom_advisory` join table, fetches linked advisories, counts by severity -- **connected**
  - Output: `SeveritySummary` struct serialized as JSON response -- **connected**
  - **COMPLETE**

### Contract & sibling parity
- `SeveritySummary` is a standalone response struct, does not implement an existing trait -- no contract gaps
- Sibling parity with `AdvisoryDetails`, `SbomDetails` handlers: error handling pattern matches, response serialization matches
- No cross-module shared entity concerns (read-only query, no inserts/updates)

### CI checks from CONVENTIONS.md
- Would run all CI check commands extracted from `CONVENTIONS.md`
- Would run `cargo fmt --check`, `cargo clippy`, `cargo build`, `cargo test` (or whatever is specified)

## Step 10 -- Commit and Push

### Commit message

```
git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary that returns counts of
advisories by severity level (critical, high, medium, low) for a
given SBOM. Includes AdvisoryService.severity_summary method,
SeveritySummary response model, and integration tests.

Implements TC-9201"
```

### Push and PR

```
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "## Summary

Add a service method and REST endpoint that aggregates vulnerability advisory severity
counts for a given SBOM, enabling dashboard widgets to render severity breakdowns.

- Add `GET /api/v2/sbom/{id}/advisory-summary` returning `{ critical, high, medium, low, total }`
- Add `AdvisoryService::severity_summary` method using sbom_advisory join table
- Add `SeveritySummary` response model
- Add integration tests for valid SBOM, 404, empty, and deduplication cases

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)"
```

The `--base main` flag is explicitly specified to target the correct branch (extracted from Target Branch).

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field** (`customfield_10875`) on TC-9201 with the PR URL in ADF format (inlineCard)
2. **Add comment** to TC-9201 with:
   - PR link
   - Summary: Added severity aggregation endpoint, service method, response model, and integration tests
   - No deviations from plan
   - Comment ends with the sdlc-workflow/implement-task footer (version read from plugin.json)
3. **Transition** TC-9201 to In Review
