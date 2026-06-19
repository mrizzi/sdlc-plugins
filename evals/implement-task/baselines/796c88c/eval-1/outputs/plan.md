# Implementation Plan — TC-9201: Add advisory severity aggregation service and endpoint

## Task Summary

**Jira ID:** TC-9201
**Repository:** trustify-backend
**Target Branch:** main
**Branch Name:** TC-9201
**Summary:** Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM, returning counts per severity level (Critical, High, Medium, Low) and a total.

## Step 0 — Validate Project Configuration

Verify the project's CLAUDE.md contains:
1. `## Repository Registry` — present, with `trustify-backend` mapped to Serena instance `serena_backend` at path `./`
2. `## Jira Configuration` — present, with Project key `TC`, Cloud ID, Feature issue type ID `10142`, Git Pull Request custom field `customfield_10875`, GitHub Issue custom field `customfield_10747`
3. `## Code Intelligence` — present, with tool naming convention `mcp__<serena-instance>__<tool>` and `serena_backend` configured with `rust-analyzer`

All sections are present and valid. Proceed.

## Step 1 — Fetch and Parse Jira Task

Fetch TC-9201 from Jira using `jira.get_issue("TC-9201")`. Parse the structured description:

- **Repository:** trustify-backend
- **Target Branch:** main (extracted for use in branch creation and PR base)
- **Description:** Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM
- **Files to Modify:**
  - `modules/fundamental/src/advisory/service/advisory.rs` — add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` — register the new route
  - `modules/fundamental/src/advisory/model/mod.rs` — add `pub mod severity_summary;`
  - `server/src/main.rs` — no changes needed (auto-mount)
- **Files to Create:**
  - `modules/fundamental/src/advisory/model/severity_summary.rs` — SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` — GET handler
  - `tests/api/advisory_summary.rs` — integration tests
- **API Changes:** `GET /api/v2/sbom/{id}/advisory-summary` — NEW
- **Implementation Notes:** Follow existing patterns in `get.rs`, `advisory.rs` service, use `sbom_advisory` join table, use `AdvisorySummary.severity` field, return `AppError` with `.context()`, return struct directly with Axum `Json`
- **Acceptance Criteria:** 5 criteria (see task)
- **Test Requirements:** 4 test cases
- **Dependencies:** None
- **Bookend Type:** Not present (standard flow)
- **Target PR:** Not present (standard flow)

Capture the issue `webUrl` (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for use in PR description.

Check GitHub Issue custom field (`customfield_10747`) on the fetched issue. If a GitHub issue URL is present, parse and store the reference for use in PR description.

## Step 1.5 — Verify Description Integrity (Description Digest Check)

1. Retrieve issue comments: `jira.get_issue_comments("TC-9201")`
2. Search for comments starting with `[sdlc-workflow] Description digest:`
3. If multiple digest comments found, select the most recent by `created` timestamp
4. If no digest comment found: log warning "No description digest found — skipping integrity check. This task may have been created before digest tracking was introduced." and proceed
5. If digest comment found:
   a. Check comment `created` vs `updated` timestamps for edit detection
   b. Extract tagged digest value (e.g., `sha256-md:a1b2...` or `sha256-adf:a1b2...`)
   c. If legacy untagged format (`sha256:<hex>`), log warning and skip
   d. Write description to `/tmp/desc-TC-9201.txt` and compute digest: `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
   e. Compare format tags; if mismatch, log warning and skip
   f. If tags match, compare hex digests; if mismatch, alert user and stop for confirmation

## Step 2 — Verify Dependencies

No dependencies listed. Proceed.

## Step 3 — Transition to In Progress and Assign

1. `jira.user_info()` — get current user's account ID
2. `jira.edit_issue("TC-9201", assignee=<account-id>)` — assign to self
3. `jira.transition_issue("TC-9201")` → In Progress

## Step 4 — Understand the Code

### 4.1 Inspect Files to Modify

Use `mcp__serena_backend__get_symbols_overview` on each file to understand structure:

- **`modules/fundamental/src/advisory/service/advisory.rs`** — inspect `AdvisoryService` struct and its existing methods (`fetch`, `list`, `search`) to understand the method signature pattern, particularly how `&self`, `Id`, and `Transactional` parameters are used
- **`modules/fundamental/src/advisory/endpoints/mod.rs`** — inspect route registration pattern (`Router::new().route(...)`) to understand how to add new routes
- **`modules/fundamental/src/advisory/model/mod.rs`** — inspect existing `pub mod` declarations to follow the same pattern for adding `pub mod severity_summary;`

Use `mcp__serena_backend__find_symbol` with `include_body=true` on:
- `AdvisoryService::fetch` — understand the method signature and error handling pattern
- `AdvisoryService::list` — understand alternative method pattern
- The route registration in `endpoints/mod.rs` — understand `Router::new().route("/path", get(handler))` pattern

Use `mcp__serena_backend__find_referencing_symbols` on:
- `AdvisoryService` — identify all callers to ensure new method won't break existing ones

### 4.2 Inspect Sibling Files (Convention Conformance Analysis)

**Sibling endpoint files:**
- `modules/fundamental/src/advisory/endpoints/get.rs` — primary pattern reference for the new endpoint
- `modules/fundamental/src/advisory/endpoints/list.rs` — secondary pattern reference
- `modules/fundamental/src/sbom/endpoints/get.rs` — cross-module endpoint pattern

**Sibling model files:**
- `modules/fundamental/src/advisory/model/summary.rs` — AdvisorySummary struct (has `severity` field to use)
- `modules/fundamental/src/advisory/model/details.rs` — AdvisoryDetails struct pattern
- `modules/fundamental/src/sbom/model/summary.rs` — cross-module model pattern

**Sibling service files:**
- `modules/fundamental/src/advisory/service/advisory.rs` — same file being modified, inspect existing methods

### 4.3 Inspect Entity Layer

- `entity/src/sbom_advisory.rs` — understand the SBOM-Advisory join table structure for querying advisories linked to an SBOM

### 4.4 Inspect Error Handling

- `common/src/error.rs` — understand `AppError` enum and `IntoResponse` implementation

### 4.5 CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). If present, read and extract:
- Coding conventions for implementation
- CI check commands for Step 9 verification
- Code generation commands

### 4.6 Documentation File Identification

- `README.md` at repository root
- `docs/api.md` — API reference documentation
- `docs/architecture.md` — system architecture

### 4.7 Test Convention Analysis

**Sibling test files:**
- `tests/api/advisory.rs` — primary pattern reference for advisory endpoint tests
- `tests/api/sbom.rs` — secondary pattern reference for SBOM-related tests
- `tests/api/search.rs` — cross-module test pattern

Inspect for: assertion style, response validation, error case coverage, test naming, setup/teardown, parameterized test usage.

## Step 5 — Create Branch

```bash
git checkout main
git pull
git checkout -b TC-9201
```

Branch name: `TC-9201` (matches Jira issue ID per convention).

## Step 6 — Implement Changes

### Files to Create

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** — SeveritySummary response struct
2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** — GET handler for `/api/v2/sbom/{id}/advisory-summary`

### Files to Modify

3. **`modules/fundamental/src/advisory/model/mod.rs`** — add `pub mod severity_summary;`
4. **`modules/fundamental/src/advisory/service/advisory.rs`** — add `severity_summary` method
5. **`modules/fundamental/src/advisory/endpoints/mod.rs`** — register the new route

### Files to Create (Tests)

6. **`tests/api/advisory_summary.rs`** — integration tests

(See individual file descriptions in `outputs/file-N-description.md` for detailed changes.)

## Step 7 — Write Tests

Implement the 4 test cases described in Test Requirements in `tests/api/advisory_summary.rs`. Follow test conventions discovered from sibling test files. Run:

```bash
cargo test
```

Fix any failures before proceeding.

## Step 8 — Verify Acceptance Criteria

Walk through each criterion:
- [ ] GET /api/v2/sbom/{id}/advisory-summary returns correct JSON shape
- [ ] Returns 404 when SBOM ID does not exist
- [ ] Counts only unique advisories (deduplicates by advisory ID)
- [ ] All severity levels default to 0
- [ ] Response time under 200ms for SBOMs with up to 500 advisories

## Step 9 — Self-Verification

### Scope containment
Run `git diff --name-only` and compare against Files to Modify and Files to Create. Flag any out-of-scope files.

### Untracked file check
Run `git status --short`, filter for `??` entries in directories with modified files, search for code references.

### Sensitive-pattern check
Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'`

### Documentation currency
Check if `docs/api.md` needs updating to document the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

### CI checks from CONVENTIONS.md
Run any CI check commands extracted from CONVENTIONS.md in Step 4.5.

### Data-flow trace
- `GET /api/v2/sbom/{id}/advisory-summary` → extract path param (`Path<Id>`) ✓ → call `AdvisoryService::severity_summary(sbom_id, tx)` ✓ → query `sbom_advisory` join table ✓ → aggregate by severity ✓ → return `SeveritySummary` as JSON ✓ — COMPLETE

### Contract & sibling parity
- Verify `SeveritySummary` struct implements `Serialize` (required for Axum JSON response)
- Verify endpoint handler returns `Result<Json<SeveritySummary>, AppError>` matching sibling pattern
- Verify service method signature follows `(&self, sbom_id: Id, tx: &Transactional<'_>)` pattern

### Duplication check
Search for existing severity aggregation logic to avoid duplicating.

### Cross-section reference consistency
Verify file paths are consistent across Files to Modify, Files to Create, and Implementation Notes sections.

## Step 10 — Commit and Push

### Commit message

```
feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to an SBOM.
Includes SeveritySummary model, AdvisoryService::severity_summary method,
and integration tests.

Implements TC-9201
```

### Commit command

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      tests/api/advisory_summary.rs
git commit --trailer='Assisted-by: Claude Code' -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to an SBOM.
Includes SeveritySummary model, AdvisoryService::severity_summary method,
and integration tests.

Implements TC-9201"
```

### Push and create PR

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "## Summary
- Add GET /api/v2/sbom/{id}/advisory-summary endpoint returning severity counts per level
- Add SeveritySummary response model with critical, high, medium, low, total fields
- Add AdvisoryService::severity_summary method using sbom_advisory join table
- Add integration tests for the new endpoint

## Jira
Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
"
```

If a GitHub issue reference was extracted in Step 1, append `Closes <owner>/<repo>#<number>` to the PR body.

## Step 11 — Update Jira

1. Update Git Pull Request custom field (`customfield_10875`) with PR URL in ADF format:
   ```
   jira.update_issue("TC-9201", fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
   ```
2. Add comment to TC-9201 with PR link, summary of changes, and any deviations (with skill footnote)
3. Transition: `jira.transition_issue("TC-9201")` → In Review
