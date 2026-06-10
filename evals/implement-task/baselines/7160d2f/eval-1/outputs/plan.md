# Implementation Plan for TC-9201

## Task Summary

Add an advisory severity aggregation service method and REST endpoint that returns severity counts (Critical, High, Medium, Low, total) for a given SBOM, enabling dashboard widgets to render severity breakdowns.

## Step-by-Step Execution Plan

### Step 0 -- Validate Project Configuration

Read CLAUDE.md and verify all required sections exist:
- Repository Registry: present (trustify-backend, serena_backend, path `./`)
- Jira Configuration: present (Project key TC, Cloud ID, Feature issue type ID, Git Pull Request custom field customfield_10875, GitHub Issue custom field customfield_10747)
- Code Intelligence: present (serena_backend with rust-analyzer)

Result: Configuration valid. Proceed.

### Step 0.5 -- JIRA Access Initialization

Would attempt MCP first for all Jira operations. If MCP fails, would prompt user for REST API fallback.

### Step 1 -- Fetch and Parse Jira Task

Would call `jira.get_issue(TC-9201)` and parse the structured description.

Parsed fields:
- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add service method and REST endpoint for advisory severity aggregation
- **Files to Modify**: 3 files (advisory.rs service, endpoints/mod.rs, model/mod.rs)
- **Files to Create**: 3 files (severity_summary.rs model, severity_summary.rs endpoint, advisory_summary.rs test)
- **API Changes**: GET /api/v2/sbom/{id}/advisory-summary (NEW)
- **Implementation Notes**: follow existing patterns, use sbom_advisory join table, use AdvisorySummary severity field
- **Acceptance Criteria**: 5 criteria
- **Test Requirements**: 4 test cases
- **Target PR**: none
- **Bookend Type**: none
- **Dependencies**: none

Would also capture the issue's `webUrl` (e.g., `https://redhat.atlassian.net/browse/TC-9201`).

GitHub Issue custom field (customfield_10747): would check the field value on the fetched issue. If populated, parse the GitHub issue URL for use in PR description.

### Step 1.5 -- Verify Description Integrity

Would call `jira.get_issue_comments(TC-9201)` and search for comments starting with `[sdlc-workflow] Description digest:`.

- If no digest comment found: log warning "No description digest found -- skipping integrity check."
- If digest comment found:
  - Check if `created` != `updated` timestamps (warn if edited)
  - Extract tagged digest (e.g., `sha256-md:a1b2...`)
  - If legacy untagged format: log warning and skip
  - Write description to `/tmp/desc-TC-9201.txt` and compute digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
  - Compare format tags; if mismatch, log warning and skip
  - If tags match, compare hex digests; if mismatch, alert user and stop for confirmation

### Step 2 -- Verify Dependencies

Task has no dependencies. Skip.

### Step 3 -- Transition to In Progress and Assign

1. Call `jira.user_info()` to get current user's account ID
2. Call `jira.edit_issue(TC-9201, assignee=<account-id>)` to assign
3. Call `jira.transition_issue(TC-9201)` to transition to In Progress

### Step 4 -- Understand the Code

Would use `mcp__serena_backend__<tool>` for all code inspection.

#### Code inspection actions:
1. `get_symbols_overview` on `modules/fundamental/src/advisory/service/advisory.rs` -- understand AdvisoryService methods (fetch, list, search)
2. `get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand route registration pattern
3. `get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/get.rs` -- understand endpoint handler pattern (Path<Id> extraction, service call, JSON return)
4. `get_symbols_overview` on `modules/fundamental/src/advisory/model/mod.rs` -- understand model module registration
5. `get_symbols_overview` on `modules/fundamental/src/advisory/model/summary.rs` -- understand AdvisorySummary struct and its severity field
6. `find_symbol` with `include_body=true` on `AdvisoryService::fetch` -- read the fetch method body to follow the pattern
7. `find_symbol` with `include_body=true` on `AdvisoryService::list` -- read the list method body to follow the pattern
8. `get_symbols_overview` on `entity/src/sbom_advisory.rs` -- understand the SBOM-Advisory join table structure
9. `find_symbol` on `AppError` in `common/src/error.rs` -- understand error handling pattern
10. `find_referencing_symbols` on any symbols we plan to modify to check backward compatibility

#### Sibling analysis for convention conformance:
- Siblings of `advisory/endpoints/severity_summary.rs`: `advisory/endpoints/get.rs`, `advisory/endpoints/list.rs`, `sbom/endpoints/get.rs`
- Siblings of `advisory/model/severity_summary.rs`: `advisory/model/summary.rs`, `advisory/model/details.rs`
- Siblings of `advisory/service/advisory.rs`: `sbom/service/sbom.rs`

#### Test sibling analysis:
- Siblings of `tests/api/advisory_summary.rs`: `tests/api/advisory.rs`, `tests/api/sbom.rs`, `tests/api/search.rs`

#### CONVENTIONS.md lookup:
- Would read `./CONVENTIONS.md` via serena_backend or direct Read
- Extract CI check commands (e.g., `cargo fmt --check`, `cargo clippy`, `cargo test`)
- Extract code generation commands if any

#### Documentation files identified:
- `docs/api.md` -- REST API reference, will need updating for new endpoint
- `README.md`, `docs/architecture.md` -- review for relevance

### Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```
git checkout main
git pull
git checkout -b TC-9201
```

### Step 6 -- Implement Changes

#### Files to Create

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- SeveritySummary response struct
2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- GET handler for /api/v2/sbom/{id}/advisory-summary

#### Files to Modify

3. **`modules/fundamental/src/advisory/model/mod.rs`** -- add `pub mod severity_summary;`
4. **`modules/fundamental/src/advisory/service/advisory.rs`** -- add `severity_summary` method
5. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- register the new route

#### Files to Create (Tests)

6. **`tests/api/advisory_summary.rs`** -- integration tests

#### Documentation Updates

7. **`docs/api.md`** -- add documentation for the new endpoint (if the file documents endpoints)

### Step 7 -- Write Tests

See file-6-description.md for test implementation details. Would run `cargo test` after writing tests and fix any failures.

### Step 8 -- Verify Acceptance Criteria

1. GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }` -- verified by endpoint implementation and test
2. Returns 404 when SBOM ID does not exist -- verified by 404 test case
3. Counts only unique advisories (deduplicates by advisory ID) -- verified by deduplication logic in service method and dedup test
4. All severity levels default to 0 when no advisories exist -- verified by zero-advisory test case
5. Response time under 200ms for SBOMs with up to 500 advisories -- verified by efficient query (single DB query with GROUP BY)

### Step 9 -- Self-Verification

#### Scope containment
- `git diff --name-only` should show only the files listed in Files to Modify and Files to Create
- If `docs/api.md` was modified, flag as out-of-scope and ask user to approve (documentation update is justified by new endpoint)

#### Untracked file check
- `git status --short` to find `??` entries
- Check proximity to modified directories
- Search for code references to any untracked files

#### Sensitive-pattern check
- `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'`
- Expect no matches

#### Documentation currency
- Verify `docs/api.md` covers the new endpoint (if not already updated in Step 6)

#### Cross-section reference consistency
- Entity `AdvisoryService`: referenced in Files to Modify as `modules/fundamental/src/advisory/service/advisory.rs` and in Implementation Notes as `modules/fundamental/src/advisory/service/advisory.rs` -- CONSISTENT
- Entity `AdvisorySummary`: referenced in Implementation Notes as `modules/fundamental/src/advisory/model/summary.rs` -- not being modified, only read for reference -- OK
- Entity `sbom_advisory`: referenced in Implementation Notes as `entity/src/sbom_advisory.rs` -- not being modified, only used as join table -- OK

#### Duplication check
- Search for existing severity aggregation/counting logic in the codebase
- Search for similar function names (`severity_summary`, `severity_count`, `aggregate_severity`)

#### CI checks from CONVENTIONS.md
- Run all CI check commands extracted from CONVENTIONS.md (e.g., `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo test`)
- Hard stop on any failure

#### Data-flow trace
- `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param (Id) -> call AdvisoryService::severity_summary(sbom_id, tx) -> query sbom_advisory join table -> join with advisory table -> group by severity -> count per level -> build SeveritySummary struct -> return Json(summary) -- COMPLETE

#### Contract & sibling parity
- SeveritySummary struct: no trait/interface contract to implement (new standalone struct with Serialize/Deserialize)
- Endpoint handler: follows same pattern as `get.rs` siblings (Path<Id>, service call, Json response)
- Service method: follows same pattern as `fetch`/`list` siblings (&self, id, tx params, Result return type)
- Error handling: uses AppError with .context() like all siblings

#### Caller-site parity
- No existing callers of the new code (it is a new endpoint) -- skip

### Step 10 -- Commit and Push

#### Commit message:

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, service method,
endpoint handler, and integration tests.

Implements TC-9201
```

With `--trailer="Assisted-by: Claude Code"`.

#### Branch and PR:

```
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" --body "..."
```

PR description would include:
- `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)`
- Summary of changes
- If GitHub issue reference was found, append `Closes <owner>/<repo>#<number>`

### Step 11 -- Update Jira

1. Update Git Pull Request custom field (customfield_10875) with PR URL in ADF format:
   ```
   jira.update_issue(TC-9201, fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
   ```

2. Add comment to TC-9201 with:
   - PR link
   - Summary of changes (new endpoint, model, service method, tests)
   - No deviations from plan
   - Comment footer with sdlc-workflow/implement-task version and link

3. Transition TC-9201 to In Review:
   ```
   jira.transition_issue(TC-9201) -> In Review
   ```

## Files Summary

| # | File | Action | Description |
|---|---|---|---|
| 1 | modules/fundamental/src/advisory/model/severity_summary.rs | CREATE | SeveritySummary response struct |
| 2 | modules/fundamental/src/advisory/endpoints/severity_summary.rs | CREATE | GET handler for /api/v2/sbom/{id}/advisory-summary |
| 3 | modules/fundamental/src/advisory/model/mod.rs | MODIFY | Register severity_summary module |
| 4 | modules/fundamental/src/advisory/service/advisory.rs | MODIFY | Add severity_summary method |
| 5 | modules/fundamental/src/advisory/endpoints/mod.rs | MODIFY | Register new route |
| 6 | tests/api/advisory_summary.rs | CREATE | Integration tests |
| 7 | docs/api.md | MODIFY | Document new endpoint (if applicable) |
