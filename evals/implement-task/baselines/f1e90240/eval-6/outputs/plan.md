# Implementation Plan: TC-9201

**Task:** Add advisory severity aggregation service and endpoint
**Repository:** trustify-backend
**Target Branch:** main
**Parent Feature:** TC-9001

---

## Step 0 -- Validate Project Configuration

Verify CLAUDE.md contains required sections under `# Project Configuration`:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena Instance `serena_backend` at path `./`
2. **Jira Configuration** -- present, contains Project key (TC), Cloud ID, Feature issue type ID
3. **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend` using rust-analyzer

All sections are present and valid. Proceed.

## Step 0.5 -- JIRA Access Initialization

Determine the JIRA access method. Attempt MCP first for all JIRA operations. If MCP fails, prompt the user to choose between REST API fallback, skip, or retry.

## Step 1 -- Fetch and Parse Jira Task

Fetch the issue:

```
jira.get_issue(TC-9201)
```

Parse the structured description:

| Section | Value |
|---|---|
| **Repository** | trustify-backend |
| **Target Branch** | main |
| **Description** | Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM |
| **Files to Modify** | `modules/fundamental/src/advisory/service/advisory.rs`, `modules/fundamental/src/advisory/endpoints/mod.rs`, `modules/fundamental/src/advisory/model/mod.rs` |
| **Files to Create** | `modules/fundamental/src/advisory/model/severity_summary.rs`, `modules/fundamental/src/advisory/endpoints/severity_summary.rs`, `tests/api/advisory_summary.rs` |
| **API Changes** | `GET /api/v2/sbom/{id}/advisory-summary` (NEW) |
| **Target PR** | None |
| **Bookend Type** | None |
| **Dependencies** | None |

Capture the issue `webUrl` (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for use in the PR description.

Check the GitHub Issue custom field (`customfield_10747`) -- extract if present, skip silently if empty.

## Step 1.5 -- Verify Description Integrity

(See digest-match.md for full details.)

1. Fetch comments: `jira.get_issue_comments(TC-9201)`
2. Locate digest comment: one comment matches marker `[sdlc-workflow] Description digest:`
3. Comment edit detection: `created == updated` -- comment is unmodified, no warning
4. Extract stored digest: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
5. Compute current digest: `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt` outputs `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
6. Format tags match (`sha256-md` == `sha256-md`)
7. Hex digests match -- proceed silently, no user prompt

## Step 2 -- Verify Dependencies

The task lists `Dependencies: None`. No dependency verification needed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's account ID: `jira.user_info()`
2. Assign the task: `jira.edit_issue(TC-9201, assignee=<current-user-account-id>)`
3. Transition to In Progress: `jira.transition_issue(TC-9201) -> In Progress`

## Step 4 -- Understand the Code

Use the Serena instance `serena_backend` (from Repository Registry) to inspect the codebase. Tools are called as `mcp__serena_backend__<tool>`.

Note from Code Intelligence section: rust-analyzer may take 30-60 seconds to index on first use.

### 4.1 Inspect files to modify

**`modules/fundamental/src/advisory/service/advisory.rs`** (AdvisoryService):

```
mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/service/advisory.rs")
```

- Examine the `fetch` and `list` methods to understand the pattern for the new `severity_summary` method
- Note method signatures: `&self`, parameters like `Id`, `Transactional<'_>`
- Use `mcp__serena_backend__find_symbol` with `include_body=true` on `fetch` or `list` to see the full implementation pattern

**`modules/fundamental/src/advisory/endpoints/mod.rs`** (route registration):

```
mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/endpoints/mod.rs")
```

- Understand how routes are registered via `Router::new().route("/path", get(handler))`

**`modules/fundamental/src/advisory/model/mod.rs`** (model module registration):

```
mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/model/mod.rs")
```

- See how existing model submodules are declared (`pub mod summary;`, `pub mod details;`)

### 4.2 Inspect reference files mentioned in Implementation Notes

**`modules/fundamental/src/advisory/endpoints/get.rs`** (pattern reference for new endpoint):

```
mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/endpoints/get.rs")
mcp__serena_backend__find_symbol("get handler", include_body=true)
```

- Understand Path<Id> extraction, service call, JSON response pattern

**`entity/src/sbom_advisory.rs`** (join table for SBOM-advisory link):

```
mcp__serena_backend__get_symbols_overview("entity/src/sbom_advisory.rs")
```

- Understand the join table schema for querying advisories linked to an SBOM

**`modules/fundamental/src/advisory/model/summary.rs`** (AdvisorySummary with severity field):

```
mcp__serena_backend__find_symbol("AdvisorySummary", include_body=true)
```

- Examine the `severity` field type and values

**`common/src/error.rs`** (AppError pattern):

```
mcp__serena_backend__get_symbols_overview("common/src/error.rs")
```

- Understand AppError enum and `.context()` wrapping pattern

### 4.3 Check backward compatibility

```
mcp__serena_backend__find_referencing_symbols("AdvisoryService")
```

- Identify all callers of AdvisoryService to ensure adding a new method won't break existing code (it should not, since we are only adding, not modifying)

### 4.4 Convention conformance analysis

**Sibling files for endpoint pattern:**
- `modules/fundamental/src/advisory/endpoints/get.rs`
- `modules/fundamental/src/advisory/endpoints/list.rs`
- `modules/fundamental/src/sbom/endpoints/get.rs`

Examine 2-3 siblings with `get_symbols_overview` to discover:
- Naming conventions (handler function names, route paths)
- Error handling (Result<T, AppError> with .context())
- Parameter extraction (Path<Id>)
- Response types (Json<T> vs direct struct return)
- Import organization

**Sibling files for service pattern:**
- `modules/fundamental/src/advisory/service/advisory.rs` (existing methods)
- `modules/fundamental/src/sbom/service/sbom.rs`

Examine to discover:
- Method signature patterns (verb_noun, &self, Id, Transactional)
- Query construction patterns (SeaORM)
- Error handling within service methods

**Sibling files for model pattern:**
- `modules/fundamental/src/advisory/model/summary.rs`
- `modules/fundamental/src/advisory/model/details.rs`
- `modules/fundamental/src/sbom/model/summary.rs`

Examine to discover:
- Derive macros (Serialize, Deserialize, etc.)
- Field naming and type conventions
- Documentation comment style

### 4.5 Test convention analysis

**Sibling test files:**
- `tests/api/advisory.rs`
- `tests/api/sbom.rs`
- `tests/api/search.rs`

Examine 2-3 with `get_symbols_overview` to discover:
- Assertion style (`assert_eq!(resp.status(), StatusCode::OK)`)
- Response body deserialization pattern
- 404 test coverage
- Test naming (`test_<endpoint>_<scenario>`)
- Test setup and database seeding patterns
- Whether parameterized tests (rstest) are used

### 4.6 Documentation file identification

Identify documentation files for potential update:
- `README.md` at repository root
- `docs/api.md` (API reference)
- `docs/architecture.md` (system architecture)
- `CONVENTIONS.md` at repository root

### 4.7 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). If present:
- Read it and follow its conventions throughout implementation
- Extract CI check commands (look for headings like "CI checks", "Linting", "Verification")
- Extract any code generation commands
- Record all commands for use in Step 9

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

Create the SeveritySummary response struct following the pattern from sibling model files:

```rust
use serde::{Deserialize, Serialize};

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Provides a per-severity breakdown (Critical, High, Medium, Low) and a total
/// count, enabling dashboard widgets to render severity distributions without
/// client-side counting.
#[derive(Clone, Debug, Default, Serialize, Deserialize)]
pub struct SeveritySummary {
    /// Count of advisories with Critical severity.
    pub critical: u32,
    /// Count of advisories with High severity.
    pub high: u32,
    /// Count of advisories with Medium severity.
    pub medium: u32,
    /// Count of advisories with Low severity.
    pub low: u32,
    /// Total count of unique advisories across all severity levels.
    pub total: u32,
}
```

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add the new model module registration:

```rust
pub mod severity_summary;
```

Following the existing pattern of `pub mod summary;` and `pub mod details;`.

### 6.3 Modify `modules/fundamental/src/advisory/service/advisory.rs`

Add a `severity_summary` method to AdvisoryService following the pattern of existing `fetch` and `list` methods:

```rust
/// Computes aggregated severity counts for all advisories linked to the given SBOM.
///
/// Returns a `SeveritySummary` with counts per severity level (Critical, High, Medium, Low)
/// and a total. Advisories are deduplicated by advisory ID before counting.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify SBOM exists (return 404 if not)
    // 2. Query sbom_advisory join table for advisories linked to this SBOM
    // 3. Deduplicate by advisory ID
    // 4. For each unique advisory, fetch its severity from AdvisorySummary
    // 5. Count by severity level
    // 6. Return SeveritySummary with counts and total
}
```

Key implementation details:
- Use the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) to find advisories linked to the SBOM
- Deduplicate by advisory ID to satisfy acceptance criteria
- Use the `severity` field from `AdvisorySummary` to categorize counts
- Return 404 (via AppError with `.context()`) when the SBOM ID does not exist
- Default all severity counts to 0 when no advisories exist

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern from `endpoints/get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;

/// Handler for `GET /api/v2/sbom/{id}/advisory-summary`.
///
/// Returns aggregated severity counts for all advisories linked to the specified SBOM.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: /* injected AdvisoryService */,
    tx: /* transactional context */,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to compute advisory severity summary")?;
    Ok(Json(summary))
}
```

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route in the existing router following the pattern of other route registrations:

```rust
mod severity_summary;

// In the router builder:
Router::new()
    // ... existing routes ...
    .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

### 6.6 Verify `server/src/main.rs`

Per the task description: "no changes needed (routes auto-mount via module registration)." Confirm this by inspecting the file -- the advisory module's routes should be automatically included.

### 6.7 Code quality practices

Verify all new symbols have documentation comments:
- `SeveritySummary` struct and its fields -- documented
- `severity_summary` service method -- documented
- `get_severity_summary` handler -- documented

### 6.8 Documentation impact

Check if `docs/api.md` needs updating with the new endpoint. Since a new public API endpoint is added (`GET /api/v2/sbom/{id}/advisory-summary`), update the API documentation to include:
- Endpoint path and method
- Request parameters (SBOM ID as path parameter)
- Response shape (`{ critical, high, medium, low, total }`)
- Error responses (404 for non-existent SBOM)

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with integration tests following sibling test conventions from `tests/api/advisory.rs` and `tests/api/sbom.rs`.

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that an SBOM with known linked advisories returns the correct severity breakdown.
#[tokio::test]
async fn test_advisory_summary_returns_correct_counts() {
    // Given an SBOM with advisories at known severity levels
    // (seed test database with SBOM + linked advisories: 2 Critical, 1 High, 3 Medium, 0 Low)

    // When requesting the advisory summary
    let resp = client
        .get("/api/v2/sbom/{id}/advisory-summary")
        .send()
        .await;

    // Then the response contains correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 1);
    assert_eq!(summary.medium, 3);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 6);
}
```

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom_returns_404() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    let resp = client
        .get("/api/v2/sbom/nonexistent-id/advisory-summary")
        .send()
        .await;

    // Then the response is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns zero for all severity counts.
#[tokio::test]
async fn test_advisory_summary_no_advisories_returns_zeros() {
    // Given an SBOM with no linked advisories
    // (seed test database with SBOM but no advisory links)

    // When requesting the advisory summary
    let resp = client
        .get("/api/v2/sbom/{id}/advisory-summary")
        .send()
        .await;

    // Then all counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}
```

### Test 4: Duplicate advisory links are deduplicated

```rust
/// Verifies that duplicate advisory links to the same SBOM are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisory_links() {
    // Given an SBOM with duplicate links to the same advisory
    // (seed test database with SBOM linked to advisory A twice, advisory B once; both Critical)

    // When requesting the advisory summary
    let resp = client
        .get("/api/v2/sbom/{id}/advisory-summary")
        .send()
        .await;

    // Then the count reflects unique advisories only
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 2);  // A and B, not 3
    assert_eq!(summary.total, 2);
}
```

Run tests:

```bash
cargo test --test advisory_summary
```

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` | Verified by test 1 (correct counts) and the SeveritySummary struct shape |
| Returns 404 when SBOM ID does not exist | Verified by test 2 (404 response) |
| Counts only unique advisories (deduplicates by advisory ID) | Verified by test 4 (deduplication) |
| All severity levels default to 0 when no advisories exist | Verified by test 3 (all zeros) and SeveritySummary derives Default |
| Response time under 200ms for SBOMs with up to 500 advisories | Verified by efficient query design using join table with deduplication at the database level; performance testing may require a larger dataset |

## Step 9 -- Self-Verification

### Scope containment

Run `git diff --name-only` and compare against Files to Modify and Files to Create:

**Expected modified files:**
- `modules/fundamental/src/advisory/service/advisory.rs`
- `modules/fundamental/src/advisory/endpoints/mod.rs`
- `modules/fundamental/src/advisory/model/mod.rs`

**Expected created files:**
- `modules/fundamental/src/advisory/model/severity_summary.rs`
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- `tests/api/advisory_summary.rs`

**Potentially out-of-scope (needs approval if modified):**
- `docs/api.md` -- justified by documentation impact analysis (new public API endpoint)

Flag any other modified files to the user for approval.

### Untracked file check

Run `git status --short` and check for `??` entries in directories where implementation work occurred. For each proximity-matched untracked file, search for code references before asking whether to stage.

### Sensitive-pattern check

```bash
git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
```

Flag any matches and do not proceed until resolved.

### Documentation currency

Verify `docs/api.md` covers the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. If not already updated in Step 6.8, update it now.

### Documentation scope preservation

If `docs/api.md` was modified, verify the replacement text still covers all previously documented endpoints and use cases.

### Cross-section reference consistency

Verify file paths are consistent across task description sections:

- `AdvisoryService` -- Files to Modify: `modules/fundamental/src/advisory/service/advisory.rs`, Implementation Notes: `modules/fundamental/src/advisory/service/advisory.rs` -- consistent
- Route registration -- Files to Modify: `modules/fundamental/src/advisory/endpoints/mod.rs`, Implementation Notes: `modules/fundamental/src/advisory/endpoints/mod.rs` -- consistent
- `AdvisorySummary.severity` -- Implementation Notes: `modules/fundamental/src/advisory/model/summary.rs` -- consistent

### Duplication check

Search for existing severity aggregation or summary functions:

```
mcp__serena_backend__search_for_pattern("severity_summary")
mcp__serena_backend__search_for_pattern("severity.*count")
mcp__serena_backend__search_for_pattern("advisory.*aggregate")
```

If similar logic exists, refactor to reuse it.

### CI checks from CONVENTIONS.md

Run all CI check commands extracted from CONVENTIONS.md in Step 4.7. If any fail, stop and fix before proceeding. Hard stop on any non-zero exit.

### Data-flow trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract Path<Id> -> call `AdvisoryService::severity_summary(id, tx)` -> query sbom_advisory join table -> fetch advisory severities -> aggregate counts -> return Json<SeveritySummary> -- **COMPLETE**

### Contract & sibling parity

- `SeveritySummary` -- standalone struct, no trait/interface to implement. Derives Serialize/Deserialize matching sibling model structs.
- `get_severity_summary` handler -- follows same Result<Json<T>, AppError> pattern as `get.rs` handler. Uses Path<Id> extraction, .context() error wrapping.
- `severity_summary` service method -- follows same `&self, Id, Transactional` signature as sibling methods. Uses same error handling pattern.

## Step 10 -- Commit and Push

### Commit

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
       modules/fundamental/src/advisory/model/mod.rs \
       modules/fundamental/src/advisory/service/advisory.rs \
       modules/fundamental/src/advisory/endpoints/severity_summary.rs \
       modules/fundamental/src/advisory/endpoints/mod.rs \
       tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add a service method and REST endpoint that aggregates vulnerability
advisory severity counts for a given SBOM. The endpoint returns a
summary with counts per severity level (Critical, High, Medium, Low)
and a total, enabling dashboard widgets to render severity breakdowns
without client-side counting.

Implements TC-9201"
```

If documentation was updated, also stage `docs/api.md`.

### Fork detection

```bash
git remote get-url upstream 2>/dev/null
```

- If upstream remote exists: parse `<upstream-owner/repo>` from upstream URL and `<fork-owner>` from origin URL
- If no upstream remote: use default `gh pr create` behavior

### Push and create PR

```bash
git push -u origin TC-9201
```

**If fork detected:**

```bash
gh pr create -R <upstream-owner/repo> --head <fork-owner>:TC-9201 --base main \
  --title "feat(api): add advisory severity aggregation endpoint" \
  --body "## Summary

- Add \`SeveritySummary\` response struct with per-severity counts
- Add \`severity_summary\` method to \`AdvisoryService\` using sbom_advisory join table
- Add \`GET /api/v2/sbom/{id}/advisory-summary\` endpoint
- Add integration tests for correct counts, 404, empty results, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)"
```

**If no fork detected:**

```bash
gh pr create --base main \
  --title "feat(api): add advisory severity aggregation endpoint" \
  --body "## Summary

- Add \`SeveritySummary\` response struct with per-severity counts
- Add \`severity_summary\` method to \`AdvisoryService\` using sbom_advisory join table
- Add \`GET /api/v2/sbom/{id}/advisory-summary\` endpoint
- Add integration tests for correct counts, 404, empty results, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)"
```

If a GitHub issue reference was extracted in Step 1, append a `Closes <owner>/<repo>#<number>` line to the PR description body.

## Step 11 -- Update Jira

### Set Git Pull Request custom field

Look up `customfield_10875` from Jira Configuration. Update the field with ADF containing the PR URL:

```
jira.update_issue(TC-9201, fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
```

### Add comment

Post a comment to TC-9201 with:
- PR link
- Summary of changes:
  - Created `SeveritySummary` response struct
  - Added `severity_summary` method to `AdvisoryService`
  - Added `GET /api/v2/sbom/{id}/advisory-summary` endpoint
  - Added 4 integration tests covering correct counts, 404, empty results, and deduplication
- No deviations from the plan

Include the comment footnote (read version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`):

```
---
This comment was AI-generated by [sdlc-workflow/implement-task](https://github.com/RHEcosystemAppEng/sdlc-plugins) v{version}.
```

### Transition to In Review

```
jira.transition_issue(TC-9201) -> In Review
```
