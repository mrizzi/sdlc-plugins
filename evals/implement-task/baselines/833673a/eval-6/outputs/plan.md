# Implementation Plan -- TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Task Summary

**Jira Issue:** TC-9201
**Repository:** trustify-backend
**Target Branch:** main
**Parent Feature:** TC-9001 (linked via "is incorporated by")
**Dependencies:** None

Add a service method and REST endpoint that aggregates vulnerability advisory severity
counts for a given SBOM. The endpoint returns a summary with counts per severity level
(Critical, High, Medium, Low) and a total.

---

## Step 0 -- Validate Project Configuration

Verified that the project's CLAUDE.md contains:
- **Repository Registry** -- present, with `trustify-backend` mapped to Serena instance `serena_backend`
- **Jira Configuration** -- present, with Project key `TC`, Cloud ID, Feature issue type ID, and custom fields
- **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and `serena_backend` configured with `rust-analyzer`

All required sections are present. Proceeding.

## Step 1 -- Fetch and Parse Jira Task

Parsed the structured description for TC-9201:

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Add severity aggregation service + endpoint |
| Bookend Type | (none) |
| Target PR | (none) |
| Dependencies | None |

**Files to Modify:**
- `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
- `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`

**Files to Create:**
- `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
- `tests/api/advisory_summary.rs` -- integration tests

**API Changes:**
- `GET /api/v2/sbom/{id}/advisory-summary` -- NEW endpoint

**GitHub Issue custom field:** `customfield_10747` -- check the fetched issue for a value; extract and store if present.

**Git Pull Request custom field:** `customfield_10875` -- will be used in Step 11 to store the PR URL.

**Issue webUrl:** Captured for use in PR description (e.g., `https://redhat.atlassian.net/browse/TC-9201`).

## Step 1.5 -- Verify Description Integrity

See `digest-match.md` for the full verification walkthrough. Summary:

- Located digest comment with marker `[sdlc-workflow] Description digest:`
- Comment `created` and `updated` timestamps are identical -- comment was not edited
- Parsed format tag: `sha256-md`, hex digest: `a1b2c3d4e5f67890...`
- Computed current digest using `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
- Format tags match (`sha256-md` == `sha256-md`)
- Hex digests match
- **Result:** Proceed silently -- no user prompt, no interruption

## Step 2 -- Verify Dependencies

The task lists "Depends on: None". No dependency checks required. Proceeding.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's account ID via `jira.user_info()`
2. Assign TC-9201 to current user: `jira.edit_issue("TC-9201", assignee=<account-id>)`
3. Transition TC-9201 to In Progress: `jira.transition_issue("TC-9201") -> In Progress`

## Step 4 -- Understand the Code

### 4.1 Inspect Files to Modify

Using `mcp__serena_backend__get_symbols_overview` on each file:

**`modules/fundamental/src/advisory/service/advisory.rs`:**
- Contains `AdvisoryService` struct with methods: `fetch`, `list`, `search`
- Uses `Transactional<'_>` for transaction handling
- Methods return `Result<T, AppError>`
- The new `severity_summary` method will follow the same pattern as `fetch`

**`modules/fundamental/src/advisory/endpoints/mod.rs`:**
- Registers routes using `Router::new().route("/path", get(handler))`
- Existing routes: list, get by ID
- The new route will be added following the same registration pattern

**`modules/fundamental/src/advisory/model/mod.rs`:**
- Re-exports model submodules (`pub mod summary;`, `pub mod details;`)
- Will add `pub mod severity_summary;`

### 4.2 Inspect Sibling Files for Conventions

**Sibling endpoint file -- `modules/fundamental/src/advisory/endpoints/get.rs`:**
- Extracts path params via `Path<Id>`
- Calls service method
- Returns `Json<T>` response
- Error handling with `Result<Json<T>, AppError>` and `.context()`

**Sibling model file -- `modules/fundamental/src/advisory/model/summary.rs`:**
- `AdvisorySummary` struct with `severity` field
- Derives `Serialize`, `Deserialize`, `Debug`, `Clone`
- Has doc comments on the struct and its fields

**Sibling service file -- `modules/fundamental/src/sbom/service/sbom.rs`:**
- `SbomService` follows the same struct/method pattern as `AdvisoryService`
- Methods take `&self`, entity ID, and `tx: &Transactional<'_>`

### 4.3 Inspect Entity Layer

**`entity/src/sbom_advisory.rs`:**
- Join table linking SBOMs to advisories
- Will be used to find advisories linked to a given SBOM

### 4.4 CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). The repo
structure shows `CONVENTIONS.md` exists. Read it and extract:
- CI check commands (for Step 9)
- Code generation commands (if any)
- Project-specific conventions

### 4.5 Discovered Conventions

**Production code conventions (from sibling analysis):**
- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Naming:** Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`)
- **Endpoint pattern:** Extract path params via `Path<Id>`, call service, return `Json<T>`
- **Route registration:** `Router::new().route("/path", get(handler))` in `endpoints/mod.rs`
- **Model structs:** Derive `Serialize, Deserialize, Debug, Clone`; include doc comments
- **Module registration:** `pub mod <name>;` in parent `mod.rs`

**Test conventions (from sibling test analysis):**
- **Location:** Integration tests in `tests/api/`
- **Assertion style:** `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Error cases:** Include 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming:** `test_<endpoint>_<scenario>` pattern

### 4.6 Documentation File Identification

- `README.md` at repository root
- `docs/api.md` -- API reference (may need update for new endpoint)
- `docs/architecture.md` -- system architecture overview

### 4.7 Check for Existing Utilities

Search for existing severity counting or aggregation logic that could be reused.
Use `mcp__serena_backend__search_for_pattern` to look for severity-related functions.

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

New file defining the `SeveritySummary` response struct:

```rust
use serde::{Deserialize, Serialize};

/// Summary of advisory severity counts for an SBOM.
///
/// Provides aggregated counts of vulnerability advisories grouped by
/// severity level, enabling dashboard widgets to render severity
/// breakdowns without client-side counting.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SeveritySummary {
    /// Count of critical-severity advisories.
    pub critical: u64,
    /// Count of high-severity advisories.
    pub high: u64,
    /// Count of medium-severity advisories.
    pub medium: u64,
    /// Count of low-severity advisories.
    pub low: u64,
    /// Total count of advisories across all severity levels.
    pub total: u64,
}

impl Default for SeveritySummary {
    fn default() -> Self {
        Self {
            critical: 0,
            high: 0,
            medium: 0,
            low: 0,
            total: 0,
        }
    }
}
```

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add module registration:

```rust
pub mod severity_summary;
```

### 6.3 Add `severity_summary` Method to `AdvisoryService`

In `modules/fundamental/src/advisory/service/advisory.rs`, add a method following
the existing `fetch`/`list` pattern:

```rust
/// Computes an aggregated severity summary for all advisories linked to a given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with the
/// specified SBOM, deduplicates by advisory ID, and counts each severity level.
/// Returns a `SeveritySummary` with counts for Critical, High, Medium, and Low,
/// plus a total. All counts default to 0 when no advisories exist at that level.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify the SBOM exists (return 404 if not found)
    // 2. Query sbom_advisory join table for advisories linked to this SBOM
    // 3. Deduplicate by advisory ID
    // 4. For each unique advisory, read the severity from AdvisorySummary
    // 5. Count by severity level (Critical, High, Medium, Low)
    // 6. Return SeveritySummary with counts and total
}
```

Key implementation details:
- Verify SBOM existence first (return 404 via `AppError` if not found, matching existing SBOM endpoints)
- Use `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) to find linked advisories
- Deduplicate by advisory ID to satisfy acceptance criteria
- Read `severity` field from `AdvisorySummary` to classify each advisory
- Default all counts to 0

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

New endpoint handler following the pattern in `endpoints/get.rs`:

```rust
use axum::{extract::Path, Json};

/// GET handler for `/api/v2/sbom/{id}/advisory-summary`.
///
/// Returns an aggregated severity summary of all vulnerability advisories
/// linked to the specified SBOM.
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

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route following the existing pattern:

```rust
use severity_summary::get_severity_summary;

// Add to the Router chain:
.route("/api/v2/sbom/:id/advisory-summary", get(get_severity_summary))
```

### 6.6 Documentation Impact

- Check `docs/api.md` for API endpoint documentation -- add entry for the new
  `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- No changes needed to `server/src/main.rs` (routes auto-mount via module registration)

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with the following test cases:

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that a valid SBOM with known linked advisories returns the correct
/// severity count breakdown.
#[tokio::test]
async fn test_advisory_summary_returns_correct_counts() {
    // Given an SBOM with advisories at known severity levels
    // (seed test DB with SBOM + linked advisories: 2 Critical, 1 High, 3 Medium, 0 Low)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response contains correct counts per severity
    // assert_eq!(resp.status(), StatusCode::OK)
    // assert_eq!(body.critical, 2)
    // assert_eq!(body.high, 1)
    // assert_eq!(body.medium, 3)
    // assert_eq!(body.low, 0)
    // assert_eq!(body.total, 6)
}
```

### Test 2: Non-existent SBOM returns 404

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM ID
/// returns a 404 Not Found response.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom_returns_404() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    // GET /api/v2/sbom/{nonexistent-id}/advisory-summary

    // Then the response is 404
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND)
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns a summary where
/// all severity counts and the total are zero.
#[tokio::test]
async fn test_advisory_summary_no_advisories_returns_zeros() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then all counts are zero
    // assert_eq!(resp.status(), StatusCode::OK)
    // assert_eq!(body.critical, 0)
    // assert_eq!(body.high, 0)
    // assert_eq!(body.medium, 0)
    // assert_eq!(body.low, 0)
    // assert_eq!(body.total, 0)
}
```

### Test 4: Duplicate advisory links are deduplicated

```rust
/// Verifies that duplicate advisory links in the sbom_advisory join table
/// are deduplicated, so each advisory is counted only once in the summary.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisory_links() {
    // Given an SBOM with duplicate links to the same advisory

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the advisory is counted only once
    // assert_eq!(body.total, 1)  // not 2, despite duplicate link
}
```

Run tests: `cargo test`

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns correct JSON shape | Test 1 validates the full response shape with correct counts |
| Returns 404 when SBOM ID does not exist | Test 2 validates 404 response |
| Counts only unique advisories (deduplicates by advisory ID) | Test 4 validates deduplication |
| All severity levels default to 0 when no advisories exist | Test 3 validates zero defaults |
| Response time under 200ms for SBOMs with up to 500 advisories | Verify via test timing or load test; query uses indexed join table |

## Step 9 -- Self-Verification

### Scope containment

Run `git diff --name-only` and verify all changed files are in scope:

**Expected modified files:**
- `modules/fundamental/src/advisory/service/advisory.rs`
- `modules/fundamental/src/advisory/endpoints/mod.rs`
- `modules/fundamental/src/advisory/model/mod.rs`

**Expected created files:**
- `modules/fundamental/src/advisory/model/severity_summary.rs`
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- `tests/api/advisory_summary.rs`

Any file outside this list requires user approval.

### Untracked file check

Run `git status --short`, filter `??` entries in directories with modified files,
search for code references. Flag any referenced untracked files for user approval.

### Sensitive-pattern check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'`
to ensure no secrets are staged.

### Documentation currency

Check if `docs/api.md` needs updating for the new endpoint. Update if not already
done in Step 6.

### Duplication check

Search for existing severity counting or aggregation functions in the codebase to
ensure no duplication with the new `severity_summary` method.

### Data-flow trace

- `GET /api/v2/sbom/{id}/advisory-summary`
  -> extract path param (SBOM ID) -> call `AdvisoryService::severity_summary`
  -> verify SBOM exists -> query `sbom_advisory` join table
  -> deduplicate advisories -> count by severity -> return `Json<SeveritySummary>`
  -- **COMPLETE**

### Contract and sibling parity

- `SeveritySummary` struct: standalone, no trait/interface contract to implement
- Sibling parity with `get.rs` endpoint: error handling pattern (`.context()`) present,
  path extraction (`Path<Id>`) present, JSON response present
- Sibling parity with `fetch`/`list` service methods: transaction parameter present,
  return type `Result<T, AppError>` present

### CI checks

Run any CI check commands extracted from `CONVENTIONS.md` (formatting, linting,
compilation). Fix any failures before proceeding.

### Cross-section reference consistency

Verify file paths are consistent across all sections of the task description:
- `AdvisoryService` -- referenced in both Files to Modify and Implementation Notes
  as `modules/fundamental/src/advisory/service/advisory.rs` -- consistent
- Route registration -- referenced in both Files to Modify and Implementation Notes
  as `modules/fundamental/src/advisory/endpoints/mod.rs` -- consistent

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
       modules/fundamental/src/advisory/model/mod.rs \
       modules/fundamental/src/advisory/service/advisory.rs \
       modules/fundamental/src/advisory/endpoints/severity_summary.rs \
       modules/fundamental/src/advisory/endpoints/mod.rs \
       tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns aggregated
severity counts (Critical, High, Medium, Low, total) for advisories linked
to a given SBOM. Includes SeveritySummary model, AdvisoryService method,
endpoint handler, and integration tests.

Implements TC-9201"
```

Push and create PR:

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "..."
```

PR description includes:
- Summary of changes
- `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)`
- GitHub issue `Closes` line if a GitHub issue reference was found in `customfield_10747`

## Step 11 -- Update Jira

1. Update `customfield_10875` (Git Pull Request custom field) with the PR URL in ADF format:
   ```
   jira.update_issue("TC-9201", fields={"customfield_10875": {"type": "doc", ...}})
   ```

2. Add comment to TC-9201 with:
   - PR link
   - Summary of changes: Added SeveritySummary model, severity_summary service method,
     GET endpoint at /api/v2/sbom/{id}/advisory-summary, and integration tests
   - No deviations from the plan

3. Transition TC-9201 to In Review:
   ```
   jira.transition_issue("TC-9201") -> In Review
   ```
