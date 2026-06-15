# Implementation Plan for TC-9201

## Task Summary
**Jira Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Status**: To Do
**Repository**: trustify-backend
**Target Branch**: main
**Labels**: ai-generated-jira
**Linked Issues**: is incorporated by TC-9001

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md contains all required sections:
1. **Repository Registry** -- present, contains `trustify-backend` with Serena Instance `serena_backend` and Path `./`
2. **Jira Configuration** -- present with Project key (TC), Cloud ID, Feature issue type ID, Git Pull Request custom field (customfield_10875), GitHub Issue custom field (customfield_10747)
3. **Code Intelligence** -- present with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend` (rust-analyzer)

Configuration is valid. Proceeding.

## Step 1 -- Fetch and Parse Jira Task

### Parsed Sections

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. The endpoint returns a summary with counts per severity level (Critical, High, Medium, Low) and a total, enabling dashboard widgets to render severity breakdowns without client-side counting.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method to AdvisoryService
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;` to register the new model module
  - `server/src/main.rs` -- no changes needed (routes auto-mount via module registration)
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler for /api/v2/sbom/{id}/advisory-summary
  - `tests/api/advisory_summary.rs` -- integration tests for the new endpoint
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }`
- **Implementation Notes**: Follow existing endpoint pattern in `get.rs`; add `severity_summary` method to AdvisoryService following `fetch`/`list` pattern; use `sbom_advisory` join table; use `AdvisorySummary.severity` field for counting; register route in `endpoints/mod.rs`; return `AppError` with `.context()` wrapping; return struct directly (Axum's `Json` extractor handles serialization)
- **Acceptance Criteria**: 5 criteria covering response format, 404 handling, deduplication, zero defaults, and performance
- **Test Requirements**: 4 test cases covering valid counts, 404, empty SBOM, and deduplication
- **Target PR**: Not present (standard flow -- will create new branch and PR)
- **Bookend Type**: Not present (standard implementation task)
- **Dependencies**: None

### Target Branch Extraction
Target branch: `main`

### GitHub Issue Extraction
GitHub Issue custom field is `customfield_10747` per Jira Configuration. Would check the fetched issue's fields for this custom field value. (Not available in this eval context.)

### Task webUrl
Would be captured from the API response (e.g., `https://redhat.atlassian.net/browse/TC-9201`).

## Step 1.5 -- Verify Description Integrity (Description Digest Protocol)

Per the description-digest-protocol:
1. Retrieve issue comments via `jira.get_issue_comments(TC-9201)`
2. Search for comments whose body starts with `[sdlc-workflow] Description digest:`
3. If multiple matching comments exist, select the most recent one by `created` timestamp
4. If no digest comment found: log warning "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced." and proceed
5. If digest comment found:
   a. Check `created` vs `updated` timestamps for comment edit detection
   b. Extract the tagged digest value (e.g., `sha256-md:<hex>` or `sha256-adf:<hex>`)
   c. If legacy untagged format (`sha256:<hex>`), log warning and skip integrity check
   d. Write description to temp file and compute digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
   e. Compare format tags -- if they differ, log warning about format mismatch and skip
   f. If tags match, compare hex digests -- match proceeds silently, mismatch alerts user

## Step 2 -- Verify Dependencies
Dependencies: None. Proceeding.

## Step 3 -- Transition to In Progress and Assign
1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign task via `jira.edit_issue(TC-9201, assignee=<account-id>)`
3. Transition to In Progress via `jira.transition_issue(TC-9201, "In Progress")`

## Step 4 -- Understand the Code

### Code Inspection Plan

Using Serena instance `serena_backend` (tools called as `mcp__serena_backend__<tool>`):

1. **Inspect files to modify**:
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/service/advisory.rs` to see AdvisoryService structure and existing methods (`fetch`, `list`, `search`)
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/mod.rs` to see route registration pattern
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/mod.rs` to see model module structure

2. **Read specific symbols**:
   - `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::fetch` to understand the method signature pattern
   - `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::list` to see list method pattern
   - `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisorySummary` struct in `model/summary.rs` to see the `severity` field type

3. **Check backward compatibility**:
   - `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to identify all callers

4. **Non-symbolic search**:
   - `mcp__serena_backend__search_for_pattern` for `sbom_advisory` to find the join table usage patterns
   - `mcp__serena_backend__search_for_pattern` for `Router::new().route` in endpoints to see route registration

5. **Convention conformance analysis** (siblings):
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/sbom/endpoints/get.rs` (sibling endpoint handler)
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/sbom/service/sbom.rs` (sibling service)
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/sbom/model/summary.rs` (sibling model)

6. **Test convention analysis** (sibling tests):
   - `mcp__serena_backend__get_symbols_overview` on `tests/api/sbom.rs` (sibling test file)
   - `mcp__serena_backend__get_symbols_overview` on `tests/api/advisory.rs` (sibling test file)

7. **CONVENTIONS.md lookup**:
   - Read `./CONVENTIONS.md` at the repository root
   - Extract any CI check commands for Step 9 verification
   - Extract any code generation commands

8. **Documentation file identification**:
   - Check `docs/api.md` for API documentation that may need updating
   - Check `README.md` at the root
   - Check `docs/architecture.md` for architectural documentation

### Cross-section Reference Consistency Check

Checking for entity-to-file-path consistency across task description sections:

- **AdvisoryService**: referenced in Files to Modify (`modules/fundamental/src/advisory/service/advisory.rs`) and in Implementation Notes (`modules/fundamental/src/advisory/service/advisory.rs`) -- CONSISTENT
- **SeveritySummary model**: referenced in Files to Create (`modules/fundamental/src/advisory/model/severity_summary.rs`) -- single reference, no conflict
- **AdvisorySummary struct**: referenced in Implementation Notes (`modules/fundamental/src/advisory/model/summary.rs`) -- this is a read-only reference for understanding the severity field, not a file being modified -- CONSISTENT
- **Route registration**: Files to Modify (`modules/fundamental/src/advisory/endpoints/mod.rs`) and Implementation Notes (`modules/fundamental/src/advisory/endpoints/mod.rs`) -- CONSISTENT
- **sbom_advisory join table**: Implementation Notes (`entity/src/sbom_advisory.rs`) -- single reference, no conflict
- **Endpoint pattern reference**: Implementation Notes (`modules/fundamental/src/advisory/endpoints/get.rs`) -- reference for pattern, not modified -- CONSISTENT
- **Error handling reference**: Implementation Notes (`common/src/error.rs`) -- reference for pattern, not modified -- CONSISTENT

All cross-section references are consistent. No mismatches detected.

## Step 5 -- Create Branch

Standard flow (no Target PR, no Bookend Type):

```
git checkout main
git pull
git checkout -b TC-9201
```

Branch name: `TC-9201`

## Step 6 -- Implement Changes

### Files to Create

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- SeveritySummary response struct
2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- GET handler
3. **`tests/api/advisory_summary.rs`** -- integration tests

### Files to Modify

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- add `severity_summary` method
2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- register new route
3. **`modules/fundamental/src/advisory/model/mod.rs`** -- add `pub mod severity_summary;`

### Files NOT Modified (confirmed by task)
- `server/src/main.rs` -- no changes needed (routes auto-mount via module registration)

See individual `file-N-description.md` files for detailed changes per file.

## Step 7 -- Write Tests

Tests are detailed in `file-6-description.md` (tests/api/advisory_summary.rs).

Would run: `cargo test` and fix any failures.

## Step 8 -- Verify Acceptance Criteria

1. GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }` -- verified by response struct shape and endpoint implementation
2. Returns 404 when SBOM ID does not exist -- verified by error handling with AppError and 404 test
3. Counts only unique advisories (deduplicates by advisory ID) -- verified by using HashSet or DISTINCT in query
4. All severity levels default to 0 when no advisories exist at that level -- verified by SeveritySummary::default() initialization
5. Response time under 200ms for SBOMs with up to 500 advisories -- verified by using efficient SQL query with GROUP BY

## Step 9 -- Self-Verification

### Scope Containment
Run `git diff --name-only` and compare against Files to Modify and Files to Create:
- `modules/fundamental/src/advisory/model/severity_summary.rs` -- in Files to Create
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- in Files to Create
- `tests/api/advisory_summary.rs` -- in Files to Create
- `modules/fundamental/src/advisory/service/advisory.rs` -- in Files to Modify
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- in Files to Modify
- `modules/fundamental/src/advisory/model/mod.rs` -- in Files to Modify

All files in scope.

### Untracked File Check
Check `git status --short` for `??` entries in directories where implementation occurred.

### Sensitive Pattern Check
Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- expecting no matches.

### Documentation Currency
Check `docs/api.md` -- new endpoint GET /api/v2/sbom/{id}/advisory-summary should be documented if the API docs list endpoints.

### Data-flow Trace
- `GET /api/v2/sbom/{id}/advisory-summary` -> extract Path<Id> -> call `AdvisoryService::severity_summary(sbom_id, tx)` -> query sbom_advisory join table -> aggregate by severity -> return SeveritySummary JSON -- COMPLETE

### Contract & Sibling Parity
- SeveritySummary: new struct, no trait contract to implement (it's a response DTO with Serialize)
- AdvisoryService::severity_summary: follows same pattern as `fetch` and `list` methods (takes `&self`, domain ID, `&Transactional<'_>`, returns `Result<T, AppError>`)
- Endpoint handler: follows same pattern as `get.rs` (extract Path<Id>, call service, return Json)
- Error handling: uses `.context()` wrapping matching all sibling handlers

### Duplication Check
Search for existing severity aggregation logic -- none expected to exist per task description.

### CI Checks from CONVENTIONS.md
Run all CI check commands extracted from CONVENTIONS.md.

## Step 10 -- Commit and Push

### Commit Message

```
feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to an SBOM.
Includes SeveritySummary model, AdvisoryService.severity_summary method,
and integration tests.

Implements TC-9201
```

With trailer: `--trailer="Assisted-by: Claude Code"`

### Push and PR

```
git push -u origin TC-9201
gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "..."
```

PR description would include:
- Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
- Summary of changes
- If GitHub issue reference was extracted, append `Closes <owner>/<repo>#<number>`

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (`customfield_10875`) with PR URL using ADF format (inlineCard)
2. **Add comment** with PR link, summary of changes, and any deviations
3. **Transition** to In Review via `jira.transition_issue(TC-9201, "In Review")`
