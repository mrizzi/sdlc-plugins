# Implementation Plan for TC-9201

## Task Summary
Add an advisory severity aggregation service method and REST endpoint that returns severity counts (Critical, High, Medium, Low, total) for a given SBOM.

## Pre-Implementation Steps

### Step 0 -- Validate Project Configuration
Verify CLAUDE.md contains:
- Repository Registry: trustify-backend with Serena Instance `serena_backend` at path `./` -- present.
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID -- present.
- Code Intelligence: tool naming convention `mcp__serena_backend__<tool>` -- present.

Configuration is valid. Proceed.

### Step 1 -- Fetch and Parse Jira Task
Fetch TC-9201 via `jira.get_issue("TC-9201")`. Parse structured description:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add severity aggregation service and endpoint for SBOM advisory summaries.
- **Files to Modify**: 3 files (advisory.rs service, endpoints/mod.rs, model/mod.rs)
- **Files to Create**: 3 files (severity_summary model, severity_summary endpoint, integration test)
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Implementation Notes**: Follow existing endpoint/service patterns, use sbom_advisory join table, use AdvisorySummary.severity field, return AppError with .context(), return struct directly for JSON serialization.
- **Acceptance Criteria**: 5 items (correct counts, 404 handling, deduplication, zero defaults, performance)
- **Test Requirements**: 4 items (valid counts, 404, empty SBOM, deduplication)
- **Target PR**: not present (default flow)
- **Bookend Type**: not present (default flow)
- **Dependencies**: None

Capture `webUrl` for the issue (e.g., `https://redhat.atlassian.net/browse/TC-9201`).

Extract GitHub Issue custom field (`customfield_10747`) from the fetched issue fields. If present, parse `owner/repo#number` for use in PR description.

### Step 1.5 -- Verify Description Integrity
Fetch all comments on TC-9201 via `jira.get_issue_comments("TC-9201")`.

Search for comments whose body starts with `[sdlc-workflow] Description digest:`.

**If no digest comment is found**: Log warning and proceed normally -- "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced." This is the backward-compatible behavior for tasks created before the digest protocol was introduced.

**If a digest comment is found**:
1. Check comment edit detection: compare `created` vs `updated` timestamps. Warn if edited.
2. Extract the tagged digest value (e.g., `sha256-md:a1b2...` or `sha256-adf:a1b2...`). Parse the format tag and hex digest. If legacy untagged format (`sha256:<hex>`), log warning and skip.
3. Write current description to `/tmp/desc-TC-9201.txt` and compute digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`.
4. Compare format tags: if tags differ, log "Digest format mismatch" warning and proceed.
5. Compare hex digests (when tags match): if match, proceed silently; if mismatch, alert user with expected vs actual digests and ask whether to proceed or stop.

### Step 2 -- Verify Dependencies
Dependencies: None. Proceed.

### Step 3 -- Transition to In Progress and Assign
1. Get current user via `jira.user_info()`.
2. Assign TC-9201 to current user via `jira.edit_issue("TC-9201", assignee=<account-id>)`.
3. Transition to In Progress via `jira.transition_issue("TC-9201", "In Progress")`.

### Step 4 -- Understand the Code
Use `mcp__serena_backend__get_symbols_overview` on files to modify:
- `modules/fundamental/src/advisory/service/advisory.rs` -- inspect `AdvisoryService` methods (`fetch`, `list`, `search`) and their signatures.
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- inspect route registration pattern.
- `modules/fundamental/src/advisory/model/mod.rs` -- inspect existing module declarations.

Use `mcp__serena_backend__find_symbol` with `include_body=true` on:
- `AdvisoryService::fetch` and `AdvisoryService::list` -- understand method signatures and patterns for the new `severity_summary` method.
- `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` -- understand the `severity` field type and values.
- `get` handler in `modules/fundamental/src/advisory/endpoints/get.rs` -- understand endpoint handler pattern.
- `AppError` in `common/src/error.rs` -- understand error handling pattern.
- `sbom_advisory` entity in `entity/src/sbom_advisory.rs` -- understand the join table structure.

Use `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to ensure adding a method won't break existing callers.

**Sibling analysis** (convention conformance):
- Inspect `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs` as sibling endpoint handlers.
- Inspect `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` as sibling model structs.
- Inspect `modules/fundamental/src/sbom/service/sbom.rs` as sibling service implementation.

**Test sibling analysis**:
- Inspect `tests/api/sbom.rs` and `tests/api/advisory.rs` for test patterns, assertion style, naming, and setup.

**Documentation file identification**:
- `README.md` at repo root.
- `CONVENTIONS.md` at repo root.
- `docs/api.md` and `docs/architecture.md` referenced in CLAUDE.md.

**CONVENTIONS.md lookup**: Read `./CONVENTIONS.md` for project conventions. Extract any CI check commands from a CI checks section. Extract any code generation commands.

### Step 5 -- Create Branch
```
git checkout main
git pull
git checkout -b TC-9201
```

Target branch is `main` (from task description). No Target PR, no Bookend Type -- use default flow.

## Files to Modify

### 1. `modules/fundamental/src/advisory/model/mod.rs`
Add `pub mod severity_summary;` to register the new model module alongside existing `pub mod summary;` and `pub mod details;`.

### 2. `modules/fundamental/src/advisory/service/advisory.rs`
Add a `severity_summary` method to `AdvisoryService`:
- Signature: `pub async fn severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<SeveritySummary, AppError>`
- Query the `sbom_advisory` join table to find all advisories linked to the given SBOM.
- Deduplicate by advisory ID (use `DISTINCT` or equivalent).
- For each linked advisory, retrieve the `AdvisorySummary` and extract the `severity` field.
- Count occurrences per severity level (Critical, High, Medium, Low).
- Return a `SeveritySummary` struct with counts and total.
- Error handling: return 404 via `AppError` with `.context()` if the SBOM does not exist.

### 3. `modules/fundamental/src/advisory/endpoints/mod.rs`
Register the new route:
- Add `mod severity_summary;` to import the new handler module.
- Add `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))` to the router following the existing `Router::new().route(...)` pattern.

## Files to Create

### 4. `modules/fundamental/src/advisory/model/severity_summary.rs`
Create the `SeveritySummary` response struct:
- Derive `Serialize`, `Deserialize`, `Debug`, `Clone`, `Default`.
- Fields: `critical: u32`, `high: u32`, `medium: u32`, `low: u32`, `total: u32`.
- Add doc comment explaining the struct's purpose.

### 5. `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
Create the GET handler:
- `pub async fn get_severity_summary(Path(id): Path<Id>, service: ...) -> Result<Json<SeveritySummary>, AppError>`
- Extract the SBOM ID from path params via `Path<Id>`.
- Call `service.severity_summary(id, &tx).await.context("Failed to fetch advisory severity summary")?`.
- Return `Ok(Json(summary))`.
- Add doc comment on the handler function.

### 6. `tests/api/advisory_summary.rs`
Create integration tests:
- `test_advisory_summary_valid_sbom` -- create test SBOM with known advisories at different severity levels, call GET endpoint, assert correct counts per severity and total.
- `test_advisory_summary_not_found` -- call GET with a non-existent SBOM ID, assert 404 status.
- `test_advisory_summary_empty` -- create test SBOM with no advisories, call GET, assert all counts are 0 and total is 0.
- `test_advisory_summary_deduplication` -- create test SBOM with duplicate advisory links, call GET, assert counts reflect unique advisories only.
- Each test function has a `///` doc comment explaining what it verifies.
- Non-trivial tests include `// Given`, `// When`, `// Then` section comments.

## Post-Implementation Steps

### Step 8 -- Verify Acceptance Criteria
- GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }` -- verified by `test_advisory_summary_valid_sbom`.
- Returns 404 for non-existent SBOM -- verified by `test_advisory_summary_not_found`.
- Counts only unique advisories -- verified by `test_advisory_summary_deduplication`.
- All severity levels default to 0 -- verified by `test_advisory_summary_empty`.
- Response time under 200ms for up to 500 advisories -- verified by query design using database-level aggregation with deduplication.

### Step 9 -- Self-Verification
- **Scope containment**: `git diff --name-only` must list only the 6 files above plus `tests/api/mod.rs` if it needs a `mod advisory_summary;` declaration.
- **Untracked file check**: Check `git status --short` for `??` entries in proximity directories.
- **Sensitive-pattern check**: Scan staged diff for secrets/credentials.
- **Documentation currency**: Check if `docs/api.md` needs updating for the new endpoint; if so, add a brief entry for `GET /api/v2/sbom/{id}/advisory-summary`.
- **Duplication check**: Search for existing severity aggregation logic in the codebase.
- **CI checks**: Run commands from CONVENTIONS.md CI checks section. Hard stop on any failure.
- **Data-flow trace**: `GET request` -> `Path<Id> extraction` -> `AdvisoryService::severity_summary` -> `sbom_advisory join query` -> `severity counting` -> `SeveritySummary struct` -> `Json response` -- COMPLETE.
- **Contract & sibling parity**: `SeveritySummary` follows the model pattern from siblings; `get_severity_summary` handler follows the endpoint pattern; service method follows the service pattern.

### Step 10 -- Commit and Push
```
git add modules/fundamental/src/advisory/model/mod.rs
git add modules/fundamental/src/advisory/model/severity_summary.rs
git add modules/fundamental/src/advisory/service/advisory.rs
git add modules/fundamental/src/advisory/endpoints/mod.rs
git add modules/fundamental/src/advisory/endpoints/severity_summary.rs
git add tests/api/advisory_summary.rs
```

Commit message:
```
git commit --trailer='Assisted-by: Claude Code' -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, AdvisoryService
method, and integration tests.

Implements TC-9201"
```

Push and create PR:
```
git push -u origin TC-9201
gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "..."
```

PR description includes:
- Summary of changes
- `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)`
- `Closes <owner>/<repo>#<number>` if GitHub Issue custom field was present

### Step 11 -- Update Jira
1. Update `customfield_10875` (Git Pull Request custom field) with the PR URL in ADF format.
2. Add comment to TC-9201 with PR link and summary of changes (with skill footnote).
3. Transition TC-9201 to In Review.
