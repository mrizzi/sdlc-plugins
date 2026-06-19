# Implementation Plan: TC-9201

## Task Summary

**Jira Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Status**: To Do
**Parent Feature**: TC-9001 (linked via "is incorporated by")

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md (claude-md-mock.md) contains all required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present, contains Project key (TC), Cloud ID, Feature issue type ID, Git Pull Request custom field (`customfield_10875`), GitHub Issue custom field (`customfield_10747`)
3. **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend` using `rust-analyzer`

Validation passes. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP for all JIRA operations. If MCP fails, prompt user for REST API v3 fallback choice.

## Step 1 -- Fetch and Parse Jira Task

Fetch the issue via `jira.get_issue("TC-9201")` and parse the structured description:

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM |
| Files to Modify | 3 files (advisory service, endpoints mod, model mod) |
| Files to Create | 3 files (severity_summary model, severity_summary endpoint, integration tests) |
| API Changes | `GET /api/v2/sbom/{id}/advisory-summary` (NEW) |
| Implementation Notes | Follow existing endpoint/service patterns |
| Acceptance Criteria | 5 criteria |
| Test Requirements | 4 test cases |
| Target PR | Not present (default flow) |
| Bookend Type | Not present (default flow) |
| Dependencies | None |

**GitHub Issue extraction**: Check `customfield_10747` on the fetched issue. If populated, parse the GitHub issue URL and store as `<owner>/<repo>#<number>` for the PR description.

**webUrl**: Capture the issue URL (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for use in the PR description.

## Step 1.5 -- Verify Description Integrity

(See `digest-match.md` for full details.)

1. Fetch comments via `jira.get_issue_comments("TC-9201")`
2. Locate comment with marker `[sdlc-workflow] Description digest:`
3. Found: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
4. Comment `created` and `updated` timestamps are identical -- comment was not edited
5. Parse format tag: `sha256-md`, hex digest: `a1b2c3d4...`
6. Compute current digest: `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt` outputs `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
7. Format tags match (both `sha256-md`)
8. Hex digests match
9. **Result**: Proceed silently -- no user prompt, no warning

## Step 2 -- Verify Dependencies

The task description states "Dependencies: None". No dependency verification needed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's account ID via `jira.user_info()`
2. Assign TC-9201 to current user: `jira.edit_issue("TC-9201", assignee=<account-id>)`
3. Transition to In Progress: `jira.transition_issue("TC-9201") -> In Progress`

## Step 4 -- Understand the Code

### 4.1 Serena Instance

Use `serena_backend` instance (from Repository Registry). Tools called as `mcp__serena_backend__<tool>`.

Note limitation: rust-analyzer may take 30-60 seconds to index on first use.

### 4.2 Inspect Files to Modify

**File 1: `modules/fundamental/src/advisory/service/advisory.rs`**
- `mcp__serena_backend__get_symbols_overview` to see AdvisoryService structure
- `mcp__serena_backend__find_symbol("fetch", include_body=true)` to understand existing service method pattern
- `mcp__serena_backend__find_symbol("list", include_body=true)` for the list method pattern
- Note: new `severity_summary` method takes `&self, sbom_id: Id, tx: &Transactional<'_>`

**File 2: `modules/fundamental/src/advisory/endpoints/mod.rs`**
- `mcp__serena_backend__get_symbols_overview` to see route registration pattern
- Note: uses `Router::new().route("/path", get(handler))` pattern

**File 3: `modules/fundamental/src/advisory/model/mod.rs`**
- `mcp__serena_backend__get_symbols_overview` to see existing module registrations
- Note: need to add `pub mod severity_summary;`

### 4.3 Inspect Reference Files

**`modules/fundamental/src/advisory/endpoints/get.rs`** -- reference for endpoint pattern:
- `mcp__serena_backend__get_symbols_overview` and `find_symbol` to see Path<Id> extraction, service call, JSON return

**`modules/fundamental/src/advisory/model/summary.rs`** -- reference for AdvisorySummary:
- `mcp__serena_backend__find_symbol("AdvisorySummary", include_body=true)` to see severity field

**`entity/src/sbom_advisory.rs`** -- join table for SBOM-Advisory relationship:
- `mcp__serena_backend__get_symbols_overview` to understand join entity structure

**`common/src/error.rs`** -- reference for error handling:
- `mcp__serena_backend__find_symbol("AppError", include_body=true)` to see error enum and `.context()` pattern

### 4.4 Check Backward Compatibility

- `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to ensure adding a method won't break existing callers
- `mcp__serena_backend__find_referencing_symbols` on the advisory endpoints `mod.rs` to ensure route registration changes are safe

### 4.5 CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at repository root (path `./` from Registry):
- `mcp__serena_backend__list_dir("./")` or Read `./CONVENTIONS.md`
- The repo-backend.md indicates `CONVENTIONS.md` exists at root
- Read and follow conventions; extract CI check commands for Step 9

### 4.6 Convention Conformance Analysis

**Sibling analysis for endpoints:**
- Inspect `endpoints/get.rs` and `endpoints/list.rs` in the advisory module
- Note patterns: `Path<Id>` extraction, `Result<T, AppError>` return, `.context()` wrapping, `Json` response

**Sibling analysis for models:**
- Inspect `model/summary.rs` and `model/details.rs` in the advisory module
- Note patterns: struct with `#[derive(Serialize, Deserialize)]`, field types, documentation

**Sibling analysis for services:**
- Inspect existing `fetch` and `list` methods in `service/advisory.rs`
- Note patterns: `&self`, `Transactional` parameter, query building, error handling

### 4.7 Test Convention Analysis

- Inspect `tests/api/advisory.rs` and `tests/api/sbom.rs`
- Note patterns: assertion style (`assert_eq!(resp.status(), StatusCode::OK)`), body deserialization, 404 testing, test naming
- Check for parameterized test usage (e.g., `#[rstest]`)

### 4.8 Documentation File Identification

- `README.md` at repo root
- `docs/api.md` referenced in CLAUDE.md -- may need update for new endpoint
- `docs/architecture.md` -- likely no update needed

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
/// Summary of advisory severity counts for an SBOM.
///
/// Aggregates the number of linked advisories by severity level,
/// enabling dashboard widgets to render severity breakdowns.
#[derive(Clone, Debug, Default, Serialize, Deserialize, utoipa::ToSchema)]
pub struct SeveritySummary {
    /// Count of critical-severity advisories.
    pub critical: u32,
    /// Count of high-severity advisories.
    pub high: u32,
    /// Count of medium-severity advisories.
    pub medium: u32,
    /// Count of low-severity advisories.
    pub low: u32,
    /// Total count of unique advisories across all severity levels.
    pub total: u32,
}
```

Follow the pattern from `model/summary.rs` for derive macros and documentation style.

### 6.2 Register the model module in `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` to expose the new model, following existing module registration pattern.

### 6.3 Add `severity_summary` method to AdvisoryService in `modules/fundamental/src/advisory/service/advisory.rs`

```rust
/// Computes advisory severity counts for a given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories linked to the
/// specified SBOM, deduplicates by advisory ID, and counts by severity level.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Query sbom_advisory join table for the given SBOM ID
    // 2. Join with advisory table to get severity field
    // 3. Deduplicate by advisory ID
    // 4. Count by severity level (Critical, High, Medium, Low)
    // 5. Return SeveritySummary with counts and total
}
```

Follow the `fetch` and `list` method patterns for:
- Using SeaORM query builder
- Transaction handling via `Transactional`
- Error wrapping with `.context()`
- Return type `Result<T, AppError>`

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler:

```rust
/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity breakdown of advisories linked to the specified SBOM.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    State(service): State<AdvisoryService>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("fetching advisory severity summary")?;
    Ok(Json(summary))
}
```

Follow the pattern from `endpoints/get.rs`:
- Extract path params via `Path<Id>`
- Call service method
- Return JSON with `Json` wrapper
- Error handling with `.context()`

### 6.5 Register the route in `modules/fundamental/src/advisory/endpoints/mod.rs`

Add the new route following existing `Router::new().route()` pattern:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

### 6.6 Documentation Impact

- Check if `docs/api.md` documents existing endpoints -- if so, add entry for `GET /api/v2/sbom/{id}/advisory-summary`
- `server/src/main.rs` needs no changes (routes auto-mount via module registration per task description)

### 6.7 Code Quality Checks

- Every new struct, function, and method has documentation comments (using `///` Rust convention)
- Public API symbols have descriptions of parameters and return values where not obvious from the name

## Step 7 -- Write Tests

### Create `tests/api/advisory_summary.rs`

Follow conventions discovered from `tests/api/advisory.rs` and `tests/api/sbom.rs`:

**Test 1: Valid SBOM with known advisories returns correct severity counts**

```rust
/// Verifies that an SBOM with linked advisories of known severities returns correct per-level counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with advisories at known severity levels
    // (seed test DB with SBOM + linked advisories: 2 Critical, 1 High, 0 Medium, 3 Low)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response contains correct counts
    // assert_eq!(resp.status(), StatusCode::OK)
    // assert_eq!(body.critical, 2)
    // assert_eq!(body.high, 1)
    // assert_eq!(body.medium, 0)
    // assert_eq!(body.low, 3)
    // assert_eq!(body.total, 6)
}
```

**Test 2: Non-existent SBOM ID returns 404**

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    // GET /api/v2/sbom/{non_existent_id}/advisory-summary

    // Then the response is 404
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND)
}
```

**Test 3: SBOM with no advisories returns all zeros**

```rust
/// Verifies that an SBOM with no linked advisories returns a summary with all zero counts.
#[tokio::test]
async fn test_advisory_summary_empty() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then all severity counts are zero
    // assert_eq!(body.critical, 0)
    // assert_eq!(body.high, 0)
    // assert_eq!(body.medium, 0)
    // assert_eq!(body.low, 0)
    // assert_eq!(body.total, 0)
}
```

**Test 4: Duplicate advisory links are deduplicated**

```rust
/// Verifies that duplicate advisory links in the join table are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with duplicate links to the same advisory
    // (same advisory ID appears multiple times in sbom_advisory)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the advisory is counted only once
    // assert_eq!(body.total, expected_unique_count)
}
```

Run tests: `cargo test` -- fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification Method |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns correct JSON shape | Test 1 validates response structure and values |
| Returns 404 when SBOM ID does not exist | Test 2 validates 404 response |
| Counts only unique advisories (deduplicates by advisory ID) | Test 4 validates deduplication |
| All severity levels default to 0 when no advisories exist | Test 3 validates zero defaults |
| Response time under 200ms for SBOMs with up to 500 advisories | Code review of query efficiency; ensure single SQL query with GROUP BY rather than N+1 |

## Step 9 -- Self-Verification

### Scope Containment

Run `git diff --name-only` and verify all modified/created files match:

**Expected modified files:**
- `modules/fundamental/src/advisory/service/advisory.rs`
- `modules/fundamental/src/advisory/endpoints/mod.rs`
- `modules/fundamental/src/advisory/model/mod.rs`

**Expected created files:**
- `modules/fundamental/src/advisory/model/severity_summary.rs`
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- `tests/api/advisory_summary.rs`

Flag any out-of-scope files for user approval.

### Untracked File Check

Run `git status --short`, identify `??` entries in implementation directories, search for code references, and flag for review.

### Sensitive-Pattern Check

```bash
git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
```

No secrets expected -- flag if any found.

### Documentation Currency

Check `docs/api.md` -- if it lists endpoints, verify the new endpoint is documented. Update if needed.

### Cross-Section Reference Consistency

Verify file paths are consistent across task sections:
- `AdvisoryService` referenced in both Files to Modify (`advisory/service/advisory.rs`) and Implementation Notes (`advisory/service/advisory.rs`) -- consistent
- Endpoints `mod.rs` referenced consistently
- `AdvisorySummary.severity` field referenced in Implementation Notes matches `model/summary.rs`

### Duplication Check

Search for existing severity aggregation logic in the codebase to ensure no duplication.

### Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary` request received -> path param extracted -> `AdvisoryService.severity_summary()` called -> queries `sbom_advisory` join table -> aggregates by severity -> returns `SeveritySummary` as JSON -- **COMPLETE**

### Contract & Sibling Parity

- `SeveritySummary` follows the same derive macro pattern as `AdvisorySummary` and `SbomSummary`
- `get_severity_summary` handler follows same pattern as `get.rs` handlers
- `severity_summary` service method follows same pattern as `fetch` and `list` methods
- Error handling consistent: `Result<T, AppError>` with `.context()`

### CI Checks

Run CI check commands extracted from `CONVENTIONS.md` (if found in Step 4). Hard stop on any failure.

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs
git add modules/fundamental/src/advisory/model/mod.rs
git add modules/fundamental/src/advisory/service/advisory.rs
git add modules/fundamental/src/advisory/endpoints/severity_summary.rs
git add modules/fundamental/src/advisory/endpoints/mod.rs
git add tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns severity
counts (critical, high, medium, low, total) for advisories linked to an SBOM.
Includes SeveritySummary model, AdvisoryService.severity_summary() method,
and integration tests for valid SBOM, 404, empty, and deduplication cases.

Implements TC-9201"

git push -u origin TC-9201
```

Create PR targeting the `main` branch:

```bash
gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "## Summary

Add a new REST endpoint `GET /api/v2/sbom/{id}/advisory-summary` that aggregates
vulnerability advisory severity counts for a given SBOM, returning counts per
severity level (Critical, High, Medium, Low) and a total.

### Changes
- New `SeveritySummary` response struct in `advisory/model/severity_summary.rs`
- New `severity_summary` method on `AdvisoryService`
- New endpoint handler in `advisory/endpoints/severity_summary.rs`
- Route registration in `advisory/endpoints/mod.rs`
- Integration tests covering valid SBOM, 404, empty SBOM, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)

[Closes <owner>/<repo>#<number> if GitHub Issue field was populated]"
```

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (`customfield_10875`) on TC-9201 with the PR URL in ADF format:

```
jira.update_issue("TC-9201", fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
```

2. **Add a comment** to TC-9201 with:
   - PR link
   - Summary of changes: added `SeveritySummary` model, `severity_summary` service method, GET endpoint at `/api/v2/sbom/{id}/advisory-summary`, and 4 integration tests
   - No deviations from the plan
   - Comment ends with the skill footnote (version read from `plugins/sdlc-workflow/.claude-plugin/plugin.json`)

3. **Transition** TC-9201 to In Review:

```
jira.transition_issue("TC-9201") -> In Review
```
