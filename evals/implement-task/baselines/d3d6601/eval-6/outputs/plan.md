# Implementation Plan for TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Task Summary

**Jira Issue:** TC-9201
**Repository:** trustify-backend
**Target Branch:** main
**Branch Name:** TC-9201
**Parent Feature:** TC-9001 (linked via "is incorporated by")

Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. The endpoint returns a summary with counts per severity level (Critical, High, Medium, Low) and a total.

## Step 0 -- Validate Project Configuration

Verify CLAUDE.md contains:
- **Repository Registry**: Present -- trustify-backend is registered with Serena instance `serena_backend` at path `./`
- **Jira Configuration**: Present -- Project key TC, Cloud ID, Feature issue type ID, Git Pull Request custom field (customfield_10875), GitHub Issue custom field (customfield_10747)
- **Code Intelligence**: Present -- tool naming convention `mcp__serena_backend__<tool>`, rust-analyzer language server

All sections are complete. Proceed.

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue(TC-9201)` and parse the structured description:

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Add severity aggregation service and endpoint for SBOM advisory summaries |
| Files to Modify | 3 files (advisory.rs service, endpoints/mod.rs, model/mod.rs) |
| Files to Create | 3 files (severity_summary.rs model, severity_summary.rs endpoint, advisory_summary.rs test) |
| API Changes | GET /api/v2/sbom/{id}/advisory-summary (NEW) |
| Target PR | Not present |
| Bookend Type | Not present |
| Dependencies | None |

Capture the issue's webUrl (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for use in PR description.

Check GitHub Issue custom field (customfield_10747) -- extract if present for PR description `Closes` line.

## Step 1.5 -- Verify Description Integrity

1. Fetch comments via `jira.get_issue_comments(TC-9201)`
2. Locate comment with marker `[sdlc-workflow] Description digest:` -- found one comment with body: `[sdlc-workflow] Description digest: sha256:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
3. Check comment timestamps: `created` == `updated` -- comment was not edited, no warning needed
4. Extract stored digest: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
5. Compute current digest using `python3 scripts/sha256-digest.py` on the description field content
6. Compare: digests match -- proceed silently without prompting the user

## Step 2 -- Verify Dependencies

The task lists "Depends on: None". No dependency verification needed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Get current user account ID via `jira.user_info()`
2. Assign task: `jira.edit_issue(TC-9201, assignee=<account-id>)`
3. Transition: `jira.transition_issue(TC-9201)` to "In Progress"

## Step 4 -- Understand the Code

### 4.1 Inspect files to modify

Use the Serena instance `serena_backend` (tools called as `mcp__serena_backend__<tool>`):

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- `mcp__serena_backend__get_symbols_overview` to see AdvisoryService methods (`fetch`, `list`, `search`). Then `mcp__serena_backend__find_symbol` with `include_body=true` on the `list` or `fetch` method to understand the pattern for the new `severity_summary` method (parameter types, return type, transaction handling, error wrapping).

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- `mcp__serena_backend__get_symbols_overview` to see route registration pattern. Understand how routes are composed with `Router::new().route(...)`.

3. **`modules/fundamental/src/advisory/model/mod.rs`** -- `mcp__serena_backend__get_symbols_overview` to see existing `pub mod` declarations for models (summary, details). This is where `pub mod severity_summary;` will be added.

### 4.2 Inspect reference files

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- `mcp__serena_backend__find_symbol` to understand the handler pattern: `Path<Id>` extraction, service call, JSON response.

2. **`modules/fundamental/src/advisory/model/summary.rs`** -- `mcp__serena_backend__find_symbol` on `AdvisorySummary` to see the `severity` field type and structure.

3. **`entity/src/sbom_advisory.rs`** -- `mcp__serena_backend__get_symbols_overview` to understand the join table structure for SBOM-advisory relationships.

4. **`common/src/error.rs`** -- `mcp__serena_backend__find_symbol` on `AppError` to understand error handling patterns.

### 4.3 Check backward compatibility

Use `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to identify all callers and ensure the new method does not break existing consumers.

### 4.4 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root. If present, read it and extract CI check commands for use in Step 9. If not found, proceed normally.

### 4.5 Convention conformance analysis

**Sibling analysis for endpoints:**
- Inspect `endpoints/get.rs` and `endpoints/list.rs` in the advisory module for patterns in error handling, parameter extraction, response types, and imports.

**Sibling analysis for models:**
- Inspect `model/summary.rs` and `model/details.rs` for struct patterns, derive macros, serde attributes, and documentation.

**Sibling analysis for service methods:**
- Inspect `fetch` and `list` methods in `advisory.rs` for transaction handling, query patterns, and error wrapping.

### 4.6 Test convention analysis

- Inspect `tests/api/advisory.rs` and `tests/api/sbom.rs` for test naming, assertion style, setup patterns, and error case coverage.
- Expected conventions: `assert_eq!(resp.status(), StatusCode::OK)`, body deserialization, 404 tests, `test_<endpoint>_<scenario>` naming.

### 4.7 Documentation file identification

- Check `docs/api.md` (referenced in CLAUDE.md) for API documentation that may need updating with the new endpoint.
- Check `README.md` at repository root for any API endpoint listings.

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

New file -- SeveritySummary response struct:

```rust
use serde::Serialize;

/// Summary of advisory severity counts for an SBOM.
///
/// Aggregates the number of advisories at each severity level
/// linked to a specific SBOM, enabling dashboard severity breakdowns.
#[derive(Clone, Debug, Default, Serialize)]
pub struct SeveritySummary {
    /// Number of critical-severity advisories.
    pub critical: u64,
    /// Number of high-severity advisories.
    pub high: u64,
    /// Number of medium-severity advisories.
    pub medium: u64,
    /// Number of low-severity advisories.
    pub low: u64,
    /// Total number of unique advisories across all severity levels.
    pub total: u64,
}
```

Derive macros and field types will be adjusted based on what sibling model files use (discovered in Step 4).

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add module registration:

```rust
pub mod severity_summary;
```

Following the existing pattern of `pub mod summary;` and `pub mod details;`.

### 6.3 Add `severity_summary` method to `modules/fundamental/src/advisory/service/advisory.rs`

Add a new method to `AdvisoryService` following the pattern of existing `fetch`/`list` methods:

```rust
/// Computes a severity summary for all advisories linked to the given SBOM.
///
/// Queries the sbom_advisory join table to find advisories associated with
/// the SBOM, deduplicates by advisory ID, and counts by severity level.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Query sbom_advisory join table for advisories linked to this SBOM
    // 2. Deduplicate by advisory ID
    // 3. For each unique advisory, read severity from AdvisorySummary
    // 4. Count by severity level (Critical, High, Medium, Low)
    // 5. Return SeveritySummary with counts and total
}
```

Implementation details:
- Use the `sbom_advisory` entity from `entity/src/sbom_advisory.rs` to join SBOMs to advisories
- Deduplicate advisory IDs using a HashSet or SQL DISTINCT
- Map severity strings to count fields using pattern matching
- Default all counts to 0 (via `SeveritySummary::default()`)
- Wrap errors with `.context()` matching the pattern in `common/src/error.rs`

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

New endpoint handler following the pattern from `endpoints/get.rs`:

```rust
/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity summary with counts of advisories at each severity
/// level (Critical, High, Medium, Low) linked to the specified SBOM.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: Extension<AdvisoryService>,
    tx: Extension<Transactional<'_>>,
) -> Result<Json<SeveritySummary>, AppError> {
    // 1. Call service.severity_summary(id, &tx)
    // 2. Return 404 if SBOM not found (matching existing SBOM endpoint behavior)
    // 3. Return Json(summary) on success
}
```

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route following the existing `Router::new().route(...)` pattern:

```rust
use severity_summary::get_severity_summary;

// Add to the Router chain:
.route("/api/v2/sbom/:id/advisory-summary", get(get_severity_summary))
```

### 6.6 Cross-repo API contract verification

Not applicable -- this is a backend-only task, no frontend consumer is being written.

### 6.7 Code quality practices

- All new structs (`SeveritySummary`) have documentation comments
- All new public functions (`severity_summary`, `get_severity_summary`) have documentation comments explaining behavior, parameters, and return values
- Follow sibling patterns for derive macros, imports, and formatting

### 6.8 Documentation impact

- If `docs/api.md` exists and documents endpoints, add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint with request/response documentation
- No other documentation updates expected unless the task includes a Documentation Updates section

## Step 7 -- Write Tests

### Create `tests/api/advisory_summary.rs`

Following test conventions discovered in Step 4 (from `tests/api/advisory.rs` and `tests/api/sbom.rs`):

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_with_known_advisories() {
    // Given an SBOM with advisories at known severity levels
    // (setup: create test SBOM, link advisories with specific severities)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response contains correct counts per severity level
    // assert_eq!(resp.status(), StatusCode::OK)
    // assert_eq!(body.critical, <expected>)
    // assert_eq!(body.high, <expected>)
    // etc.
}

/// Verifies that a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_advisory_summary_sbom_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary

    // Then a 404 response is returned
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND)
}

/// Verifies that an SBOM with no advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary

    // Then all severity counts are zero and total is zero
    // assert_eq!(body.critical, 0)
    // assert_eq!(body.high, 0)
    // assert_eq!(body.medium, 0)
    // assert_eq!(body.low, 0)
    // assert_eq!(body.total, 0)
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisories() {
    // Given an SBOM with duplicate advisory links (same advisory linked multiple times)

    // When requesting the advisory summary

    // Then the count reflects unique advisories only
    // assert_eq!(body.total, <unique count, not duplicate count>)
}
```

Run tests: `cargo test` -- fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns correct shape | Test: test_advisory_summary_with_known_advisories |
| Returns 404 for non-existent SBOM ID | Test: test_advisory_summary_sbom_not_found |
| Counts only unique advisories | Test: test_advisory_summary_deduplicates_advisories |
| All severity levels default to 0 | Test: test_advisory_summary_no_advisories, also SeveritySummary derives Default |
| Response time under 200ms for 500 advisories | Verify via efficient SQL query (single aggregation query with GROUP BY, no N+1) |

## Step 9 -- Self-Verification

### Scope containment
Run `git diff --name-only` and verify all changed files are in the task's Files to Modify and Files to Create lists:
- `modules/fundamental/src/advisory/service/advisory.rs` -- in scope (Files to Modify)
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- in scope (Files to Modify)
- `modules/fundamental/src/advisory/model/mod.rs` -- in scope (Files to Modify)
- `modules/fundamental/src/advisory/model/severity_summary.rs` -- in scope (Files to Create)
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- in scope (Files to Create)
- `tests/api/advisory_summary.rs` -- in scope (Files to Create)

Any out-of-scope files would be flagged for user approval.

### Untracked file check
Run `git status --short`, check for `??` entries in directories where implementation occurred. Flag any referenced but unstaged files.

### Sensitive-pattern check
Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- expect no matches.

### Documentation currency
If `docs/api.md` was updated in Step 6.8, verify it accurately reflects the new endpoint. If not updated, check whether it needs updating now.

### CI checks from CONVENTIONS.md
If CONVENTIONS.md contained CI check commands, run all of them. If any fail, fix before proceeding.

### Duplication check
Search repository for existing severity aggregation logic, summary computation patterns, or similar endpoint implementations that could be reused.

### Data-flow trace
- Input: GET request with SBOM ID path parameter
- Processing: endpoint handler extracts ID, calls AdvisoryService.severity_summary(), which queries sbom_advisory join table, deduplicates, counts by severity
- Output: JSON response with severity counts
- All stages connected -- COMPLETE

### Contract and sibling parity
- SeveritySummary implements Serialize (required for Json response)
- Endpoint handler follows same Result<Json<T>, AppError> pattern as siblings
- Error handling uses .context() wrapping consistent with sibling endpoints

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs
git add modules/fundamental/src/advisory/model/mod.rs
git add modules/fundamental/src/advisory/service/advisory.rs
git add modules/fundamental/src/advisory/endpoints/severity_summary.rs
git add modules/fundamental/src/advisory/endpoints/mod.rs
git add tests/api/advisory_summary.rs
# Add any documentation files updated

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to an SBOM.

Includes SeveritySummary model, AdvisoryService.severity_summary() method,
endpoint handler, and integration tests.

Implements TC-9201"

git push -u origin TC-9201

gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "## Summary

Add a REST endpoint that aggregates advisory severity counts for a given SBOM, enabling dashboard widgets to render severity breakdowns without client-side counting.

- New model: SeveritySummary response struct
- New service method: AdvisoryService.severity_summary()
- New endpoint: GET /api/v2/sbom/{id}/advisory-summary
- Integration tests for happy path, 404, empty SBOM, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)"
```

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (customfield_10875) with the PR URL in ADF format:
   ```
   jira.update_issue(TC-9201, fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
   ```

2. **Add comment** to TC-9201 with:
   - PR link
   - Summary: Added advisory severity aggregation endpoint with model, service method, endpoint handler, and integration tests
   - No deviations from the plan
   - Comment ends with the skill footnote (read version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`)

3. **Transition** TC-9201 to "In Review":
   ```
   jira.transition_issue(TC-9201) -> In Review
   ```
