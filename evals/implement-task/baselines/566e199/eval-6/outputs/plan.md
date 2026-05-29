# Implementation Plan: TC-9201

## Task Summary

**Jira Issue**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Dependencies**: None
**Bookend Type**: None
**Target PR**: None

## Step 0 -- Validate Project Configuration

Verify the project's CLAUDE.md contains all required Project Configuration sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` and path `./`
2. **Jira Configuration** -- present, contains Project key (`TC`), Cloud ID, Feature issue type ID, Git Pull Request custom field (`customfield_10875`), and GitHub Issue custom field (`customfield_10747`)
3. **Code Intelligence** -- present, documents `serena_backend` instance with rust-analyzer

All required sections are present. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all JIRA operations. If MCP fails, prompt the user with the three options (REST API fallback, skip, or retry) as specified in the skill definition.

## Step 1 -- Fetch and Parse Jira Task

Fetch the issue via `jira.get_issue(TC-9201)` and parse the structured description.

### Parsed Sections

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. The endpoint returns a summary with counts per severity level (Critical, High, Medium, Low) and a total, enabling dashboard widgets to render severity breakdowns without client-side counting.
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
- **Implementation Notes**: Follow existing endpoint patterns, use AdvisoryService pattern, use `sbom_advisory` join table, use `AdvisorySummary.severity` field, register route in endpoints `mod.rs`, return `AppError` with `.context()`, return struct directly via Axum's `Json` extractor
- **Acceptance Criteria**: 5 criteria (see below)
- **Test Requirements**: 4 test cases (see below)
- **Dependencies**: None
- **Target PR**: None (not present)
- **Bookend Type**: None (not present)
- **Review Context**: None (not present)

### GitHub Issue Extraction

The GitHub Issue custom field (`customfield_10747`) would be read from the fetched issue's fields. If present, parse the GitHub issue URL to extract `owner/repo#number` for use in the PR description's `Closes` line. If empty, skip silently.

### Capture webUrl

Capture the issue's `webUrl` field (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for use in the PR description.

## Step 1.5 -- Verify Description Integrity

1. Fetch comments via `jira.get_issue_comments(TC-9201)`
2. Locate the comment with marker `[sdlc-workflow] Description digest:` -- one comment found with digest `sha256:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
3. Check comment timestamps: `created` and `updated` are identical -- comment was not edited, no warning needed
4. Compute SHA-256 of the current description using `scripts/sha256-digest.py`
5. Compare digests: **MATCH** -- proceed silently, no user prompt, no delay

## Step 2 -- Verify Dependencies

No dependencies listed. Skip.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's account ID via `jira.user_info()`
2. Assign TC-9201 to current user via `jira.edit_issue(TC-9201, assignee=<account-id>)`
3. Transition TC-9201 to "In Progress" via `jira.transition_issue`

## Step 4 -- Understand the Code

### 4.1 Code Inspection via Serena (serena_backend)

Use the `serena_backend` Serena instance (from Repository Registry) to inspect the codebase.

**Overview of files to modify:**

1. `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/service/advisory.rs`
   - Understand `AdvisoryService` struct and existing methods (`fetch`, `list`, `search`)
   - Note method signatures, parameter types, return types, transaction handling
2. `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/mod.rs`
   - Understand current route registration pattern
3. `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/mod.rs`
   - Understand module registration pattern

**Read specific symbols:**

4. `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::fetch` to understand the exact method pattern (self reference, parameters, error handling, return type)
5. `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::list` for comparison
6. `mcp__serena_backend__find_symbol` with `include_body=true` on existing endpoint handler in `modules/fundamental/src/advisory/endpoints/get.rs` to understand handler pattern

**Check backward compatibility:**

7. `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to understand all callers and ensure new method doesn't conflict

**Non-symbolic search:**

8. `mcp__serena_backend__search_for_pattern` for `sbom_advisory` to understand the join table structure
9. `mcp__serena_backend__search_for_pattern` for `severity` in the advisory model to understand the severity field

### 4.2 Sibling File Inspection

**Endpoint siblings** (for convention conformance):
- `modules/fundamental/src/advisory/endpoints/get.rs` -- GET handler for single advisory
- `modules/fundamental/src/advisory/endpoints/list.rs` -- GET handler for advisory list
- `modules/fundamental/src/sbom/endpoints/get.rs` -- GET handler in sibling module (SBOM)

Use `get_symbols_overview` on 2-3 of these to extract conventions.

**Model siblings:**
- `modules/fundamental/src/advisory/model/summary.rs` -- AdvisorySummary struct
- `modules/fundamental/src/advisory/model/details.rs` -- AdvisoryDetails struct

**Service siblings:**
- `modules/fundamental/src/sbom/service/sbom.rs` -- SbomService for cross-module comparison

### 4.3 CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). The repo structure indicates it exists. Read it and extract:
- CI check commands (for Step 9 verification)
- Code generation commands (if any)
- Any explicit naming, structure, or pattern conventions

### 4.4 Convention Conformance Analysis

**Expected discovered conventions (from sibling analysis):**
- **Error handling:** All handlers and service methods use `Result<T, AppError>` with `.context()` for wrapping
- **Naming:** Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`)
- **Endpoint pattern:** Extract path params via `Path<Id>`, call service, return `Json(result)`
- **Route registration:** `Router::new().route("/path", get(handler))` pattern in `endpoints/mod.rs`
- **Response types:** List endpoints return `PaginatedResults<T>`; single-item endpoints return the model directly
- **Module registration:** Each model has a `pub mod <name>;` in `model/mod.rs`
- **Transaction handling:** Service methods take `&Transactional<'_>` parameter

### 4.5 Test Convention Analysis

**Sibling test files:**
- `tests/api/advisory.rs` -- advisory endpoint integration tests
- `tests/api/sbom.rs` -- SBOM endpoint integration tests

Use `get_symbols_overview` on these to discover test conventions.

**Expected discovered test conventions:**
- **Assertion style:** `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Response validation:** Validate specific field values, not just counts
- **Error cases:** Include 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming:** `test_<endpoint>_<scenario>` pattern
- **Setup:** Tests use a real PostgreSQL test database with fixture data
- **Test organization:** Grouped by endpoint in separate files under `tests/api/`

### 4.6 Documentation File Identification

Related documentation files:
- `docs/api.md` -- REST API reference, may need updating with new endpoint
- `docs/architecture.md` -- system architecture, unlikely to need changes
- `README.md` -- repository readme

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
use utoipa::ToSchema;

/// Summary of advisory severity counts for an SBOM.
///
/// Provides aggregated counts of linked advisories grouped by severity level,
/// enabling dashboard widgets to render severity breakdowns without client-side counting.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
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

### 6.2 Register model module in `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` to expose the new model module.

### 6.3 Add `severity_summary` method to `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`

Add a new method following the existing `fetch` and `list` patterns:

```rust
/// Computes a severity summary for all unique advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with the SBOM,
/// deduplicates by advisory ID, and counts occurrences by severity level.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Query sbom_advisory join table for advisories linked to this SBOM
    // Join with advisory table to get severity field
    // Deduplicate by advisory ID
    // Count by severity level (Critical, High, Medium, Low)
    // Return SeveritySummary with counts and total
}
```

Key implementation details:
- Use `sbom_advisory` entity to find linked advisories
- Join with the advisory entity to access the `severity` field from `AdvisorySummary`
- Use `DISTINCT` or equivalent to deduplicate by advisory ID
- Group and count by severity level
- Default all counts to 0 when no advisories exist at that level
- Wrap errors with `.context("Failed to compute severity summary for SBOM")`
- Verify the SBOM exists first; return 404 `AppError` if not found

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern in `endpoints/get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

/// Handles GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity summary with counts of advisories linked to the specified
/// SBOM, grouped by severity level (Critical, High, Medium, Low).
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: Extension<AdvisoryService>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service.severity_summary(id, &tx).await
        .context("Error fetching advisory severity summary")?;
    Ok(Json(summary))
}
```

### 6.5 Register route in `modules/fundamental/src/advisory/endpoints/mod.rs`

Add the new route to the router following the existing registration pattern:

```rust
pub mod severity_summary;

// In the router builder:
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

### 6.6 Cross-repo API Contract Verification

Not applicable -- this task creates a new backend endpoint, not a frontend consuming one. No cross-repo verification needed.

### 6.7 Code Quality Practices

- All new structs (`SeveritySummary`) have documentation comments
- All new functions (`severity_summary`, `get_severity_summary`) have documentation comments explaining purpose, parameters, and behavior
- Follow existing error handling patterns with `.context()` wrapping

### 6.8 Documentation Impact

- Update `docs/api.md` to document the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint, including request parameters, response schema, and example response
- No changes needed to `docs/architecture.md` (no architectural changes)

## Step 7 -- Write Tests

### Create `tests/api/advisory_summary.rs`

Following the test conventions discovered in Step 4 (assertion style, naming, setup patterns from sibling test files `tests/api/advisory.rs` and `tests/api/sbom.rs`):

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_with_known_advisories() {
    // Given an SBOM with advisories of known severities seeded in the test database
    // (e.g., 2 Critical, 3 High, 1 Medium, 0 Low)

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then the response is 200 OK with correct counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 3);
    assert_eq!(summary.medium, 1);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 6);
}

/// Verifies that a non-existent SBOM ID returns 404 Not Found.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{nonexistent-id}/advisory-summary").await;

    // Then the response is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_empty() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then all counts are zero
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
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with the same advisory linked multiple times in sbom_advisory

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then the advisory is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.total, 1); // Not 3 (the duplicate count)
    assert_eq!(summary.critical, 1); // Assuming the duplicated advisory is Critical
}
```

All test functions include:
- Documentation comment explaining what is verified
- Given-When-Then section comments for structure
- Value-based assertions on specific fields (not just counts or lengths)

Run tests with `cargo test` and fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| # | Criterion | Verification |
|---|---|---|
| 1 | GET /api/v2/sbom/{id}/advisory-summary returns correct JSON shape | Verified by `test_advisory_summary_with_known_advisories` -- asserts all fields present with correct values |
| 2 | Returns 404 for non-existent SBOM ID | Verified by `test_advisory_summary_not_found` |
| 3 | Counts only unique advisories (deduplicates) | Verified by `test_advisory_summary_deduplication` |
| 4 | All severity levels default to 0 | Verified by `test_advisory_summary_empty` -- asserts all fields are 0 |
| 5 | Response time under 200ms for 500 advisories | Verified structurally: query uses database-level aggregation (GROUP BY + COUNT) rather than loading all advisories into memory; single query with join and distinct |

## Step 9 -- Self-Verification

### Scope Containment

Run `git diff --name-only` and compare against the declared file lists:

**Expected modified files:**
- `modules/fundamental/src/advisory/service/advisory.rs` -- in Files to Modify
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- in Files to Modify
- `modules/fundamental/src/advisory/model/mod.rs` -- in Files to Modify

**Expected created files:**
- `modules/fundamental/src/advisory/model/severity_summary.rs` -- in Files to Create
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- in Files to Create
- `tests/api/advisory_summary.rs` -- in Files to Create

**Potential out-of-scope files:**
- `docs/api.md` -- out of scope but justified by Documentation Impact analysis; ask user to approve
- `tests/api/mod.rs` or test runner config -- may need updating to include new test file; ask user to approve if modified

### Untracked File Check

Run `git status --short` and check for `??` entries in directories where implementation occurred. Flag any untracked files referenced by code (e.g., via `include_str!`) for user review.

### Sensitive-Pattern Check

Run: `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'`

Flag any matches.

### Documentation Currency

Verify `docs/api.md` has been updated with the new endpoint documentation. If not already updated in Step 6, update it now.

### Documentation Scope Preservation

If `docs/api.md` was modified, verify that the replacement text still covers all previously documented endpoints and use cases. No scope narrowing should occur from adding a new endpoint.

### Eval Coverage Currency

No `SKILL.md` files are being modified. Skip.

### Example Consistency

If documentation examples were added (e.g., example response in `docs/api.md`), verify the example JSON matches the `SeveritySummary` struct fields and types.

### Cross-Section Reference Consistency

Verify file paths are consistent across the task description sections:
- `AdvisoryService` -- referenced in Files to Modify as `modules/fundamental/src/advisory/service/advisory.rs` and in Implementation Notes as `modules/fundamental/src/advisory/service/advisory.rs` -- consistent
- `SeveritySummary` -- referenced in Files to Create as `modules/fundamental/src/advisory/model/severity_summary.rs` -- consistent
- Endpoint handler -- referenced in Files to Create as `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- consistent

### Duplication Check

Search the repository for existing severity aggregation or summary functions. Check for:
- Existing severity counting logic that could be reused
- Similar aggregation patterns in other modules (e.g., package license counting)
- Duplicate function names or patterns

### CI Checks from CONVENTIONS.md

Run all CI check commands extracted from `CONVENTIONS.md` in Step 4. Fix any failures before proceeding. Hard stop on any non-zero exit code.

### Data-Flow Trace

Trace the complete data flow for the new feature:

1. **Input**: HTTP GET request to `/api/v2/sbom/{id}/advisory-summary` with SBOM ID path parameter
2. **Processing -- Route dispatch**: Axum routes the request to `get_severity_summary` handler
3. **Processing -- Parameter extraction**: `Path<Id>` extracts the SBOM ID from the URL
4. **Processing -- Service call**: Handler calls `AdvisoryService::severity_summary(sbom_id, tx)`
5. **Processing -- Database query**: Service queries `sbom_advisory` join table, joins with advisory table, deduplicates by advisory ID, groups by severity, counts per group
6. **Processing -- SBOM existence check**: Service verifies the SBOM exists; returns 404 if not
7. **Processing -- Aggregation**: Counts are mapped to `SeveritySummary` struct fields
8. **Output**: Handler returns `Json(SeveritySummary)` as HTTP 200 response

All stages connected. **COMPLETE**.

### Contract and Sibling Parity

**Contract verification:**
- `SeveritySummary` implements `Serialize`, `Deserialize`, `ToSchema` -- all required for Axum JSON response and OpenAPI
- `get_severity_summary` handler returns `Result<Json<SeveritySummary>, AppError>` -- matches the contract for Axum handlers

**Sibling parity:**
- Compare `get_severity_summary` with `get.rs` handler in same module:
  - Error handling: both use `.context()` wrapping -- parity maintained
  - Parameter extraction: both use `Path<Id>` -- parity maintained
  - Response type: get.rs returns model directly, severity_summary returns model directly -- parity maintained
- Compare `AdvisoryService::severity_summary` with `AdvisoryService::fetch`:
  - Transaction handling: both take `&Transactional<'_>` -- parity maintained
  - Error handling: both use `Result<T, AppError>` with `.context()` -- parity maintained

**Cross-module shared entity analysis:**
- Entity `sbom_advisory` -- used by ingestor module (`ingestor/graph/advisory/mod.rs`) for ingestion. Verify new code follows same transaction and constraint handling patterns.

**Caller-site parity:**
- New code calls `AdvisoryService` methods -- verify call pattern matches existing callers in endpoints.

## Step 10 -- Commit and Push

### Commit

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
       modules/fundamental/src/advisory/model/mod.rs \
       modules/fundamental/src/advisory/service/advisory.rs \
       modules/fundamental/src/advisory/endpoints/severity_summary.rs \
       modules/fundamental/src/advisory/endpoints/mod.rs \
       tests/api/advisory_summary.rs \
       docs/api.md

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated severity counts (critical, high, medium, low, total) for
advisories linked to a given SBOM. Includes SeveritySummary model,
AdvisoryService::severity_summary method, and integration tests.

Implements TC-9201"
```

### Push and Create PR

```bash
git push -u origin TC-9201

gh pr create --base main \
  --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" \
  --body "## Summary

Add a new REST endpoint \`GET /api/v2/sbom/{id}/advisory-summary\` that returns
aggregated vulnerability advisory severity counts for a given SBOM. The endpoint
returns counts per severity level (Critical, High, Medium, Low) and a total,
enabling dashboard widgets to render severity breakdowns without client-side counting.

### Changes
- New \`SeveritySummary\` response model
- New \`AdvisoryService::severity_summary\` method using \`sbom_advisory\` join table
- New GET handler registered at \`/api/v2/sbom/{id}/advisory-summary\`
- Integration tests for happy path, 404, empty, and deduplication cases
- API documentation updated

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)"
```

If a GitHub issue reference was extracted in Step 1, append `Closes <owner>/<repo>#<number>` to the PR body.

## Step 11 -- Update Jira

### Set Git Pull Request Custom Field

Update `customfield_10875` with the PR URL in ADF format:

```
jira.update_issue(TC-9201, fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
```

### Add Comment

Post a comment to TC-9201 with:
- PR link
- Summary of changes made (new endpoint, model, service method, tests)
- Note: no deviations from the plan

Include the skill footer with version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`.

### Transition to In Review

```
jira.transition_issue(TC-9201) -> In Review
```
