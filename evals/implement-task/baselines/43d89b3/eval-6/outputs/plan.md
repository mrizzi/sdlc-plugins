# Implementation Plan for TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Step 0 -- Validate Project Configuration

Verify the project's CLAUDE.md contains the required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`.
2. **Jira Configuration** -- present, contains Project key `TC`, Cloud ID, Feature issue type ID `10142`, Git Pull Request custom field `customfield_10875`, GitHub Issue custom field `customfield_10747`.
3. **Code Intelligence** -- present, confirms tool naming convention `mcp__serena_backend__<tool>` and notes rust-analyzer may take 30-60 seconds to index.

All required sections are present. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP for all JIRA operations. If MCP fails, prompt the user for REST API fallback per the documented fallback protocol.

## Step 1 -- Fetch and Parse Jira Task

Fetch the issue:

```
jira.get_issue(TC-9201)
```

Parsed sections:

- **Repository:** trustify-backend
- **Target Branch:** main
- **Description:** Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns summary with counts per severity level (Critical, High, Medium, Low) and a total.
- **Files to Modify:**
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`
  - `server/src/main.rs` -- no changes needed
- **Files to Create:**
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes:** `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Implementation Notes:** Follow existing patterns in `get.rs`, use `sbom_advisory` join table, use `AdvisorySummary.severity` field for counting, return `Result<T, AppError>` with `.context()`.
- **Acceptance Criteria:** 5 items (correct JSON response, 404 for missing SBOM, deduplication, zero defaults, performance)
- **Test Requirements:** 4 tests (valid SBOM counts, 404, empty SBOM, deduplication)
- **Dependencies:** None
- **Target PR:** not present (default flow)
- **Bookend Type:** not present (default flow)

Capture `webUrl` for Jira link in PR description (e.g., `https://redhat.atlassian.net/browse/TC-9201`).

Check `customfield_10747` (GitHub Issue custom field) -- extract GitHub issue reference if present; skip silently if empty.

## Step 1.5 -- Verify Description Integrity

This step was analyzed in detail in `digest-match.md`. Summary:

1. Fetch comments on TC-9201 via `jira.get_issue_comments(TC-9201)`.
2. Locate the comment with marker `[sdlc-workflow] Description digest:`.
3. Found: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`.
4. Comment `created` and `updated` timestamps are identical -- not edited, no warning needed.
5. Format tag is `sha256-md` (not legacy untagged format) -- proceed with comparison.
6. Compute current digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt` -- output: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`.
7. Format tags match (`sha256-md` == `sha256-md`) -- no format mismatch warning.
8. Hex digests match -- description is unmodified since plan-feature created it.
9. **Proceed silently** -- no user prompt, no added latency, no warning message. Continue directly to Step 2.

## Step 2 -- Verify Dependencies

The task has no dependencies (`Dependencies: None`). No blocking checks required. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's account ID: `jira.user_info()`
2. Assign TC-9201 to current user: `jira.edit_issue(TC-9201, assignee=<account-id>)`
3. Transition to In Progress: `jira.transition_issue(TC-9201, "In Progress")`

## Step 4 -- Understand the Code

### 4.1 Inspect Files to Modify

Use Serena instance `serena_backend` (tools called as `mcp__serena_backend__<tool>`):

1. **`modules/fundamental/src/advisory/service/advisory.rs`**
   - `mcp__serena_backend__get_symbols_overview` to see AdvisoryService struct and its methods (`fetch`, `list`, `search`).
   - `mcp__serena_backend__find_symbol` with `include_body=true` on the `list` or `fetch` method to understand the pattern for service methods (signature, return type, transaction handling).

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`**
   - `mcp__serena_backend__get_symbols_overview` to see current route registration pattern.
   - Examine how existing routes are registered (`Router::new().route(...)` pattern).

3. **`modules/fundamental/src/advisory/model/mod.rs`**
   - `mcp__serena_backend__get_symbols_overview` to see current module declarations (`pub mod summary;`, `pub mod details;`).

4. **`modules/fundamental/src/advisory/model/summary.rs`**
   - `mcp__serena_backend__find_symbol` on `AdvisorySummary` to see the `severity` field type and structure.

5. **`entity/src/sbom_advisory.rs`**
   - `mcp__serena_backend__get_symbols_overview` to understand the join table structure.

6. **`common/src/error.rs`**
   - `mcp__serena_backend__find_symbol` on `AppError` to understand the error enum and `.context()` usage.

### 4.2 Convention Conformance Analysis

Identify sibling files for pattern analysis:

- **Endpoint siblings:** `modules/fundamental/src/advisory/endpoints/get.rs`, `list.rs` -- examine for handler signature, path parameter extraction, JSON response pattern.
- **Service siblings:** The existing `fetch` and `list` methods in `advisory.rs` -- examine for method signature pattern (`&self`, parameter types, return type, transaction handling).
- **Model siblings:** `modules/fundamental/src/advisory/model/summary.rs`, `details.rs` -- examine for struct definition pattern, derive macros, serde attributes.

Expected discovered conventions:
- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping.
- **Naming:** Service methods use `verb_noun` pattern.
- **Path extraction:** Handlers use `Path<Id>` extractor.
- **Response:** Return struct directly, Axum's `Json` extractor handles serialization.
- **Derive macros:** Model structs derive `Serialize`, `Deserialize`, `Debug`, and possibly `Clone`, `PartialEq`.

### 4.3 Test Convention Analysis

Examine sibling test files:
- `tests/api/advisory.rs` -- advisory endpoint integration tests
- `tests/api/sbom.rs` -- SBOM endpoint integration tests

Expected test conventions:
- Assertion style: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization.
- Error cases: 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.
- Test naming: `test_<endpoint>_<scenario>` pattern.
- Setup: real PostgreSQL test database with test fixtures.

### 4.4 CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the repository root. If present, read it and extract CI check commands. Follow any conventions found throughout implementation.

### 4.5 Documentation File Identification

Identify documentation files for later review:
- `docs/api.md` -- REST API reference (may need updating for the new endpoint)
- `docs/architecture.md` -- system architecture overview
- `README.md` -- project readme

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

Define the `SeveritySummary` response struct:

```rust
/// Summary of advisory severity counts for a given SBOM.
///
/// Aggregates the number of advisories at each severity level,
/// enabling dashboard widgets to render severity breakdowns.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct SeveritySummary {
    /// Number of critical-severity advisories.
    pub critical: u32,
    /// Number of high-severity advisories.
    pub high: u32,
    /// Number of medium-severity advisories.
    pub medium: u32,
    /// Number of low-severity advisories.
    pub low: u32,
    /// Total number of unique advisories across all severity levels.
    pub total: u32,
}
```

Follow the derive macro pattern observed in sibling model files (`summary.rs`, `details.rs`). Add `Default` derive to support zero-initialization.

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add module declaration:

```rust
pub mod severity_summary;
```

Following the existing pattern of `pub mod summary;` and `pub mod details;`.

### 6.3 Modify `modules/fundamental/src/advisory/service/advisory.rs`

Add `severity_summary` method to `AdvisoryService`, following the pattern of existing `fetch` and `list` methods:

```rust
/// Computes severity counts for all advisories linked to the given SBOM.
///
/// Returns a `SeveritySummary` with deduplicated counts per severity level.
/// Returns a 404-equivalent error if the SBOM does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify the SBOM exists (return 404 if not)
    // 2. Query sbom_advisory join table for advisories linked to this SBOM
    // 3. Deduplicate by advisory ID
    // 4. For each unique advisory, fetch its AdvisorySummary and read severity
    // 5. Count by severity level (Critical, High, Medium, Low)
    // 6. Return SeveritySummary with counts and total
}
```

Key implementation details:
- Use `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) to find linked advisories.
- Deduplicate by advisory ID before counting.
- Use `AdvisorySummary.severity` field for severity classification.
- Default all severity levels to 0 when no advisories exist.
- Wrap errors with `.context()` matching `common/src/error.rs` pattern.

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern in `get.rs`:

```rust
/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a JSON summary of advisory severity counts for the specified SBOM.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    State(service): State<AdvisoryService>,
    tx: Transactional<'_>,
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
use severity_summary::get_severity_summary;

// Add to router:
.route("/api/v2/sbom/:id/advisory-summary", get(get_severity_summary))
```

### 6.6 Documentation Impact

Check if `docs/api.md` documents existing endpoints. If so, add entry for `GET /api/v2/sbom/{id}/advisory-summary` with request/response documentation.

### 6.7 Code Quality Verification

Ensure all new structs and public functions have documentation comments (verified above in code snippets). Every new symbol (`SeveritySummary`, `severity_summary`, `get_severity_summary`) has a doc comment explaining its purpose.

## Step 7 -- Write Tests

### Create `tests/api/advisory_summary.rs`

Follow sibling test conventions from `tests/api/advisory.rs` and `tests/api/sbom.rs`.

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_with_known_advisories() {
    // Given an SBOM with advisories at known severity levels
    // (set up test fixtures: create SBOM, link advisories with specific severities)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response contains correct counts per severity level
    // assert_eq!(resp.status(), StatusCode::OK)
    // Deserialize body and assert specific counts match expected values
}

/// Verifies that a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary

    // Then the response is 404
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND)
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_empty() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary

    // Then all severity counts are zero and total is zero
    // assert_eq!(summary.critical, 0)
    // assert_eq!(summary.high, 0)
    // assert_eq!(summary.medium, 0)
    // assert_eq!(summary.low, 0)
    // assert_eq!(summary.total, 0)
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)

    // When requesting the advisory summary

    // Then the advisory is counted only once
    // Assert total equals the number of unique advisories, not the number of links
}
```

Run tests:

```bash
cargo test
```

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

1. `GET /api/v2/sbom/{id}/advisory-summary` returns `{ critical: N, high: N, medium: N, low: N, total: N }` -- verified via test `test_advisory_summary_with_known_advisories`.
2. Returns 404 when SBOM ID does not exist -- verified via test `test_advisory_summary_not_found`.
3. Counts only unique advisories (deduplicates by advisory ID) -- verified via test `test_advisory_summary_deduplication`.
4. All severity levels default to 0 when no advisories exist -- verified via test `test_advisory_summary_empty`.
5. Response time under 200ms for SBOMs with up to 500 advisories -- verified by ensuring query uses efficient joins and deduplication at the database level rather than in application code.

## Step 9 -- Self-Verification

### Scope Containment

Run `git diff --name-only` and compare against Files to Modify and Files to Create:

Expected modified/created files:
- `modules/fundamental/src/advisory/model/severity_summary.rs` (new)
- `modules/fundamental/src/advisory/model/mod.rs` (modified)
- `modules/fundamental/src/advisory/service/advisory.rs` (modified)
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (new)
- `modules/fundamental/src/advisory/endpoints/mod.rs` (modified)
- `tests/api/advisory_summary.rs` (new)

Flag any out-of-scope files for user approval.

### Untracked File Check

Run `git status --short`, identify `??` entries in directories where implementation work occurred. Check for code references to any untracked files. Flag for user review if found.

### Sensitive-Pattern Check

```bash
git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
```

Flag any matches.

### Documentation Currency

Check if `docs/api.md` describes the advisory endpoints. If so, verify the new endpoint is documented. Update if needed.

### Documentation Scope Preservation

If documentation was modified, verify replacement text covers all original use cases.

### Cross-Section Reference Consistency

Verify file paths are consistent across all task description sections. Notably:
- `AdvisoryService` is referenced in both Files to Modify (`modules/fundamental/src/advisory/service/advisory.rs`) and Implementation Notes (same path) -- consistent.

### Duplication Check

Search for existing severity aggregation logic in the repository. Ensure the new code does not duplicate existing utilities.

### Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param -> call `AdvisoryService.severity_summary()` -> query `sbom_advisory` join table -> aggregate severity counts -> return JSON response -- **COMPLETE**.

### Contract & Sibling Parity

- `SeveritySummary` is a standalone response struct (no trait/interface contract to verify).
- Sibling parity with `get.rs` handler: error handling pattern (`.context()` wrapping), path parameter extraction (`Path<Id>`), JSON response return -- all consistent.

### CI Checks

Run CI check commands from `CONVENTIONS.md` (if found). Fix any failures. Hard stop on non-zero exit.

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns severity
counts (Critical, High, Medium, Low, total) for advisories linked to an SBOM.
Includes SeveritySummary model, AdvisoryService.severity_summary() method,
route registration, and integration tests.

Implements TC-9201"
```

Push and create PR:

```bash
git push -u origin TC-9201

gh pr create --base main \
  --title "feat(api): add advisory severity aggregation endpoint" \
  --body "## Summary

Add a new REST endpoint that aggregates vulnerability advisory severity counts
for a given SBOM, enabling dashboard widgets to render severity breakdowns.

- New endpoint: \`GET /api/v2/sbom/{id}/advisory-summary\`
- Returns: \`{ critical: N, high: N, medium: N, low: N, total: N }\`
- Deduplicates advisories by ID before counting
- Returns 404 for non-existent SBOMs
- Includes 4 integration tests covering happy path, 404, empty, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)"
```

If a GitHub issue reference was extracted from `customfield_10747`, append `Closes <owner>/<repo>#<number>` to the PR body.

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (`customfield_10875`) with the PR URL in ADF format:

```
jira.update_issue(TC-9201, fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
```

2. **Add comment** to TC-9201 with PR link, summary of changes, and any deviations from the plan. Include the skill footnote with version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`.

3. **Transition** TC-9201 to In Review:

```
jira.transition_issue(TC-9201, "In Review")
```
