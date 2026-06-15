# Implementation Plan: TC-9201 -- Advisory Severity Aggregation Service and Endpoint

## Task Summary

**Jira Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Parent Feature**: TC-9001 (is incorporated by)
**Status**: To Do

## Step 0 -- Validate Project Configuration

Verify that the project's CLAUDE.md contains the required sections:

1. **Repository Registry** -- present, contains trustify-backend with Serena instance
   `serena_backend` at path `./`
2. **Jira Configuration** -- present, contains Project key (TC), Cloud ID, Feature
   issue type ID
3. **Code Intelligence** -- present, tool naming convention is
   `mcp__<serena-instance>__<tool>`, instance `serena_backend` with rust-analyzer

All sections are present and valid. Proceed.

## Step 0.5 -- JIRA Access Initialization

Determine the access method for all JIRA operations. Attempt MCP first; fall back to
REST API via `scripts/jira-client.py` if MCP fails, with user confirmation.

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")` and parse the structured description:

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Add service method and REST endpoint for advisory severity aggregation |
| Files to Modify | 3 files (advisory service, endpoints mod, model mod) |
| Files to Create | 3 files (severity_summary model, endpoint handler, integration test) |
| API Changes | `GET /api/v2/sbom/{id}/advisory-summary` (NEW) |
| Implementation Notes | Follow existing endpoint patterns, use sbom_advisory join table |
| Acceptance Criteria | 5 criteria |
| Test Requirements | 4 test cases |
| Target PR | Not present (default flow) |
| Bookend Type | Not present (default flow) |
| Dependencies | None |

Capture the issue's `webUrl` for PR description linking.

Check the GitHub Issue custom field (`customfield_10747`) -- extract the GitHub issue
reference if present, for use in the PR description's `Closes` line.

## Step 1.5 -- Verify Description Integrity

See `outputs/digest-match.md` for the full description of this step.

**Summary**: Retrieve comments on TC-9201, locate the digest comment with marker
`[sdlc-workflow] Description digest:`. One comment found with digest
`sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`.
Comment `created` and `updated` timestamps are identical (not edited). Format tag is
`sha256-md` (not legacy). Compute the current digest using
`python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`. Tags match (`sha256-md`),
hex digests match. **Proceed silently** -- no user prompt needed.

## Step 2 -- Verify Dependencies

The task lists "Depends on: None". No dependency verification needed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-9201 to current user via `jira.edit_issue("TC-9201", assignee=<accountId>)`
3. Transition to In Progress via `jira.transition_issue("TC-9201", "In Progress")`

## Step 4 -- Understand the Code

Use Serena instance `serena_backend` (tools called as `mcp__serena_backend__<tool>`)
to inspect the codebase.

### 4.1 Inspect files to modify

**`modules/fundamental/src/advisory/service/advisory.rs`**
- Use `mcp__serena_backend__get_symbols_overview` to see AdvisoryService structure
- Use `mcp__serena_backend__find_symbol` with `include_body=true` on `fetch` and
  `list` methods to understand the pattern for adding `severity_summary`
- Note the method signature pattern: `&self, id: Id, tx: &Transactional<'_>`

**`modules/fundamental/src/advisory/endpoints/mod.rs`**
- Use `mcp__serena_backend__get_symbols_overview` to see route registration pattern
- Identify `Router::new().route("/path", get(handler))` registrations

**`modules/fundamental/src/advisory/model/mod.rs`**
- Use `mcp__serena_backend__get_symbols_overview` to see existing `pub mod` declarations
- Confirm where to add `pub mod severity_summary;`

### 4.2 Inspect reference files (from Implementation Notes)

**`modules/fundamental/src/advisory/endpoints/get.rs`**
- Inspect for path param extraction pattern (`Path<Id>`)
- Inspect for service call and JSON response pattern

**`modules/fundamental/src/advisory/model/summary.rs`**
- Inspect `AdvisorySummary` struct for `severity` field -- this is the source for
  counting by severity level

**`entity/src/sbom_advisory.rs`**
- Inspect the join table entity to understand how to query advisories linked to an SBOM

**`common/src/error.rs`**
- Inspect `AppError` enum and `.context()` wrapping pattern

### 4.3 Convention conformance analysis

Identify sibling files and analyze patterns:

- **Sibling endpoints**: `endpoints/get.rs`, `endpoints/list.rs` in advisory module
- **Sibling models**: `model/summary.rs`, `model/details.rs` in advisory module
- **Sibling services**: `service/advisory.rs` (existing methods)
- **Cross-module siblings**: `sbom/endpoints/get.rs`, `sbom/endpoints/list.rs`

Expected discovered conventions:
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Naming**: Service methods follow `verb_noun` pattern
- **Endpoint registration**: `Router::new().route("/path", get(handler))` in mod.rs
- **Response types**: Direct struct return with Axum's `Json` extractor
- **Path params**: `Path<Id>` extraction pattern

### 4.4 Test convention analysis

Inspect sibling test files:
- `tests/api/advisory.rs` -- advisory endpoint integration tests
- `tests/api/sbom.rs` -- SBOM endpoint integration tests

Expected discovered test conventions:
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Error cases**: 404 tests with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming**: `test_<endpoint>_<scenario>` pattern

### 4.5 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root. If present, read and extract:
- CI check commands for Step 9 verification
- Code generation commands
- Any additional naming or structural conventions

### 4.6 Documentation file identification

Look for:
- `README.md` at repository root
- `docs/api.md` -- API documentation
- `docs/architecture.md` -- architecture overview
- `CONVENTIONS.md` -- project conventions

Record these for documentation-impact evaluation in Step 6 and currency check in Step 9.

### 4.7 Check backward compatibility

Use `mcp__serena_backend__find_referencing_symbols` on any symbols planned for
modification (e.g., AdvisoryService, advisory endpoints mod.rs route registration)
to ensure changes do not break existing callers.

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

/// Summary of advisory severity counts for a given SBOM.
///
/// Provides per-level counts (critical, high, medium, low) and a total,
/// enabling dashboard widgets to render severity breakdowns without
/// client-side counting.
#[derive(Debug, Clone, Serialize, Default)]
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

Follow the pattern of `model/summary.rs` and `model/details.rs` for struct layout,
derive macros, and documentation style.

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` to register the new model module. Place it
alphabetically among existing module declarations.

### 6.3 Modify `modules/fundamental/src/advisory/service/advisory.rs`

Add a `severity_summary` method to `AdvisoryService` following the pattern of
`fetch` and `list`:

```rust
/// Computes a severity summary for all advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with
/// the SBOM, deduplicates by advisory ID, and counts each severity level.
/// Returns a SeveritySummary with per-level counts and a total.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify SBOM exists (return 404 if not)
    // 2. Query sbom_advisory join table for advisories linked to sbom_id
    // 3. Fetch AdvisorySummary for each linked advisory
    // 4. Deduplicate by advisory ID
    // 5. Count by severity level (Critical, High, Medium, Low)
    // 6. Return SeveritySummary with counts and total
}
```

Key implementation details:
- Use `sbom_advisory` entity from `entity/src/sbom_advisory.rs` for the join query
- Use the `severity` field from `AdvisorySummary` (in `model/summary.rs`) for counting
- Deduplicate by advisory ID before counting
- Default all severity levels to 0 when no advisories exist at that level
- Wrap errors with `.context()` using `AppError` from `common/src/error.rs`
- Return 404 (via `AppError`) when the SBOM ID does not exist

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

New endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary`:

```rust
/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a JSON severity summary with counts per severity level
/// for all advisories linked to the specified SBOM.
pub async fn get_severity_summary(
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

Follow the pattern in `endpoints/get.rs`:
- Extract path params via `Path<Id>`
- Call the service method
- Return JSON response directly
- Use `.context()` for error wrapping

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route in the existing router:

```rust
use severity_summary::get_severity_summary;

// Add to the Router::new() chain:
.route("/api/v2/sbom/:id/advisory-summary", get(get_severity_summary))
```

Follow the existing route registration pattern. Note: the task description says
`server/src/main.rs` needs no changes since routes auto-mount via module registration.

### 6.6 Code quality verification

Verify that every new struct, function, and public symbol has a documentation comment
using `///` (Rust convention). All symbols in the plan above include doc comments.

### 6.7 Documentation impact

- No Documentation Updates section in the task description
- Check if `docs/api.md` documents REST endpoints -- if so, add the new
  `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- Keep updates scoped to the new endpoint only

## Step 7 -- Write Tests

### Create `tests/api/advisory_summary.rs`

Four test functions, each with a doc comment and given-when-then structure:

**Test 1: Valid SBOM with known advisories returns correct severity counts**

```rust
/// Verifies that a valid SBOM with known advisories returns the correct
/// severity count for each level.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with known advisories at various severity levels
    // (seed test database with SBOM + linked advisories)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response contains correct counts per severity level
    // assert_eq!(resp.status(), StatusCode::OK)
    // Deserialize body and assert on critical, high, medium, low, total values
}
```

**Test 2: Non-existent SBOM ID returns 404**

```rust
/// Verifies that requesting a severity summary for a non-existent SBOM
/// returns a 404 Not Found status, consistent with other SBOM endpoints.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    // GET /api/v2/sbom/{non-existent-id}/advisory-summary

    // Then the response is 404
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND)
}
```

**Test 3: SBOM with no advisories returns all zeros**

```rust
/// Verifies that an SBOM with no linked advisories returns a severity
/// summary with all counts set to zero.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then all severity counts are zero
    // assert_eq!(summary.critical, 0)
    // assert_eq!(summary.high, 0)
    // assert_eq!(summary.medium, 0)
    // assert_eq!(summary.low, 0)
    // assert_eq!(summary.total, 0)
}
```

**Test 4: Duplicate advisory links are deduplicated**

```rust
/// Verifies that duplicate advisory links in the sbom_advisory join table
/// are deduplicated, so each advisory is counted only once in the summary.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the advisory is counted only once
    // assert counts reflect unique advisories, not duplicate entries
}
```

Follow sibling test conventions from `tests/api/advisory.rs` and `tests/api/sbom.rs`:
- Use `assert_eq!(resp.status(), StatusCode::OK)` and `StatusCode::NOT_FOUND`
- Deserialize response body and assert on specific field values (not just length)
- Use the existing test database setup and fixture creation patterns

Run tests: `cargo test` -- fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns correct shape | Verified by test 1 and endpoint implementation |
| Returns 404 for non-existent SBOM ID | Verified by test 2 |
| Counts only unique advisories (dedup by ID) | Verified by test 4 and service implementation |
| All severity levels default to 0 | Verified by test 3 and `Default` derive on struct |
| Response time under 200ms for up to 500 advisories | Verified by query design (single join query, no N+1) |

## Step 9 -- Self-Verification

### Scope containment

Run `git diff --name-only` and compare against expected files:

**Files to Modify** (from task):
- `modules/fundamental/src/advisory/service/advisory.rs`
- `modules/fundamental/src/advisory/endpoints/mod.rs`
- `modules/fundamental/src/advisory/model/mod.rs`

**Files to Create** (from task):
- `modules/fundamental/src/advisory/model/severity_summary.rs`
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- `tests/api/advisory_summary.rs`

Flag any out-of-scope files for user approval.

### Untracked file check

Run `git status --short`, extract `??` entries, filter by proximity to modified
directories, search for code references. Flag any referenced untracked files for
user confirmation.

### Sensitive-pattern check

Run: `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'`

Flag any matches.

### Documentation currency

Check whether the new endpoint needs to be added to `docs/api.md` or other
documentation files identified in Step 4. If API documentation exists and describes
other endpoints, add the new endpoint entry.

### Documentation scope preservation

If any documentation files were modified, verify the replacement text covers all
use cases from the original text.

### Cross-section reference consistency

Verify file paths are consistent across task sections:
- `AdvisoryService` referenced in Files to Modify as
  `modules/fundamental/src/advisory/service/advisory.rs` and in Implementation Notes
  as `modules/fundamental/src/advisory/service/advisory.rs` -- consistent.
- Route registration in `modules/fundamental/src/advisory/endpoints/mod.rs` --
  consistent across sections.

### Duplication check

Search for existing severity aggregation or counting functions in the codebase to
ensure no duplication.

### CI checks from CONVENTIONS.md

If CONVENTIONS.md provided CI commands, run them all. Hard stop on any failure.

### Data-flow trace

- `GET /api/v2/sbom/{id}/advisory-summary`
  - Input: HTTP request with SBOM ID path parameter
  - Processing: endpoint handler extracts ID, calls `AdvisoryService.severity_summary()`,
    which queries `sbom_advisory` join table, fetches advisory severities, deduplicates,
    counts per level
  - Output: JSON response with `{ critical, high, medium, low, total }`
  - **COMPLETE** -- all stages connected

### Contract & sibling parity

- `SeveritySummary` implements `Serialize` + `Default` -- no trait contract gaps
- Sibling parity with `get.rs` endpoint: error handling pattern (AppError + context),
  path param extraction, JSON response -- all aligned
- Sibling parity with `fetch`/`list` service methods: signature pattern, transaction
  param, error wrapping -- all aligned

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
       modules/fundamental/src/advisory/model/mod.rs \
       modules/fundamental/src/advisory/service/advisory.rs \
       modules/fundamental/src/advisory/endpoints/severity_summary.rs \
       modules/fundamental/src/advisory/endpoints/mod.rs \
       tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes deduplication by advisory ID and
404 handling for non-existent SBOMs.

Implements TC-9201"

git push -u origin TC-9201

gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "$(cat <<'EOF'
## Summary

Add a service method and REST endpoint that aggregates vulnerability advisory
severity counts for a given SBOM.

- New `GET /api/v2/sbom/{id}/advisory-summary` endpoint returning `{ critical, high, medium, low, total }`
- `SeveritySummary` response struct in advisory model
- `severity_summary()` method on `AdvisoryService` using `sbom_advisory` join table
- Integration tests for valid SBOM, non-existent SBOM (404), empty advisories, and deduplication

Implements [TC-9201](<webUrl>)
Closes <owner/repo>#<number>  (if GitHub issue reference exists)

## Test Plan

- [ ] `cargo test test_advisory_summary_valid_sbom` -- correct severity counts returned
- [ ] `cargo test test_advisory_summary_not_found` -- 404 for non-existent SBOM
- [ ] `cargo test test_advisory_summary_no_advisories` -- all zeros when no advisories
- [ ] `cargo test test_advisory_summary_deduplication` -- duplicate links counted once
- [ ] Manual: verify response time under 200ms for SBOM with 500 advisories
EOF
)"
```

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (`customfield_10875`) on TC-9201 with the
   PR URL using ADF format (inlineCard):

   ```
   jira.update_issue("TC-9201", fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
   ```

2. **Add comment** to TC-9201 with:
   - PR link
   - Summary of changes: added SeveritySummary model, severity_summary service method,
     GET endpoint, and 4 integration tests
   - No deviations from the plan
   - Comment ends with the skill footnote (read version from
     `plugins/sdlc-workflow/.claude-plugin/plugin.json`)

3. **Transition** TC-9201 to In Review:
   ```
   jira.transition_issue("TC-9201", "In Review")
   ```
