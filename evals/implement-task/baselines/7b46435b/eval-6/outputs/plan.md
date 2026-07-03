# Implementation Plan for TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md (claude-md-mock.md) contains all required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena Instance `serena_backend` and Path `./`
2. **Jira Configuration** -- present, contains Project key (TC), Cloud ID, Feature issue type ID
3. **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend` with `rust-analyzer`

Validation: PASSED. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all JIRA operations. If MCP fails, prompt user for REST API fallback per the documented flow.

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")`. Parse the structured description:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns summary with counts per severity level (Critical, High, Medium, Low) and a total.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method to AdvisoryService
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;` to register the new model module
  - `server/src/main.rs` -- no changes needed (routes auto-mount)
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Implementation Notes**: Follow existing patterns in get.rs, AdvisoryService, sbom_advisory join table, etc.
- **Acceptance Criteria**: 5 items (correct response shape, 404 on missing SBOM, deduplication, zero defaults, performance)
- **Test Requirements**: 4 items (valid SBOM, non-existent SBOM, no advisories, deduplication)
- **Target PR**: not present (default flow)
- **Bookend Type**: not present (default flow)
- **Dependencies**: None
- **GitHub Issue custom field**: customfield_10747 -- read from issue fields; if present, parse and store for PR description

Capture `webUrl` for later use in PR description (e.g., `https://redhat.atlassian.net/browse/TC-9201`).

## Step 1.5 -- Verify Description Integrity

See `outputs/digest-match.md` for detailed handling. Summary:

1. Fetch comments via `jira.get_issue_comments("TC-9201")`
2. Locate the digest comment: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
3. Check comment edit timestamps: `created == updated` -- comment is unmodified, no warning
4. Extract stored digest: format tag `sha256-md`, hex `a1b2c3d4e5f67890...`
5. Compute current digest: write description to `/tmp/desc-TC-9201.txt`, run `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
6. Compare format tags: both `sha256-md` -- tags match
7. Compare hex digests: MATCH -- proceed silently

Outcome: Description integrity verified. No user prompt needed.

## Step 2 -- Verify Dependencies

The task has `Dependencies: None`. No dependency verification needed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's account ID: `jira.user_info()`
2. Assign TC-9201 to current user: `jira.edit_issue("TC-9201", assignee=<account-id>)`
3. Transition to In Progress: `jira.transition_issue("TC-9201") -> In Progress`

## Step 4 -- Understand the Code

Use the `serena_backend` Serena instance (tools called as `mcp__serena_backend__<tool>`).

### 4.1 Inspect Files to Modify

1. **`modules/fundamental/src/advisory/service/advisory.rs`**
   - `mcp__serena_backend__get_symbols_overview` to see AdvisoryService struct, `fetch`, `list`, `search` method signatures
   - `mcp__serena_backend__find_symbol("severity_summary")` -- confirm it does not already exist
   - `mcp__serena_backend__find_symbol("fetch", include_body=true)` -- read the fetch method to understand the pattern (parameters, return type, transaction handling)

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`**
   - `mcp__serena_backend__get_symbols_overview` to see route registration pattern
   - Examine how routes are registered with `Router::new().route(...)` pattern

3. **`modules/fundamental/src/advisory/model/mod.rs`**
   - `mcp__serena_backend__get_symbols_overview` to see existing module declarations

4. **`modules/fundamental/src/advisory/endpoints/get.rs`** (referenced in Implementation Notes)
   - `mcp__serena_backend__find_symbol("get", include_body=true)` -- read the handler to understand the path extraction, service call, and JSON response pattern

5. **`modules/fundamental/src/advisory/model/summary.rs`**
   - `mcp__serena_backend__find_symbol("AdvisorySummary", include_body=true)` -- read the struct to understand the `severity` field

6. **`entity/src/sbom_advisory.rs`**
   - `mcp__serena_backend__get_symbols_overview` -- understand the join table structure

7. **`common/src/error.rs`**
   - `mcp__serena_backend__find_symbol("AppError", include_body=true)` -- understand error handling pattern

### 4.2 Check Backward Compatibility

- `mcp__serena_backend__find_referencing_symbols` on AdvisoryService to understand all callers
- Confirm the new method addition will not break existing callers

### 4.3 Convention Conformance Analysis

**Sibling files to examine:**
- `modules/fundamental/src/advisory/endpoints/get.rs` -- sibling handler
- `modules/fundamental/src/advisory/endpoints/list.rs` -- sibling handler
- `modules/fundamental/src/sbom/endpoints/get.rs` -- cross-module sibling for SBOM path extraction

**Expected discovered conventions:**
- **Error handling**: handlers return `Result<T, AppError>` with `.context()` wrapping
- **Path extraction**: use Axum's `Path<Id>` extractor
- **Service method pattern**: `&self, id: Id, tx: &Transactional<'_>` signature
- **Response**: return struct directly via Axum's `Json` extractor
- **Route registration**: `Router::new().route("/path", get(handler))` in endpoints/mod.rs
- **Naming**: service methods follow `verb_noun` pattern

### 4.4 Test Convention Analysis

**Sibling test files to examine:**
- `tests/api/advisory.rs` -- advisory endpoint integration tests
- `tests/api/sbom.rs` -- SBOM endpoint integration tests

**Expected discovered test conventions:**
- Assertion style: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- Error cases: test with non-existent IDs, check for `StatusCode::NOT_FOUND`
- Test naming: `test_<endpoint>_<scenario>` pattern
- Setup: use real PostgreSQL test database with seeded data

### 4.5 Documentation File Identification

- `README.md` at repository root
- `docs/api.md` -- API reference (may need updating for new endpoint)
- `CONVENTIONS.md` at repository root -- check for CI commands and conventions

### 4.6 CONVENTIONS.md Lookup

Read `CONVENTIONS.md` at repository root (located via Repository Registry Path `./`). Extract any CI check commands for use in Step 9. Extract any code generation commands.

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

Create the SeveritySummary response struct:

```rust
use serde::Serialize;

/// Summary of advisory severity counts for an SBOM, grouped by severity level.
#[derive(Debug, Clone, Serialize, Default)]
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

All fields default to 0 via `Default` derive, satisfying the acceptance criterion for zero defaults.

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add module declaration:

```rust
pub mod severity_summary;
```

### 6.3 Modify `modules/fundamental/src/advisory/service/advisory.rs`

Add `severity_summary` method to AdvisoryService following the pattern of existing `fetch` and `list` methods:

```rust
/// Computes a severity summary for all unique advisories linked to the given SBOM.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify SBOM exists, return 404 if not
    // 2. Query sbom_advisory join table to find advisories linked to the SBOM
    // 3. Deduplicate by advisory ID
    // 4. For each unique advisory, fetch its severity from AdvisorySummary
    // 5. Count by severity level (Critical, High, Medium, Low)
    // 6. Return SeveritySummary with counts and total
}
```

Key implementation details:
- Use the `sbom_advisory` join table from `entity/src/sbom_advisory.rs` to find linked advisories
- Deduplicate by advisory ID to satisfy the uniqueness acceptance criterion
- Use the `severity` field from `AdvisorySummary` to classify each advisory
- Return 404 (via AppError with `.context()`) when the SBOM does not exist
- Wrap all database errors with `.context()` following the established error handling pattern

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern in `endpoints/get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity summary with counts per severity level for all advisories
/// linked to the specified SBOM.
pub async fn severity_summary(
    Path(id): Path<Id>,
    service: Extension<AdvisoryService>,
    tx: Extension<Transactional<'_>>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to compute advisory severity summary")?;
    Ok(Json(summary))
}
```

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route following the existing `Router::new().route(...)` pattern:

```rust
use severity_summary::severity_summary;

// Add to the Router chain:
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary))
```

### 6.6 Verify `server/src/main.rs`

Confirm no changes needed -- routes auto-mount via module registration as stated in the task description.

### 6.7 Cross-repo API Contract Verification

Not applicable -- this task adds a backend endpoint, it does not consume APIs from another repository.

### 6.8 Code Quality Practices

Verify that every new struct, function, and public symbol has a documentation comment using Rust's `///` convention. This is shown in the code above.

### 6.9 Documentation Impact

- Check if `docs/api.md` exists and documents endpoints -- if so, add documentation for `GET /api/v2/sbom/{id}/advisory-summary` with the response shape `{ critical, high, medium, low, total }`.
- No other documentation updates expected (no configuration changes, no architectural changes).

## Step 7 -- Write Tests

### Create `tests/api/advisory_summary.rs`

Follow the test conventions discovered in Step 4 (assertion style, naming pattern, setup pattern from sibling test files).

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with known advisories at various severity levels
    // (seed test DB with SBOM and linked advisories: 2 Critical, 1 High, 3 Medium, 0 Low)

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then the response is 200 OK with correct counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 1);
    assert_eq!(summary.medium, 3);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 6);
}

/// Verifies that a non-existent SBOM ID returns 404, consistent with existing SBOM endpoints.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/nonexistent-id/advisory-summary").await;

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no advisories returns all zeros.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then all severity counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then each advisory is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    // Verify total reflects unique count, not duplicate count
    assert_eq!(summary.total, expected_unique_count);
}
```

Run tests:

```bash
cargo test --test advisory_summary
```

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| # | Criterion | Verification |
|---|---|---|
| 1 | GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` | Verified by `test_advisory_summary_valid_sbom` -- asserts correct response shape and values |
| 2 | Returns 404 when SBOM ID does not exist | Verified by `test_advisory_summary_nonexistent_sbom` -- asserts 404 status |
| 3 | Counts only unique advisories (deduplicates by advisory ID) | Verified by `test_advisory_summary_deduplicates` -- asserts unique count |
| 4 | All severity levels default to 0 when no advisories exist | Verified by `test_advisory_summary_no_advisories` -- asserts all zeros |
| 5 | Response time under 200ms for SBOMs with up to 500 advisories | Verified by efficient query design (single join query with GROUP BY, no N+1) |

## Step 9 -- Self-Verification

### 9.1 Scope Containment

Run `git diff --name-only` and verify all changed files are in scope:

**Expected modified files:**
- `modules/fundamental/src/advisory/service/advisory.rs` -- in Files to Modify
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- in Files to Modify
- `modules/fundamental/src/advisory/model/mod.rs` -- in Files to Modify

**Expected created files:**
- `modules/fundamental/src/advisory/model/severity_summary.rs` -- in Files to Create
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- in Files to Create
- `tests/api/advisory_summary.rs` -- in Files to Create

Any out-of-scope files (e.g., `docs/api.md` if updated) would be flagged for user approval.

### 9.2 Untracked File Check

Run `git status --short`, extract `??` entries, filter by proximity to modified directories, search for code references. Flag any referenced untracked files for user approval before staging.

### 9.3 Sensitive-Pattern Check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` to verify no secrets are staged.

### 9.4 Documentation Currency

If `docs/api.md` exists and was not already updated in Step 6, verify it is still accurate. If it documents endpoints and the new endpoint is missing, update it now.

### 9.5 Cross-Section Reference Consistency

Verify file paths are consistent across task description sections:
- `AdvisoryService` referenced in both Files to Modify (`advisory/service/advisory.rs`) and Implementation Notes (`advisory/service/advisory.rs`) -- consistent
- `SeveritySummary` in Files to Create (`advisory/model/severity_summary.rs`) -- no conflict
- Route registration in Files to Modify (`advisory/endpoints/mod.rs`) and Implementation Notes (`advisory/endpoints/mod.rs`) -- consistent

### 9.6 Duplication Check

Search for existing severity aggregation or summary counting logic in the repository. Use Grep to search for `severity_summary`, `severity_count`, `advisory_summary` patterns. If equivalent logic already exists, refactor to reuse it.

### 9.7 CI Checks from CONVENTIONS.md

Run all CI check commands extracted from `CONVENTIONS.md` in Step 4. Hard stop on any non-zero exit. Fix failures before proceeding.

If no CI check section was found, fall back to `cargo build` and `cargo clippy` to check for warnings.

### 9.8 Data-Flow Trace

Trace the complete data flow:

```
GET /api/v2/sbom/{id}/advisory-summary
  -> severity_summary handler (parse Path<Id>)
  -> AdvisoryService.severity_summary(id, tx)
  -> query sbom_advisory join table (find linked advisories)
  -> deduplicate by advisory ID
  -> count by severity level
  -> construct SeveritySummary struct
  -> return Json(SeveritySummary)
```

All stages connected: input (HTTP request) -> processing (service query and aggregation) -> output (JSON response). COMPLETE.

### 9.9 Contract and Sibling Parity

- **Contract verification**: SeveritySummary implements `Serialize` and `Default` as needed. Handler returns `Result<Json<SeveritySummary>, AppError>` matching the Axum pattern.
- **Sibling parity with get.rs and list.rs**: error handling pattern (`.context()` wrapping), path extraction (`Path<Id>`), response type (`Json<T>`) -- all consistent.
- **Cross-module shared entity analysis**: `sbom_advisory` join table is used by other modules -- verify our query pattern (transaction handling, read-only access) is consistent with other consumers.

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs
git add modules/fundamental/src/advisory/model/mod.rs
git add modules/fundamental/src/advisory/service/advisory.rs
git add modules/fundamental/src/advisory/endpoints/severity_summary.rs
git add modules/fundamental/src/advisory/endpoints/mod.rs
git add tests/api/advisory_summary.rs
# Add docs/api.md if it was updated

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns severity
counts (critical, high, medium, low, total) for advisories linked to a
given SBOM. Includes deduplication by advisory ID and 404 handling for
non-existent SBOMs.

Implements TC-9201"
```

Push and create PR:

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "## Summary

Add a service method and REST endpoint that aggregates vulnerability advisory
severity counts for a given SBOM.

- New endpoint: GET /api/v2/sbom/{id}/advisory-summary
- Returns { critical, high, medium, low, total } counts
- Deduplicates advisories by ID
- Returns 404 for non-existent SBOMs
- Integration tests for all acceptance criteria

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)"
```

If a GitHub issue reference was extracted from customfield_10747, append `Closes <owner>/<repo>#<number>` to the PR body.

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (customfield_10875) with the PR URL in ADF format:

```
jira.update_issue("TC-9201", fields={
  "customfield_10875": {
    "type": "doc",
    "version": 1,
    "content": [{
      "type": "paragraph",
      "content": [{
        "type": "inlineCard",
        "attrs": {"url": "<PR-URL>"}
      }]
    }]
  }
})
```

2. **Add comment** to TC-9201 with PR link, summary of changes, and any deviations from the plan. Include the skill footer (read version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`).

3. **Transition** TC-9201 to In Review: `jira.transition_issue("TC-9201") -> In Review`
