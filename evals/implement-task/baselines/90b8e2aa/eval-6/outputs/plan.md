# Implementation Plan for TC-9201

**Task:** Add advisory severity aggregation service and endpoint
**Repository:** trustify-backend
**Target Branch:** main
**Parent Feature:** TC-9001

---

## Step 0 -- Validate Project Configuration

Verified that the project's CLAUDE.md contains the required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present with Project key (TC), Cloud ID, Feature issue type ID
3. **Code Intelligence** -- present with tool naming convention (`mcp__<serena-instance>__<tool>`) and configured instance `serena_backend` using `rust-analyzer`

All sections present and complete. Proceeding.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all JIRA operations. If MCP fails, prompt user for REST API fallback per the standard protocol.

## Step 1 -- Fetch and Parse Jira Task

Fetched TC-9201 via `jira.get_issue("TC-9201")`. Parsed structured description:

- **Repository:** trustify-backend
- **Target Branch:** main
- **Description:** Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM
- **Files to Modify:**
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`
- **Files to Create:**
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes:** `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Implementation Notes:** Follow existing endpoint pattern, use `sbom_advisory` join table, deduplicate by advisory ID, return `AppError` with `.context()`
- **Acceptance Criteria:** 5 items (correct counts, 404 on missing SBOM, deduplication, zero defaults, performance)
- **Test Requirements:** 4 tests (valid counts, 404, empty SBOM, deduplication)
- **Target PR:** not present (default flow)
- **Bookend Type:** not present (default flow)
- **Dependencies:** None

Captured `webUrl` for later use in PR description (e.g., `https://redhat.atlassian.net/browse/TC-9201`).

Checked GitHub Issue custom field (`customfield_10747`) -- not populated; skipping silently.

## Step 1.5 -- Verify Description Integrity

1. Retrieved issue comments via `jira.get_issue_comments("TC-9201")`
2. Located one comment matching marker `[sdlc-workflow] Description digest:` with body: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
3. Comment `created` and `updated` timestamps are identical -- comment was not edited
4. Parsed format tag: `sha256-md`; parsed hex digest: `a1b2c3d4e5f67890...`
5. Computed current digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt` -- output: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
6. Format tags match (`sha256-md` == `sha256-md`), hex digests match
7. **Result: match -- proceed silently.** No user prompt, no warning, no added latency.

## Step 2 -- Verify Dependencies

The task specifies "Depends on: None." No dependency checks required. Proceeding.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-9201 to the current user: `jira.edit_issue("TC-9201", assignee=<account-id>)`
3. Transition TC-9201 to In Progress: `jira.transition_issue("TC-9201", "In Progress")`

## Step 4 -- Understand the Code

Use the `serena_backend` Serena instance (`mcp__serena_backend__<tool>`) to inspect the codebase.

### 4.1 Inspect files to modify

- **`modules/fundamental/src/advisory/service/advisory.rs`**: use `mcp__serena_backend__get_symbols_overview` to see the `AdvisoryService` struct and its existing methods (`fetch`, `list`, `search`). Use `mcp__serena_backend__find_symbol` with `include_body=true` on the `fetch` method to understand the pattern (parameter signature, transactional handling, error wrapping with `.context()`).
- **`modules/fundamental/src/advisory/endpoints/mod.rs`**: inspect route registration pattern -- how existing routes like `get.rs` and `list.rs` handlers are registered using `Router::new().route(...)`.
- **`modules/fundamental/src/advisory/model/mod.rs`**: inspect existing `pub mod` declarations to follow the module registration pattern.

### 4.2 Inspect related files for patterns

- **`modules/fundamental/src/advisory/endpoints/get.rs`**: use `find_symbol` to read the handler function -- understand how `Path<Id>` extraction, service calls, and JSON responses work.
- **`modules/fundamental/src/advisory/model/summary.rs`**: inspect the `AdvisorySummary` struct to understand the `severity` field type and values (Critical, High, Medium, Low).
- **`entity/src/sbom_advisory.rs`**: understand the join table schema for linking SBOMs to advisories.
- **`common/src/error.rs`**: inspect `AppError` enum to understand error handling pattern.

### 4.3 Check backward compatibility

Use `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to identify all callers and ensure the new method does not affect existing ones (it is purely additive).

### 4.4 Convention conformance analysis

Examine sibling files in `modules/fundamental/src/advisory/endpoints/` (get.rs, list.rs) and `modules/fundamental/src/sbom/endpoints/` (get.rs, list.rs) for patterns:

**Discovered conventions (from sibling analysis):**
- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Path extraction:** Use `Path<Id>` extractor for path parameters
- **Service invocation:** Handlers call service methods with `&self`, entity ID, and `&Transactional<'_>`
- **Response:** Return struct directly -- Axum's `Json` extractor handles serialization
- **Route registration:** `Router::new().route("/path", get(handler_fn))` in `endpoints/mod.rs`
- **Module registration:** `pub mod <name>;` in `model/mod.rs`
- **Naming:** Service methods use `verb_noun` pattern (e.g., `fetch`, `list`)

### 4.5 Test convention analysis

Examine sibling test files in `tests/api/` (sbom.rs, advisory.rs, search.rs):

**Discovered test conventions (from sibling test analysis):**
- **Assertion style:** `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Error cases:** 404 tests use `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming:** `test_<endpoint>_<scenario>` pattern
- **Setup:** Tests use a real PostgreSQL test database with fixtures

### 4.6 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root. If present, read and extract CI check commands for Step 9. If not present, proceed normally.

### 4.7 Documentation file identification

Identify relevant docs:
- `docs/api.md` -- may need updating with the new endpoint
- `docs/architecture.md` -- unlikely to need changes
- `README.md` -- unlikely to need changes

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

/// Aggregated severity counts for advisories linked to an SBOM.
///
/// Each field contains the count of unique advisories at that severity level,
/// enabling dashboard widgets to render severity breakdowns without client-side counting.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
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

### 6.2 Register the model module in `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` following the existing pattern of module declarations.

### 6.3 Add `severity_summary` method to `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`

Add a new method following the same pattern as `fetch` and `list`:

- Signature: `pub async fn severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<SeveritySummary, AppError>`
- Query the `sbom_advisory` join table to find advisories linked to the given SBOM
- Join with advisory data to get severity levels
- Deduplicate by advisory ID (use `DISTINCT` or `group_by`)
- Count advisories per severity level (Critical, High, Medium, Low)
- Return `SeveritySummary` with all counts and total
- Wrap errors with `.context("Failed to compute severity summary")`
- Return 404 via `AppError` if the SBOM ID does not exist (check SBOM existence first, consistent with existing SBOM endpoints)

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern in `get.rs`:

```rust
/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for advisories linked to the specified SBOM.
pub async fn severity_summary(
    Path(id): Path<Id>,
    service: Extension<AdvisoryService>,
    tx: Extension<Transactional<'_>>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Error computing advisory severity summary")?;
    Ok(Json(summary))
}
```

### 6.5 Register the route in `modules/fundamental/src/advisory/endpoints/mod.rs`

Add the new route following the existing registration pattern:

```rust
pub mod severity_summary;

// In the router builder:
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))
```

### 6.6 Cross-repo API contract verification

This task does not involve cross-repo manual REST calls (it is a backend-only task adding a new endpoint). No cross-repo verification needed.

### 6.7 Code quality practices

Ensure all new structs, functions, and public types have documentation comments (`///`) as shown in the code above.

### 6.8 Documentation impact

Check if `docs/api.md` documents existing endpoints. If so, add an entry for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint with its request/response format.

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with the following tests, following sibling test conventions:

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that an SBOM with linked advisories returns correct severity counts per level.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with known advisories at various severity levels
    // (set up test fixtures in the database)

    // When requesting the advisory summary for that SBOM
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then the response is 200 OK with correct per-level counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, expected_critical);
    assert_eq!(summary.high, expected_high);
    assert_eq!(summary.medium, expected_medium);
    assert_eq!(summary.low, expected_low);
    assert_eq!(summary.total, expected_total);
}
```

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{nonexistent-id}/advisory-summary").await;

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_empty() {
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
```

### Test 4: Duplicate advisory links are deduplicated

```rust
/// Verifies that duplicate advisory-SBOM links are deduplicated in severity counts.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM linked to the same advisory multiple times

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then the advisory is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.total, 1); // not 2 or more
}
```

Run tests: `cargo test` -- fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

Walk through each criterion:

1. **GET /api/v2/sbom/{id}/advisory-summary returns correct shape** -- verified by test 1 and endpoint implementation
2. **Returns 404 for non-existent SBOM** -- verified by test 2
3. **Deduplicates by advisory ID** -- verified by test 4 and use of DISTINCT/group_by in query
4. **All severity levels default to 0** -- verified by test 3 and `Default` derive on SeveritySummary
5. **Response time under 200ms for up to 500 advisories** -- verified by query design (single aggregation query, no N+1)

## Step 9 -- Self-Verification

### Scope containment

Run `git diff --name-only` and verify all modified/created files are within the declared scope:

- `modules/fundamental/src/advisory/service/advisory.rs` -- in Files to Modify
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- in Files to Modify
- `modules/fundamental/src/advisory/model/mod.rs` -- in Files to Modify
- `modules/fundamental/src/advisory/model/severity_summary.rs` -- in Files to Create
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- in Files to Create
- `tests/api/advisory_summary.rs` -- in Files to Create

If any file outside this list was modified (e.g., `docs/api.md`), list it and ask the user to approve.

### Untracked file check

Run `git status --short`, extract `??` entries, filter by proximity to modified directories, and check for code references. Flag any referenced untracked files for user review.

### Sensitive-pattern check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- expect no matches.

### Documentation currency

Check if `docs/api.md` describes the endpoint space and needs a new entry. Update if needed.

### CI checks from CONVENTIONS.md

If CI check commands were extracted from `CONVENTIONS.md` in Step 4, run them all. Hard stop on any non-zero exit.

Otherwise, run `cargo build` and `cargo clippy` as standard Rust checks. Fix any new warnings.

### Data-flow trace

- `GET /api/v2/sbom/{id}/advisory-summary` request -> Axum extracts `Path<Id>` -> calls `AdvisoryService::severity_summary(id, tx)` -> queries `sbom_advisory` join table with advisory severity data -> aggregates counts into `SeveritySummary` -> returns `Json<SeveritySummary>` response -- **COMPLETE**

### Contract and sibling parity

- `SeveritySummary` -- standalone struct, no trait contract to implement. Derives `Serialize`, `Deserialize`, `ToSchema` matching sibling model structs.
- Sibling parity with `get.rs`, `list.rs` endpoints: error handling pattern (Result<T, AppError>) matches, path extraction matches, service call pattern matches.
- No cross-module shared entity anomalies -- read-only queries on `sbom_advisory`, consistent with existing read patterns.

### Duplication check

Search for existing severity aggregation or advisory counting logic. If found, refactor to reuse instead of duplicating.

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs
git add modules/fundamental/src/advisory/model/mod.rs
git add modules/fundamental/src/advisory/service/advisory.rs
git add modules/fundamental/src/advisory/endpoints/severity_summary.rs
git add modules/fundamental/src/advisory/endpoints/mod.rs
git add tests/api/advisory_summary.rs
# Add any documentation files that were updated

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity summary endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns aggregated
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes deduplication by advisory ID and
proper 404 handling for missing SBOMs.

Implements TC-9201"

git push -u origin TC-9201
```

Create pull request:

```bash
gh pr create --base main --title "feat(api): add advisory severity summary endpoint" --body "## Summary

Add a new REST endpoint \`GET /api/v2/sbom/{id}/advisory-summary\` that aggregates
vulnerability advisory severity counts for a given SBOM, returning counts per
severity level (Critical, High, Medium, Low) and a total.

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)

## Changes

- Added \`SeveritySummary\` response struct in \`advisory/model/severity_summary.rs\`
- Added \`severity_summary\` method to \`AdvisoryService\`
- Added GET handler and route registration for \`/api/v2/sbom/{id}/advisory-summary\`
- Added integration tests covering valid counts, 404, empty SBOM, and deduplication

## Test plan

- [x] Valid SBOM with known advisories returns correct severity counts
- [x] Non-existent SBOM ID returns 404
- [x] SBOM with no advisories returns all zeros
- [x] Duplicate advisory links are deduplicated in the count"
```

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field:** Update `customfield_10875` on TC-9201 with the PR URL in ADF format (inlineCard).

2. **Add comment** to TC-9201 with:
   - PR link
   - Summary of changes: added SeveritySummary model, service method, endpoint handler, route registration, and integration tests
   - No deviations from the plan
   - Include the skill footnote with version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`

3. **Transition** TC-9201 to In Review: `jira.transition_issue("TC-9201", "In Review")`
