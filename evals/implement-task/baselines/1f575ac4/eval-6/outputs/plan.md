# Implementation Plan for TC-9201

**Task**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Jira Web URL**: https://redhat.atlassian.net/browse/TC-9201

---

## Step 0 -- Validate Project Configuration

Project Configuration in CLAUDE.md is verified:
- **Repository Registry**: present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
- **Jira Configuration**: present, contains Project key (TC), Cloud ID, Feature issue type ID, Git Pull Request custom field (`customfield_10875`), GitHub Issue custom field (`customfield_10747`)
- **Code Intelligence**: present, with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend` using rust-analyzer

All required sections are present and complete. Proceeding.

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")` and parse the structured description:

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM |
| Files to Modify | `modules/fundamental/src/advisory/service/advisory.rs`, `modules/fundamental/src/advisory/endpoints/mod.rs`, `modules/fundamental/src/advisory/model/mod.rs`, `server/src/main.rs` (no changes needed) |
| Files to Create | `modules/fundamental/src/advisory/model/severity_summary.rs`, `modules/fundamental/src/advisory/endpoints/severity_summary.rs`, `tests/api/advisory_summary.rs` |
| API Changes | `GET /api/v2/sbom/{id}/advisory-summary` -- NEW |
| Dependencies | None |
| Target PR | Not present (default flow) |
| Bookend Type | Not present (default flow) |
| GitHub Issue custom field | Check `customfield_10747` on the fetched issue; extract GitHub issue reference if present |

Capture `webUrl` from the API response for use in the PR description.

## Step 1.5 -- Verify Description Integrity

Described in `outputs/digest-match.md`. Digest comment found with matching `sha256-md` tagged digest. Created and updated timestamps are identical (no edit detected). Hex digests match. Proceeding silently.

## Step 2 -- Verify Dependencies

The task has no dependencies listed. No dependency verification needed. Proceeding.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve the current user's Jira account ID via `jira.user_info()`
2. Assign TC-9201 to the current user via `jira.edit_issue("TC-9201", assignee=<account-id>)`
3. Transition TC-9201 to "In Progress" via `jira.transition_issue("TC-9201") -> In Progress`

## Step 4 -- Understand the Code

### 4.1 Inspect files to modify

Use the Serena instance `serena_backend` (tools called as `mcp__serena_backend__<tool>`):

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Run `mcp__serena_backend__get_symbols_overview` to see AdvisoryService struct and its existing methods (`fetch`, `list`, `search`). Then use `mcp__serena_backend__find_symbol` with `include_body=true` on one of the existing methods (e.g., `fetch`) to understand the signature pattern: `(&self, id: Id, tx: &Transactional<'_>) -> Result<...>`.

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Run `get_symbols_overview` to see existing route registrations. Examine how routes are registered using `Router::new().route("/path", get(handler))`.

3. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- Read this file to understand the endpoint handler pattern: path param extraction via `Path<Id>`, service call, JSON response, AppError handling.

4. **`modules/fundamental/src/advisory/model/mod.rs`** -- Read to see existing `pub mod` declarations (e.g., `pub mod summary;`, `pub mod details;`).

5. **`modules/fundamental/src/advisory/model/summary.rs`** -- Use `find_symbol` on `AdvisorySummary` to understand the struct and its `severity` field type.

6. **`entity/src/sbom_advisory.rs`** -- Read to understand the join table schema linking SBOMs to advisories.

7. **`common/src/error.rs`** -- Use `get_symbols_overview` to understand the `AppError` enum and how `.context()` wrapping works.

### 4.2 Inspect sibling files for convention conformance

Use `get_symbols_overview` on 2-3 siblings:
- `modules/fundamental/src/advisory/endpoints/list.rs` -- sibling endpoint handler
- `modules/fundamental/src/sbom/endpoints/get.rs` -- parallel module endpoint for comparison
- `modules/fundamental/src/sbom/model/summary.rs` -- sibling model struct

### 4.3 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). If present:
- Read and follow its conventions throughout implementation
- Extract CI check commands from any "CI checks" / "Verification" section for use in Step 9
- Extract any code generation commands

### 4.4 Convention conformance analysis

Based on sibling inspection, record discovered conventions:

**Expected discovered conventions (from sibling analysis):**
- **Error handling**: all handlers use `Result<T, AppError>` with `.context()` for wrapping
- **Naming**: service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`)
- **Endpoint pattern**: extract path params via `Path<Id>`, call service method, return `Json(result)`
- **Route registration**: `Router::new().route("/path", get(handler))` in `endpoints/mod.rs`
- **Model structs**: derive `Serialize, Deserialize, Debug, Clone` with `#[serde(rename_all = "camelCase")]`
- **Service method signature**: `(&self, ..., tx: &Transactional<'_>) -> Result<T, anyhow::Error>`

### 4.5 Test convention analysis

Inspect sibling test files:
- `tests/api/advisory.rs` -- advisory endpoint integration tests
- `tests/api/sbom.rs` -- SBOM endpoint integration tests

**Expected discovered test conventions:**
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Response validation**: check status code, deserialize body, assert on specific field values
- **Error cases**: 404 tests with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming**: `test_<endpoint>_<scenario>` pattern
- **Setup**: tests hit a real PostgreSQL test database with pre-seeded data

### 4.6 Documentation file identification

Identify related documentation:
- `README.md` at repository root
- `docs/api.md` -- REST API reference (likely needs update for new endpoint)
- `docs/architecture.md` -- system architecture overview

### 4.7 Backward compatibility check

Use `mcp__serena_backend__find_referencing_symbols` on any symbols being modified (e.g., `AdvisoryService`, the route registration in `endpoints/mod.rs`) to identify all callers and ensure changes do not break existing functionality.

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

Create the `SeveritySummary` response struct:

```rust
/// Summary of advisory severity counts for an SBOM.
///
/// Aggregates the number of linked advisories by severity level,
/// enabling dashboard widgets to render severity breakdowns.
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
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

Default all fields to 0 using `Default` derive or manual impl.

### 6.2 Register the model module in `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` alongside existing module declarations.

### 6.3 Add `severity_summary` method to `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`

Following the existing method pattern (`fetch`, `list`):

```rust
/// Computes a severity summary for all advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table, resolves each advisory's severity,
/// deduplicates by advisory ID, and returns per-level counts.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, anyhow::Error> {
    // 1. Query sbom_advisory join table for advisories linked to sbom_id
    // 2. Deduplicate by advisory ID
    // 3. For each unique advisory, fetch its severity from AdvisorySummary
    // 4. Count per severity level (Critical, High, Medium, Low)
    // 5. Return SeveritySummary with counts and total
}
```

Key implementation details:
- Use the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) to find advisories linked to the SBOM
- Deduplicate by advisory ID to satisfy acceptance criterion
- Use the `severity` field from `AdvisorySummary` to categorize
- Return all zeros when no advisories exist (default SeveritySummary)
- Wrap errors with `.context()` matching the AppError pattern in `common/src/error.rs`

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern in `advisory/endpoints/get.rs`:

```rust
/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity summary aggregating advisory counts by severity level
/// for the specified SBOM.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: Extension<AdvisoryService>,
    tx: Extension<Transactional<'_>>,
) -> Result<Json<SeveritySummary>, AppError> {
    // 1. Extract path param (SBOM ID)
    // 2. Verify SBOM exists -- return 404 if not found
    // 3. Call service.severity_summary(id, &tx)
    // 4. Return Json(result)
}
```

Key implementation details:
- Return 404 when SBOM ID does not exist, consistent with existing SBOM endpoints
- Use `.context()` wrapping for error handling
- Return the struct directly (Axum's `Json` extractor handles serialization)

### 6.5 Register the route in `modules/fundamental/src/advisory/endpoints/mod.rs`

Add the new route following the existing registration pattern:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

### 6.6 Documentation impact

- Check `docs/api.md` for existing API documentation and add the new endpoint:
  - `GET /api/v2/sbom/{id}/advisory-summary` -- returns severity count summary
  - Document the response shape: `{ critical, high, medium, low, total }`
- No changes needed to `server/src/main.rs` (routes auto-mount via module registration)

### 6.7 Code quality practices

Verify all new symbols have documentation comments:
- `SeveritySummary` struct and all its fields
- `severity_summary` service method
- `get_severity_summary` handler function

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with integration tests following the sibling test conventions discovered in Step 4.

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that a valid SBOM with known advisories returns the correct
/// severity counts broken down by level.
#[tokio::test]
async fn test_advisory_summary_with_known_advisories() {
    // Given an SBOM with pre-seeded advisories of known severities

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then the response status is 200 OK and severity counts match expected values
    // Assert on specific field values (critical, high, medium, low, total)
}
```

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM
/// returns a 404 Not Found response.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting GET /api/v2/sbom/{non_existent_id}/advisory-summary

    // Then the response status is 404 NOT_FOUND
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns a summary
/// with all severity counts set to zero.
#[tokio::test]
async fn test_advisory_summary_empty() {
    // Given an SBOM with no linked advisories

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then critical=0, high=0, medium=0, low=0, total=0
}
```

### Test 4: Duplicate advisory links are deduplicated

```rust
/// Verifies that duplicate advisory links in the sbom_advisory join table
/// are deduplicated so each advisory is counted only once.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)

    // When requesting GET /api/v2/sbom/{id}/advisory-summary

    // Then the total count reflects unique advisories only (not doubled)
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
| 1 | GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` | Verified by test 1 -- response deserialization and field assertions |
| 2 | Returns 404 when SBOM ID does not exist | Verified by test 2 -- status code assertion |
| 3 | Counts only unique advisories (deduplicates by advisory ID) | Verified by test 4 -- duplicate link deduplication |
| 4 | All severity levels default to 0 when no advisories exist | Verified by test 3 -- all-zeros assertion |
| 5 | Response time under 200ms for SBOMs with up to 500 advisories | Verified by query design using database-level aggregation rather than client-side iteration; performance testing on representative data |

## Step 9 -- Self-Verification

### Scope containment

Run `git diff --name-only` and compare against:
- **Files to Modify**: `advisory/service/advisory.rs`, `advisory/endpoints/mod.rs`, `advisory/model/mod.rs`
- **Files to Create**: `advisory/model/severity_summary.rs`, `advisory/endpoints/severity_summary.rs`, `tests/api/advisory_summary.rs`
- Any additional file (e.g., `docs/api.md`) would require user approval as out-of-scope

### Untracked file check

Run `git status --short`, extract `??` entries, filter by proximity to modified directories, search for code references, and flag any referenced untracked files for user review.

### Sensitive-pattern check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` to verify no secrets are staged.

### Documentation currency

If `docs/api.md` describes the API and the new endpoint was not added during Step 6, update it now.

### CI checks from CONVENTIONS.md

Run all CI check commands extracted from CONVENTIONS.md in Step 4 (e.g., `cargo fmt --check`, `cargo clippy`, `cargo build`). Hard stop on any failure.

### Data-flow trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param (input) -> query sbom_advisory join table -> aggregate by severity -> return JSON response (output) -- **COMPLETE**

### Contract and sibling parity

- `SeveritySummary` struct: check it has all required derives and serde attributes matching sibling model structs
- `get_severity_summary` handler: verify it follows the same `Result<Json<T>, AppError>` return pattern as sibling handlers
- `severity_summary` service method: verify it follows the same `(&self, ..., tx: &Transactional<'_>)` signature as sibling methods
- Caller-site parity: the new endpoint handler calls `AdvisoryService::severity_summary` -- compare with how other handlers call service methods

### Duplication check

Search for existing severity aggregation logic in the codebase using Grep/Serena to ensure no duplication.

### Cross-section reference consistency

Verify file paths are consistent:
- `AdvisoryService` is referenced in both Files to Modify (`advisory/service/advisory.rs`) and Implementation Notes (`advisory/service/advisory.rs`) -- consistent
- Route registration referenced in Files to Modify (`advisory/endpoints/mod.rs`) and Implementation Notes (`advisory/endpoints/mod.rs`) -- consistent

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
       modules/fundamental/src/advisory/model/mod.rs \
       modules/fundamental/src/advisory/service/advisory.rs \
       modules/fundamental/src/advisory/endpoints/severity_summary.rs \
       modules/fundamental/src/advisory/endpoints/mod.rs \
       tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes deduplication by advisory ID and
404 handling for missing SBOMs.

Implements TC-9201"
```

Push and create PR targeting main:

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "## Summary

Add a new REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM, enabling dashboard widgets to render severity breakdowns without client-side counting.

### Changes
- New \`SeveritySummary\` response struct with per-level counts
- New \`severity_summary\` method on \`AdvisoryService\`
- New \`GET /api/v2/sbom/{id}/advisory-summary\` endpoint handler
- Integration tests covering happy path, 404, empty results, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
"
```

If a GitHub issue reference was extracted from `customfield_10747`, append a `Closes <owner>/<repo>#<number>` line to the PR body.

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field** (`customfield_10875`) on TC-9201 with the PR URL using ADF inlineCard format:

   ```
   jira.update_issue("TC-9201", fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
   ```

2. **Add comment** to TC-9201 with PR link, summary of changes, and any deviations. Read the plugin version from `plugins/sdlc-workflow/.claude-plugin/plugin.json` and include the footnote with the version:

   Content:
   - PR link
   - Summary: added SeveritySummary model, severity_summary service method, GET endpoint, and integration tests
   - Deviations from plan: none (or list any)
   - Footnote with horizontal rule and `sdlc-workflow/implement-task v{version}` link

3. **Transition** TC-9201 to "In Review" via `jira.transition_issue("TC-9201") -> In Review`
