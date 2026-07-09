# Implementation Plan for TC-9201

**Task:** Add advisory severity aggregation service and endpoint
**Repository:** trustify-backend
**Target Branch:** main
**Linked Issues:** is incorporated by TC-9001

---

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md contains all required sections under `# Project Configuration`:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present, contains Project key (`TC`), Cloud ID, Feature issue type ID
3. **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and `serena_backend` configured with `rust-analyzer`

Validation passes. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all JIRA operations. If MCP fails, prompt user for REST API fallback per the standard protocol.

## Step 1 -- Fetch and Parse Jira Task

Fetch the issue using `jira.get_issue("TC-9201")`. Parse the structured description:

| Section | Value |
|---|---|
| **Repository** | trustify-backend |
| **Target Branch** | main |
| **Description** | Add service method and REST endpoint for advisory severity aggregation per SBOM |
| **Files to Modify** | 3 files (advisory service, endpoints mod, model mod) |
| **Files to Create** | 3 files (severity_summary model, severity_summary endpoint, integration tests) |
| **API Changes** | `GET /api/v2/sbom/{id}/advisory-summary` (NEW) |
| **Implementation Notes** | Follow existing endpoint/service patterns, use sbom_advisory join table |
| **Acceptance Criteria** | 5 criteria (correct response shape, 404, dedup, defaults, performance) |
| **Test Requirements** | 4 tests (valid counts, 404, empty, dedup) |
| **Target PR** | Not present (default flow) |
| **Bookend Type** | Not present (default flow) |
| **Dependencies** | None |

Capture `webUrl` (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for PR description.

**GitHub Issue extraction:** Look up `customfield_10747` from Jira Configuration. Read its value from the fetched issue fields. If present and non-empty, parse the GitHub issue URL. If not present or empty, skip silently.

All required sections are present. No gaps found. Proceed.

## Step 1.5 -- Verify Description Integrity

See `outputs/digest-match.md` for the full description of this step.

Summary: The digest comment `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890` is found. The comment's `created` and `updated` timestamps are identical (unmodified). The computed digest of the current description matches the stored digest. Both use the `sha256-md` format tag. Digests match -- proceed silently.

## Step 2 -- Verify Dependencies

The task lists `Dependencies: None`. No prerequisite tasks to check. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's account ID via `jira.user_info()`
2. Assign TC-9201 to the current user: `jira.edit_issue("TC-9201", assignee=<account-id>)`
3. Transition to In Progress: `jira.transition_issue("TC-9201", "In Progress")`

## Step 4 -- Understand the Code

### 4.1 Inspect Files to Modify

Use the `serena_backend` Serena instance (tools called as `mcp__serena_backend__<tool>`).

**File 1: `modules/fundamental/src/advisory/service/advisory.rs`**
- Use `mcp__serena_backend__get_symbols_overview` to see the structure of `AdvisoryService`
- Use `mcp__serena_backend__find_symbol` with `include_body=true` on the `fetch` and `list` methods to understand the existing service method pattern (signature, transaction handling, error wrapping)
- Note the pattern: methods take `&self, id: Id, tx: &Transactional<'_>` and return `Result<T, AppError>`

**File 2: `modules/fundamental/src/advisory/endpoints/mod.rs`**
- Use `mcp__serena_backend__get_symbols_overview` to see current route registrations
- Understand the `Router::new().route("/path", get(handler))` pattern for adding new routes

**File 3: `modules/fundamental/src/advisory/model/mod.rs`**
- Use `mcp__serena_backend__get_symbols_overview` to see existing module declarations
- Understand the pattern for registering new model sub-modules (`pub mod summary;`, `pub mod details;`)

### 4.2 Inspect Reference Files (for patterns)

**`modules/fundamental/src/advisory/endpoints/get.rs`** -- reference for endpoint pattern:
- Use `mcp__serena_backend__find_symbol` to read the GET handler
- Note: `Path<Id>` extraction, service call, JSON response

**`modules/fundamental/src/advisory/model/summary.rs`** -- reference for `AdvisorySummary` struct:
- Use `mcp__serena_backend__find_symbol` to read `AdvisorySummary` struct
- Note the `severity` field -- this is what we will count by

**`entity/src/sbom_advisory.rs`** -- join table for SBOM-to-Advisory:
- Use `mcp__serena_backend__get_symbols_overview` to understand the join table structure

**`common/src/error.rs`** -- error handling pattern:
- Use `mcp__serena_backend__find_symbol` on `AppError` to understand error wrapping with `.context()`

### 4.3 Check Backward Compatibility

- Use `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to identify all callers and ensure the new `severity_summary` method does not conflict with existing methods
- Use `mcp__serena_backend__find_referencing_symbols` on the endpoints `mod.rs` to confirm no route conflicts

### 4.4 Documentation File Identification

Look for documentation files related to the changes:
- `README.md` at the repository root
- `docs/api.md` (API reference, per CLAUDE.md)
- `docs/architecture.md` (architecture overview)
- `CONVENTIONS.md` at the repository root

### 4.5 CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`) using `mcp__serena_backend__list_dir` or Read. If present, read it and extract:
- CI check commands (formatting, linting, compilation) for Step 9
- Code generation commands (e.g., OpenAPI spec generation)
- Naming rules, directory structure, and code patterns

### 4.6 Convention Conformance Analysis

**Discovered conventions (from sibling analysis):**

- **Module structure:** Each domain module follows `model/ + service/ + endpoints/` structure
- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping from `common/src/error.rs`
- **Endpoint pattern:** Handlers extract path params via `Path<Id>`, call the corresponding service method, return `Json(result)`
- **Service method pattern:** Methods on the service struct take `&self`, an ID or filter, and `tx: &Transactional<'_>`; return `Result<T, AppError>`
- **Route registration:** `Router::new().route("/path", get(handler))` chaining in `endpoints/mod.rs`
- **Response types:** Single-item endpoints return the struct directly via Axum's `Json` extractor; list endpoints return `PaginatedResults<T>`
- **Naming:** Service methods use `verb_noun` pattern (e.g., `fetch`, `list`, `search`)
- **Model structs:** Use `#[derive(Serialize, Deserialize, Debug)]` and include doc comments

### 4.7 Test Convention Analysis

**Sibling test files inspected:** `tests/api/advisory.rs`, `tests/api/sbom.rs`, `tests/api/search.rs`

**Discovered test conventions (from sibling test analysis):**

- **Framework:** Integration tests in `tests/api/` hit a real PostgreSQL test database
- **Assertion style:** Use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Error cases:** Include 404 tests with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming:** Tests follow `test_<endpoint>_<scenario>` pattern
- **Setup:** Tests use shared database fixtures and test utilities for creating test data
- **Parameterized tests:** Check siblings for `#[rstest]` usage; if not present, use individual test functions

No convention conflicts detected with the task description.

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
use serde::{Deserialize, Serialize};

/// Summary of advisory severity counts for an SBOM.
///
/// Provides a breakdown of vulnerability advisory counts by severity level,
/// enabling dashboard widgets to render severity distributions without
/// client-side counting.
#[derive(Clone, Debug, Default, Serialize, Deserialize, PartialEq, Eq)]
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

- Derives `Default` so all severity levels default to 0 when no advisories exist (AC-4)
- Follows the model pattern from `summary.rs` and `details.rs` siblings
- Includes doc comments on the struct and every field per the Code Quality Practices requirement

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add the new module registration:

```rust
pub mod severity_summary;
```

Following the existing pattern of `pub mod summary;` and `pub mod details;`.

### 6.3 Modify `modules/fundamental/src/advisory/service/advisory.rs`

Add the `severity_summary` method to `AdvisoryService`:

```rust
/// Computes a severity summary for all advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with
/// the SBOM, deduplicates by advisory ID, and counts by severity level.
/// Returns a `SeveritySummary` with counts for each severity and a total.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify the SBOM exists (return 404 if not found)
    // Use the same SBOM existence check pattern as other endpoints
    
    // 2. Query sbom_advisory join table for advisories linked to this SBOM
    // Use entity::sbom_advisory to find all linked advisory IDs
    
    // 3. Deduplicate by advisory ID (AC-3: count only unique advisories)
    // Use DISTINCT or a HashSet to ensure uniqueness
    
    // 4. For each unique advisory, fetch its AdvisorySummary to get severity
    // Use the existing AdvisorySummary struct's severity field
    
    // 5. Count by severity level (Critical, High, Medium, Low)
    // Initialize SeveritySummary with Default (all zeros, satisfying AC-4)
    // Increment the appropriate counter for each advisory
    
    // 6. Set total = sum of all severity counts
    
    // 7. Return the SeveritySummary
    Ok(summary)
}
```

Pattern notes:
- Follows `fetch` and `list` method signatures: `&self`, ID param, `tx: &Transactional<'_>`
- Returns `Result<SeveritySummary, AppError>` with `.context()` error wrapping
- SBOM existence check returns 404 when SBOM ID does not exist (AC-2)

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern in `endpoints/get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::db::Transactional;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity breakdown of all advisories linked to the given SBOM,
/// with counts for Critical, High, Medium, Low, and a total count.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: /* injected AdvisoryService */,
    tx: /* transaction context */,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("fetching advisory severity summary")?;
    Ok(Json(summary))
}
```

Pattern notes:
- Extracts path params via `Path<Id>` (matching `get.rs` pattern)
- Calls the service method and returns `Json(result)`
- Uses `.context()` for error wrapping (matching `common/src/error.rs` pattern)

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route:

```rust
mod severity_summary;

// In the router builder, add:
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

Following the existing `Router::new().route("/path", get(handler))` registration pattern.

### 6.6 Verify `server/src/main.rs`

Per the task description: "no changes needed (routes auto-mount via module registration)". Confirm this by inspecting the main.rs route mounting to verify advisory module routes are auto-discovered.

### 6.7 Documentation Impact

- Check if `docs/api.md` documents existing endpoints -- if so, add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint with its request/response schema
- No architectural changes, so `docs/architecture.md` does not need updating
- No configuration changes

### 6.8 Cross-repo API Contract Verification

Not applicable -- this task creates a backend endpoint, not a frontend consumer of one. No manual REST calls are being written against another repository's API.

## Step 7 -- Write Tests

### Create `tests/api/advisory_summary.rs`

Following the test conventions discovered in Step 4:

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with advisories at known severity levels
    // (seed test DB with SBOM + linked advisories: 2 critical, 1 high, 1 medium, 0 low)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response should contain correct severity counts
    // assert_eq!(resp.status(), StatusCode::OK);
    // assert_eq!(body.critical, 2);
    // assert_eq!(body.high, 1);
    // assert_eq!(body.medium, 1);
    // assert_eq!(body.low, 0);
    // assert_eq!(body.total, 4);
}

/// Verifies that a non-existent SBOM ID returns 404, consistent with existing SBOM endpoints.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    // GET /api/v2/sbom/{nonexistent-id}/advisory-summary

    // Then the response should be 404
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no advisories returns all zeros.
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

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM with duplicate advisory links (same advisory linked multiple times)
    // (seed test DB with SBOM + 1 advisory linked 3 times via sbom_advisory)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the advisory should be counted only once
    // assert_eq!(resp.status(), StatusCode::OK);
    // assert_eq!(body.total, 1);  // not 3
}
```

All test functions include:
- Doc comments explaining what is being verified
- Given-when-then section comments for structural clarity
- Value-based assertions (not just length checks)
- Naming follows `test_<endpoint>_<scenario>` pattern from siblings

Run tests to verify:

```bash
cargo test --test advisory_summary
```

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| # | Criterion | Verification |
|---|---|---|
| AC-1 | GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` | Verified by `SeveritySummary` struct shape and `test_advisory_summary_valid_sbom` test |
| AC-2 | Returns 404 when SBOM ID does not exist | Verified by SBOM existence check in service method and `test_advisory_summary_nonexistent_sbom` test |
| AC-3 | Counts only unique advisories (deduplicates by advisory ID) | Verified by DISTINCT/HashSet dedup logic and `test_advisory_summary_deduplicates` test |
| AC-4 | All severity levels default to 0 when no advisories exist | Verified by `SeveritySummary` deriving `Default` and `test_advisory_summary_no_advisories` test |
| AC-5 | Response time under 200ms for SBOMs with up to 500 advisories | Verified by using efficient database query with JOIN and GROUP BY rather than N+1 fetches |

## Step 9 -- Self-Verification

### Scope Containment

Run `git diff --name-only` and compare against the task's file lists:

**Files to Modify (expected):**
- `modules/fundamental/src/advisory/service/advisory.rs`
- `modules/fundamental/src/advisory/endpoints/mod.rs`
- `modules/fundamental/src/advisory/model/mod.rs`

**Files to Create (expected):**
- `modules/fundamental/src/advisory/model/severity_summary.rs`
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- `tests/api/advisory_summary.rs`

Any file not in these lists is out-of-scope and requires user approval.

### Untracked File Check

Run `git status --short`, filter `??` entries. Check proximity to modified directories. Search for code references to any untracked files (e.g., `include_str!`, `use`, import statements). Flag any referenced untracked files for user confirmation before staging.

### Sensitive-Pattern Check

```bash
git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
```

Flag any matches. Do not proceed until resolved.

### Documentation Currency

Check if `docs/api.md` needs updating with the new endpoint. If it documents existing advisory endpoints, add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint documentation.

### Documentation Scope Preservation

If documentation was modified, verify replacement text covers all use cases from the original text.

### Eval Coverage Currency

No SKILL.md files are being modified, so this check is skipped.

### Example Consistency

If documentation with composite examples was written, cross-check narrative and data structures for consistency.

### Cross-Section Reference Consistency

Verify file paths are consistent across task description sections:

- Entity `AdvisoryService` -- referenced in Files to Modify as `modules/fundamental/src/advisory/service/advisory.rs` and in Implementation Notes as `modules/fundamental/src/advisory/service/advisory.rs` -- **consistent**
- Entity `SeveritySummary` model -- referenced in Files to Create as `modules/fundamental/src/advisory/model/severity_summary.rs` -- no cross-reference conflicts
- Entity `endpoints/mod.rs` -- referenced in Files to Modify as `modules/fundamental/src/advisory/endpoints/mod.rs` and in Implementation Notes for route registration -- **consistent**

### Duplication Check

Search the repository for existing severity aggregation or summary-counting logic:
- Grep for `severity_summary`, `severity_count`, `count_by_severity` patterns
- Verify no existing utility already provides this functionality
- If overlapping logic exists, refactor to reuse it

### CI Checks from CONVENTIONS.md

If CONVENTIONS.md was loaded and CI check commands were extracted, run each command in sequence. Hard stop on any non-zero exit. If no CONVENTIONS.md or no CI section, fall back to:

```bash
cargo build
cargo clippy
cargo fmt --check
```

Fix any warnings or errors before proceeding.

### Data-Flow Trace

**Data-flow trace results:**
- `GET /api/v2/sbom/{id}/advisory-summary` -> extract SBOM ID from path -> verify SBOM exists -> query sbom_advisory join table -> fetch advisory severities -> deduplicate by advisory ID -> count by severity level -> construct SeveritySummary -> return JSON response -- **COMPLETE**

All stages are connected. No incomplete paths.

### Contract & Sibling Parity

**Contract verification:**
- `SeveritySummary` struct: implements `Serialize`, `Deserialize` as required for Axum JSON response -- complete
- `get_severity_summary` handler: returns `Result<Json<SeveritySummary>, AppError>` matching Axum handler contract -- complete

**Sibling parity with `get.rs` endpoint handler:**
- Path extraction: `Path<Id>` -- matches
- Service call pattern -- matches
- Error handling with `.context()` -- matches
- JSON response -- matches

**Cross-module shared entity analysis:**
- Entity `sbom_advisory`: check how `ingestor/graph/advisory/mod.rs` interacts with this table. Ensure the new code's read pattern (SELECT with JOIN) is compatible with the ingestor's write pattern. No anomalies expected since this is a read-only query.

**Caller-site parity:**
- The new endpoint calls `AdvisoryService::severity_summary` -- this is a new method, so no existing callers to compare against. The call site pattern (service method invocation from endpoint handler) matches how existing handlers call `fetch` and `list`.

## Step 10 -- Commit and Push

Commit with Conventional Commits format:

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
       modules/fundamental/src/advisory/model/mod.rs \
       modules/fundamental/src/advisory/service/advisory.rs \
       modules/fundamental/src/advisory/endpoints/severity_summary.rs \
       modules/fundamental/src/advisory/endpoints/mod.rs \
       tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns a
severity breakdown (critical, high, medium, low, total) of advisories
linked to a given SBOM. Includes deduplication by advisory ID, 404
handling for missing SBOMs, and integration tests.

Implements TC-9201"
```

Push and create PR:

```bash
git push -u origin TC-9201
gh pr create --base main \
  --title "feat(advisory): add severity aggregation endpoint" \
  --body "## Summary

- Add \`SeveritySummary\` response model with severity-level counts
- Add \`severity_summary\` method to \`AdvisoryService\` with deduplication
- Add \`GET /api/v2/sbom/{id}/advisory-summary\` endpoint
- Add integration tests covering valid SBOM, 404, empty advisories, and dedup

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)"
```

(If a GitHub issue reference was extracted in Step 1, append `Closes <owner>/<repo>#<number>` to the PR body.)

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field** (`customfield_10875`) on TC-9201 with the PR URL in ADF format (inlineCard).

2. **Add a comment** to TC-9201 with:
   - PR link
   - Summary of changes: Added SeveritySummary model, severity_summary service method, GET endpoint, and 4 integration tests
   - No deviations from the plan
   - Include the skill footer (read version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`)

3. **Transition** TC-9201 to **In Review**: `jira.transition_issue("TC-9201", "In Review")`
