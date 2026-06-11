# Implementation Plan for TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Step 0 -- Validate Project Configuration

Read the project's CLAUDE.md and verify:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena Instance `serena_backend` at path `./`
2. **Jira Configuration** -- present, contains Project key `TC`, Cloud ID, Feature issue type ID `10142`
3. **Code Intelligence** -- present, tool naming convention: `mcp__<serena-instance>__<tool>`

All required sections exist. Proceed.

## Step 0.5 -- JIRA Access Initialization

Determine JIRA access method. Attempt MCP first for all JIRA operations. If MCP
fails, prompt user with the three options (REST API fallback, skip, retry).

## Step 1 -- Fetch and Parse Jira Task

Fetch the issue:

```
jira.get_issue("TC-9201")
```

### Parsed sections

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
- **Implementation Notes**: Follow existing endpoint pattern, use `Path<Id>`, call service, return JSON, use `sbom_advisory` join table, use `AdvisorySummary.severity` field for counting, register route in endpoints/mod.rs, error handling with `AppError` + `.context()`, return struct directly via Axum's `Json` extractor
- **Acceptance Criteria**: 5 criteria (correct response shape, 404 for missing SBOM, deduplicated counts, zero defaults, sub-200ms performance)
- **Test Requirements**: 4 tests (correct counts, 404, all zeros, deduplication)
- **Target PR**: not present (default flow)
- **Bookend Type**: not present (default flow)
- **Dependencies**: None
- **Linked Issues**: is incorporated by TC-9001

Capture the issue's `webUrl` (e.g., `https://redhat.atlassian.net/browse/TC-9201`).

### GitHub Issue extraction

Look up `customfield_10747` from Jira Configuration. Read the field value from the
fetched issue. If present, parse the GitHub issue URL and store the reference. If
empty, skip silently.

## Step 1.5 -- Verify Description Integrity

(Detailed in `outputs/digest-match.md`)

1. Fetch comments: `jira.get_issue_comments("TC-9201")`
2. Locate digest comment: find comment starting with `[sdlc-workflow] Description digest:`
3. Found: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
4. Comment edit detection: `created` == `updated` -- comment is unmodified, no warning
5. Extract stored digest: format tag `md`, hex `a1b2c3d4e5f67890...`
6. Not legacy format (uses `sha256-md:` not `sha256:`) -- proceed with full verification
7. Compute current digest: `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
8. Compare format tags: both `md` -- tags match
9. Compare hex digests: MATCH (per task assumptions)
10. **Outcome**: proceed silently to Step 2

## Step 2 -- Verify Dependencies

The task specifies "Dependencies: None". No prerequisite tasks to check. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's account ID:
   ```
   jira.user_info()
   ```
2. Assign the task to the current user:
   ```
   jira.edit_issue("TC-9201", assignee=<current-user-account-id>)
   ```
3. Transition to In Progress:
   ```
   jira.transition_issue("TC-9201") -> "In Progress"
   ```

## Step 4 -- Understand the Code

Use the `serena_backend` instance (from Repository Registry) for code intelligence.
Tools called as `mcp__serena_backend__<tool>`.

### 4.1 Inspect files to modify

1. **`modules/fundamental/src/advisory/service/advisory.rs`**:
   - `mcp__serena_backend__get_symbols_overview` to see structure (AdvisoryService, fetch, list, search methods)
   - `mcp__serena_backend__find_symbol("AdvisoryService", include_body=true)` to understand the service struct
   - `mcp__serena_backend__find_symbol("fetch", include_body=true)` to see the pattern for service methods (takes `&self, id, tx: &Transactional<'_>`)

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`**:
   - `mcp__serena_backend__get_symbols_overview` to see route registration pattern
   - Understand how `Router::new().route("/path", get(handler))` is structured

3. **`modules/fundamental/src/advisory/model/mod.rs`**:
   - `mcp__serena_backend__get_symbols_overview` to see existing module declarations (`pub mod summary; pub mod details;`)

### 4.2 Inspect reference files (patterns to follow)

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- reference endpoint pattern:
   - `mcp__serena_backend__get_symbols_overview` then `find_symbol` for the handler function
   - Understand: path param extraction (`Path<Id>`), service call, JSON response, error handling

2. **`modules/fundamental/src/advisory/model/summary.rs`** -- AdvisorySummary struct:
   - `mcp__serena_backend__find_symbol("AdvisorySummary", include_body=true)` to see the `severity` field

3. **`entity/src/sbom_advisory.rs`** -- join table:
   - `mcp__serena_backend__get_symbols_overview` to understand the join entity structure

4. **`common/src/error.rs`** -- AppError:
   - `mcp__serena_backend__find_symbol("AppError", include_body=true)` to see error enum variants and IntoResponse impl

### 4.3 Check backward compatibility

- `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to see all callers
- `mcp__serena_backend__find_referencing_symbols` on advisory `endpoints/mod.rs` route registration to understand the mounting pattern

### 4.4 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`).
The repo structure shows `CONVENTIONS.md` exists. Read it for:
- Naming rules
- Directory structure conventions
- Code patterns
- Test conventions
- CI check commands (verification commands extraction)
- Code generation commands

### 4.5 Convention conformance analysis

**Sibling analysis for production code:**
- Sibling endpoints: `get.rs`, `list.rs` in `advisory/endpoints/`
- Sibling models: `summary.rs`, `details.rs` in `advisory/model/`
- Sibling services: `advisory.rs` in `advisory/service/`
- Sibling tests: `advisory.rs`, `sbom.rs`, `search.rs` in `tests/api/`

Examine 2-3 siblings in each category to discover conventions for:
- Error handling (`Result<T, AppError>` with `.context()`)
- Naming (service methods: `verb_noun` pattern)
- Response types (direct struct return via Axum's `Json`)
- Route registration pattern

**Sibling analysis for test code:**
- `tests/api/advisory.rs` and `tests/api/sbom.rs` as sibling test files
- Examine assertion patterns: `assert_eq!(resp.status(), StatusCode::OK)`, body deserialization, 404 tests
- Test naming: `test_<endpoint>_<scenario>`
- Setup/teardown patterns

### 4.6 Documentation file identification

Identify docs related to the code being modified:
- `README.md` at repo root
- `docs/api.md` (API reference, if it documents endpoints)
- `docs/architecture.md` (system architecture)
- `CONVENTIONS.md` at repo root

Record for use in Step 6 documentation impact and Step 9 documentation currency.

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

Target Branch is `main`, so the PR base will be `main`.

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

New file: the SeveritySummary response struct.

```rust
use serde::Serialize;

/// Aggregated severity counts for advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// The `total` field is the sum of all severity levels.
#[derive(Debug, Clone, Serialize, Default)]
pub struct SeveritySummary {
    /// Count of advisories with Critical severity.
    pub critical: u64,
    /// Count of advisories with High severity.
    pub high: u64,
    /// Count of advisories with Medium severity.
    pub medium: u64,
    /// Count of advisories with Low severity.
    pub low: u64,
    /// Total count of unique advisories across all severity levels.
    pub total: u64,
}
```

Follow the naming and derive patterns from sibling models (`summary.rs`, `details.rs`).

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add the new module declaration:

```rust
pub mod severity_summary;
```

alongside existing `pub mod summary;` and `pub mod details;`.

### 6.3 Modify `modules/fundamental/src/advisory/service/advisory.rs`

Add a `severity_summary` method to `AdvisoryService`:

```rust
/// Computes aggregated severity counts for all advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories, then counts
/// unique advisories per severity level. Returns zero counts for severity
/// levels with no advisories.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Query sbom_advisory join table for advisories linked to the SBOM
    // 2. Verify SBOM exists -- return 404 AppError if not found
    // 3. Fetch advisory summaries, using AdvisorySummary.severity field
    // 4. Deduplicate by advisory ID
    // 5. Count by severity level (Critical, High, Medium, Low)
    // 6. Compute total
    // 7. Return SeveritySummary struct
}
```

Follow the pattern of existing `fetch` and `list` methods:
- Accept `&self, id, tx: &Transactional<'_>`
- Return `Result<T, AppError>`
- Use `.context()` for error wrapping
- Use the `sbom_advisory` entity from `entity/src/sbom_advisory.rs` for the join query
- Use `AdvisorySummary.severity` field for severity-level counting
- Deduplicate by advisory ID using a `HashSet` or SQL `DISTINCT`

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

New file: the GET handler.

```rust
use axum::extract::Path;
use axum::Json;

/// Handles GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for all advisories linked to the
/// specified SBOM. Returns 404 if the SBOM does not exist.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: /* extracted service */,
    tx: /* transactional context */,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("fetching advisory severity summary")?;
    Ok(Json(summary))
}
```

Follow the pattern from `modules/fundamental/src/advisory/endpoints/get.rs`:
- Extract path params via `Path<Id>`
- Call the service method
- Return `Json(result)`
- Error handling with `AppError` and `.context()`

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route:

```rust
mod severity_summary;

// In the router builder:
Router::new()
    // ... existing routes ...
    .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

Follow the existing route registration pattern in this file.

### 6.6 `server/src/main.rs`

No changes needed -- routes auto-mount via module registration.

### 6.7 Cross-repo API contract verification

Not applicable -- this task adds a new backend endpoint; there is no cross-repo
frontend consumer to verify against.

### 6.8 Code quality practices

- Every new struct (`SeveritySummary`) has documentation comments
- Every new function (`severity_summary`, `get_severity_summary`) has documentation comments
- Documentation uses `///` Rust doc comment convention
- One-line descriptions for fields, multi-line for complex functions

### 6.9 Documentation impact

- No Documentation Updates section in the task
- Check `docs/api.md` -- if it lists endpoints, add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- No architectural changes, so `docs/architecture.md` does not need updating
- Keep updates lightweight and scoped

## Step 7 -- Write Tests

### Create `tests/api/advisory_summary.rs`

Four tests required, following sibling test conventions from `tests/api/advisory.rs` and `tests/api/sbom.rs`:

```rust
/// Verifies that the advisory summary endpoint returns correct severity counts
/// for an SBOM with known advisories at each severity level.
#[tokio::test]
async fn test_advisory_summary_correct_counts() {
    // Given an SBOM with known advisories: 2 Critical, 3 High, 1 Medium, 0 Low
    // (set up test database with SBOM and linked advisories via sbom_advisory join table)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response should return HTTP 200 with correct counts
    // assert_eq!(resp.status(), StatusCode::OK);
    // assert_eq!(body.critical, 2);
    // assert_eq!(body.high, 3);
    // assert_eq!(body.medium, 1);
    // assert_eq!(body.low, 0);
    // assert_eq!(body.total, 6);
}

/// Verifies that requesting an advisory summary for a non-existent SBOM ID
/// returns a 404 Not Found response.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    // GET /api/v2/sbom/{non_existent_id}/advisory-summary

    // Then the response should return HTTP 404
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero counts
/// and a total of zero.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then all severity counts should be zero
    // assert_eq!(resp.status(), StatusCode::OK);
    // assert_eq!(body.critical, 0);
    // assert_eq!(body.high, 0);
    // assert_eq!(body.medium, 0);
    // assert_eq!(body.low, 0);
    // assert_eq!(body.total, 0);
}

/// Verifies that duplicate advisory links (same advisory linked to the same SBOM
/// multiple times) are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM with the same advisory linked twice via sbom_advisory

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the advisory should be counted only once
    // assert_eq!(body.total, 1);  // not 2
}
```

Test conventions applied:
- Assertion style: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- Error cases: 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- Naming: `test_advisory_summary_<scenario>`
- Documentation comments on every test function
- Given-When-Then section comments for non-trivial tests
- Value-based assertions (not length-only)

Run tests: `cargo test`

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| # | Criterion | Verification |
|---|---|---|
| 1 | GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` | Verified by `test_advisory_summary_correct_counts` |
| 2 | Returns 404 when SBOM ID does not exist | Verified by `test_advisory_summary_not_found` |
| 3 | Counts only unique advisories (deduplicates by advisory ID) | Verified by `test_advisory_summary_deduplicates` |
| 4 | All severity levels default to 0 when no advisories exist | Verified by `test_advisory_summary_no_advisories` |
| 5 | Response time under 200ms for SBOMs with up to 500 advisories | Verified by code review of query efficiency (single query with GROUP BY, no N+1) |

## Step 9 -- Self-Verification

### Scope containment

Run `git diff --name-only` and compare against Files to Modify and Files to Create:

**Expected modified files:**
- `modules/fundamental/src/advisory/service/advisory.rs` -- in scope (Files to Modify)
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- in scope (Files to Modify)
- `modules/fundamental/src/advisory/model/mod.rs` -- in scope (Files to Modify)

**Expected new files:**
- `modules/fundamental/src/advisory/model/severity_summary.rs` -- in scope (Files to Create)
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- in scope (Files to Create)
- `tests/api/advisory_summary.rs` -- in scope (Files to Create)

If any file outside this list is modified, flag to user for approval.

### Untracked file check

Run `git status --short`, extract `??` entries. Filter by proximity to implementation
directories. Search for code references to any flagged untracked files. Ask user
before staging.

### Sensitive-pattern check

```bash
git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
```

Flag any matches; do not proceed until resolved.

### Documentation currency

Check if `docs/api.md` describes the new endpoint. If it was not updated in Step 6,
update it now with the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

### Documentation scope preservation

If documentation files were modified, verify replacement text covers all original
use cases. Not expected to be a concern for this task since documentation changes
are purely additive (new endpoint).

### Eval coverage currency

No `skills/<skill-name>/SKILL.md` files are being modified. Skip.

### Example consistency

If documentation examples were added, verify narrative text matches data structures.

### Cross-section reference consistency

Verify file paths are consistent across task description sections:
- `AdvisoryService` referenced in Files to Modify as `advisory/service/advisory.rs` and in Implementation Notes as `advisory/service/advisory.rs` -- consistent
- Route registration in Files to Modify as `advisory/endpoints/mod.rs` and in Implementation Notes as `advisory/endpoints/mod.rs` -- consistent
- `AdvisorySummary` referenced in Implementation Notes at `advisory/model/summary.rs` -- this is a read-only reference, not a modification target. Consistent with repo structure.

### Duplication check

Search the repository for existing severity counting or aggregation logic:
- Grep for `severity_summary`, `severity_count`, `severity_aggregat` to check for existing implementations
- If duplicates found, refactor to reuse

### CI checks from CONVENTIONS.md

Run all CI check commands extracted from `CONVENTIONS.md` in Step 4. Hard stop on
any non-zero exit. Fix failures and re-run until all pass.

### Data-flow trace

Trace the complete data flow for the new feature:

- `GET /api/v2/sbom/{id}/advisory-summary` (input: HTTP request with SBOM ID)
  - -> `severity_summary.rs` handler extracts `Path<Id>` (input parsing)
  - -> calls `AdvisoryService.severity_summary(id, tx)` (processing)
  - -> queries `sbom_advisory` join table (data access)
  - -> fetches advisory severity from `AdvisorySummary.severity` (data enrichment)
  - -> deduplicates by advisory ID (processing)
  - -> counts by severity level, computes total (aggregation)
  - -> returns `Json(SeveritySummary)` (output: HTTP response)

**Result**: COMPLETE -- all stages connected from input to output.

### Contract & sibling parity

**Contract verification:**
- `SeveritySummary` -- standalone struct, implements `Serialize` (required for Axum's `Json` extractor). No trait/interface contract to verify beyond `Serialize`.
- `get_severity_summary` handler -- returns `Result<Json<SeveritySummary>, AppError>`, matching Axum handler contract.
- `severity_summary` service method -- returns `Result<SeveritySummary, AppError>`, consistent with existing service method patterns.

**Sibling parity:**
- Compare against `get.rs` endpoint: path extraction, service call, error handling -- all present.
- Compare against `fetch` service method: signature pattern, error wrapping -- all present.

**Cross-module shared entity analysis:**
- The new code reads from `sbom_advisory` join table. Other modules (ingestor) write to this table.
- Verify read patterns are consistent (transaction handling, query patterns).
- No insert/update/delete on `sbom_advisory` from this task -- read-only access.

**Caller-site parity:**
- New handler calls `AdvisoryService.severity_summary()`. Compare call pattern with existing endpoint handlers calling `AdvisoryService.fetch()` and `AdvisoryService.list()`. Ensure same service extraction, transaction handling, and error wrapping.

## Step 10 -- Commit and Push

### Commit

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs
git add modules/fundamental/src/advisory/model/mod.rs
git add modules/fundamental/src/advisory/service/advisory.rs
git add modules/fundamental/src/advisory/endpoints/severity_summary.rs
git add modules/fundamental/src/advisory/endpoints/mod.rs
git add tests/api/advisory_summary.rs
# Add any documentation files updated

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated severity counts (critical, high, medium, low, total)
for advisories linked to a given SBOM. Includes deduplication
by advisory ID and proper 404 handling for missing SBOMs.

Implements TC-9201"
```

### Push and create PR

```bash
git push -u origin TC-9201

gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "$(cat <<'EOF'
## Summary

Add a new REST endpoint `GET /api/v2/sbom/{id}/advisory-summary` that aggregates
vulnerability advisory severity counts for a given SBOM, returning counts per
severity level (Critical, High, Medium, Low) and a total.

### Changes
- New `SeveritySummary` response struct in `advisory/model/severity_summary.rs`
- New `severity_summary` method on `AdvisoryService`
- New GET handler in `advisory/endpoints/severity_summary.rs`
- Route registration in `advisory/endpoints/mod.rs`
- Integration tests covering correct counts, 404, zero defaults, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)

## Test plan
- [ ] `test_advisory_summary_correct_counts` -- verifies correct severity counts for known advisories
- [ ] `test_advisory_summary_not_found` -- verifies 404 for non-existent SBOM
- [ ] `test_advisory_summary_no_advisories` -- verifies all-zero response for SBOM with no advisories
- [ ] `test_advisory_summary_deduplicates` -- verifies deduplication of duplicate advisory links
EOF
)"
```

If a GitHub issue reference was extracted in Step 1, append `Closes <owner>/<repo>#<number>` to the PR body.

## Step 11 -- Update Jira

### Update Git Pull Request custom field

Look up `customfield_10875` from Jira Configuration. Update the field with ADF:

```
jira.update_issue("TC-9201", fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
```

### Add comment

Post a comment to TC-9201 with ADF `contentFormat`:

- PR link
- Summary: Added advisory severity aggregation endpoint with SeveritySummary model, AdvisoryService method, GET handler, route registration, and integration tests
- Deviations: None

Include the skill footer (read version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`):

```
---
This comment was AI-generated by [sdlc-workflow/implement-task](https://github.com/mrizzi/sdlc-plugins) v{version}.
```

### Transition to In Review

```
jira.transition_issue("TC-9201") -> "In Review"
```
