# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Task Summary

Add a `license` query parameter to the `GET /api/v2/package` list endpoint in the `trustify-backend` repository. The filter supports exact-match filtering on SPDX license identifiers, with both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) input.

## Step 0 — Validate Project Configuration

The project CLAUDE.md contains all required sections:
- **Repository Registry**: `trustify-backend` mapped to Serena instance `serena_backend`
- **Jira Configuration**: Project key `TC`, Cloud ID, Feature issue type ID present
- **Code Intelligence**: `serena_backend` instance with `rust-analyzer`

Validation passes; proceed with implementation.

## Step 1 — Fetch and Parse Jira Task

Parsed sections from TC-9203:

| Section | Content |
|---|---|
| Repository | trustify-backend |
| Description | Add `license` query parameter for filtering packages by SPDX identifier |
| Files to Modify | `modules/fundamental/src/package/endpoints/list.rs`, `modules/fundamental/src/package/service/mod.rs` |
| Files to Create | `tests/api/package_license_filter.rs` |
| API Changes | `GET /api/v2/package?license=MIT` (single), `GET /api/v2/package?license=MIT,Apache-2.0` (multi) |
| Dependencies | None |
| Target PR | None (default flow — new branch and PR) |

No missing sections; all required fields present.

## Step 2 — Verify Dependencies

No dependencies listed. Proceed.

## Step 3 — Transition to In Progress and Assign

*(Skipped — no Jira interaction in this plan-only mode.)*

Would execute:
1. `jira.user_info()` to get current user account ID
2. `jira.edit_issue(TC-9203, assignee=<accountId>)` to assign
3. `jira.transition_issue(TC-9203)` to "In Progress"

## Step 4 — Understand the Code

### 4.1 Files to inspect via Serena (`serena_backend`)

**Files to Modify:**

1. **`modules/fundamental/src/package/endpoints/list.rs`** — current package list endpoint handler
   - Use `mcp__serena_backend__get_symbols_overview` to see the handler struct and query parameter types
   - Use `mcp__serena_backend__find_symbol` on the query struct (likely `PackageListQuery` or similar) and the handler function to understand the existing parameter extraction pattern

2. **`modules/fundamental/src/package/service/mod.rs`** — PackageService list method
   - Use `mcp__serena_backend__get_symbols_overview` to see the service struct and its methods
   - Use `mcp__serena_backend__find_symbol` on the `list` method to understand how it builds queries and applies filters

**Reuse Candidate files to inspect:**

3. **`common/src/db/query.rs`** — shared query builder, specifically `apply_filter`
   - Use `mcp__serena_backend__find_symbol` with `include_body=true` on `apply_filter` to understand its signature, how it parses comma-separated values, and how it generates SQL IN clauses

4. **`modules/fundamental/src/advisory/endpoints/list.rs`** — reference implementation for `severity` filter
   - Use `mcp__serena_backend__get_symbols_overview` to see the advisory query struct pattern
   - Use `mcp__serena_backend__find_symbol` on the advisory query struct to see how the optional `severity` field is declared, extracted, and passed to the service

5. **`entity/src/package_license.rs`** — package-license join entity
   - Use `mcp__serena_backend__get_symbols_overview` to see the SeaORM entity struct, columns, and relation definitions

**Backward compatibility check:**

6. Use `mcp__serena_backend__find_referencing_symbols` on:
   - The package list handler function — to confirm no callers depend on the query struct shape
   - The `PackageService::list` method — to identify all callers and ensure adding an optional parameter is backward-compatible

### 4.2 Convention conformance analysis

**Sibling files to analyze:**

- `modules/fundamental/src/advisory/endpoints/list.rs` — sibling list endpoint (severity filter pattern)
- `modules/fundamental/src/sbom/endpoints/list.rs` — sibling list endpoint (general list pattern)
- `modules/fundamental/src/advisory/service/advisory.rs` — sibling service (filter propagation pattern)
- `modules/fundamental/src/sbom/service/sbom.rs` — sibling service (query building pattern)

**Expected discovered conventions:**
- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Response types:** List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers:** Filters use `common/src/db/query.rs` `apply_filter` for parameter parsing
- **Naming:** Service methods follow `verb_noun` pattern (e.g., `list_packages`)
- **Module pattern:** Each domain follows `model/ + service/ + endpoints/` structure

### 4.3 Test convention analysis

**Sibling test files to analyze:**

- `tests/api/advisory.rs` — advisory endpoint integration tests
- `tests/api/sbom.rs` — SBOM endpoint integration tests
- `tests/api/search.rs` — search endpoint integration tests

**Expected discovered test conventions:**
- **Assertion style:** `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Response validation:** List tests validate `total_count`, `items.len()`, and key item fields
- **Error cases:** Include tests for invalid input returning appropriate status codes
- **Test naming:** `test_<endpoint>_<scenario>` pattern (e.g., `test_list_packages_filtered_by_license`)
- **Setup:** Tests use a real PostgreSQL test database with fixture data

### 4.4 Documentation file identification

- `README.md` — repository root
- `CONVENTIONS.md` — repository root (check for CI check commands)
- `docs/api.md` — REST API reference (may need updating for new query parameter)

### 4.5 CONVENTIONS.md lookup

Would read `CONVENTIONS.md` at the repository root to extract:
- CI check commands (e.g., `cargo fmt --check`, `cargo clippy`, `cargo test`)
- Code generation commands (if any)

---

## Step 5 — Create Branch

Default flow (no Target PR):

```bash
git checkout -b TC-9203
```

---

## Step 6 — Implement Changes

### File 1: `modules/fundamental/src/package/endpoints/list.rs`

**What exists:** A handler for `GET /api/v2/package` that extracts query parameters (likely pagination and sorting) and calls `PackageService::list`.

**Changes:**

1. **Add `license` field to the query parameter struct** (e.g., `PackageListQuery`):
   ```rust
   /// Optional license filter; supports comma-separated SPDX identifiers.
   pub license: Option<String>,
   ```
   This follows the same pattern as the `severity` field in the advisory list query struct (`modules/fundamental/src/advisory/endpoints/list.rs`).

2. **Pass the `license` parameter to the service layer:**
   In the handler function, extract `query.license` and pass it to `PackageService::list()` as an additional optional parameter. If the parameter is `Some`, pass it through; if `None`, the service applies no license filter.

3. **Add input validation:**
   If the `license` value is present but contains invalid characters or empty segments after splitting on commas, return `400 Bad Request` via `AppError`. This ensures the acceptance criterion "Invalid license values return 400 Bad Request" is met.

**Reuse:** Follow the exact structural pattern from `modules/fundamental/src/advisory/endpoints/list.rs` for how the `severity` optional field is declared, extracted, and forwarded.

### File 2: `modules/fundamental/src/package/service/mod.rs`

**What exists:** `PackageService` with a `list` method that builds a SeaORM query, applies pagination/sorting, and returns `PaginatedResults<PackageSummary>`.

**Changes:**

1. **Add `license` parameter to the `list` method signature:**
   ```rust
   pub async fn list(
       &self,
       // ... existing params (pagination, sorting, etc.)
       license: Option<String>,
   ) -> Result<PaginatedResults<PackageSummary>, AppError> {
   ```

2. **Apply the license filter using `apply_filter` from `common/src/db/query.rs`:**
   ```rust
   if let Some(license_value) = license {
       query = apply_filter(query, "package_license", "license", &license_value)?;
   }
   ```
   The `apply_filter` function handles:
   - Parsing comma-separated values (e.g., `"MIT,Apache-2.0"` becomes `["MIT", "Apache-2.0"]`)
   - Generating the appropriate SQL `IN` clause
   - Joining through the `package_license` table as needed

3. **Join the `package_license` entity:**
   Use the SeaORM entity from `entity/src/package_license.rs` to join the `package_license` table when the license filter is active:
   ```rust
   if license.is_some() {
       query = query.join(
           JoinType::InnerJoin,
           entity::package_license::Relation::Package.def().rev(),
       );
   }
   ```
   This follows SeaORM conventions for join-based filtering and avoids raw SQL.

**Reuse:**
- `common/src/db/query.rs::apply_filter` — direct reuse for comma-separated parsing and SQL IN clause
- `entity/src/package_license.rs` — direct reuse of the existing entity and its relation definitions for the JOIN
- Pattern from `modules/fundamental/src/advisory/service/advisory.rs` — structural reference for how the advisory service applies the severity filter

### File 3 (new): `tests/api/package_license_filter.rs`

**What to create:** Integration tests for the license filter feature.

**Test functions:**

1. **`test_list_packages_filter_single_license`**
   - Doc comment: `/// Verifies that filtering by a single license returns only packages with that license.`
   - Given: Test database seeded with packages having MIT, Apache-2.0, and GPL-3.0 licenses
   - When: `GET /api/v2/package?license=MIT`
   - Then: Response status is 200; all returned packages have license `MIT`; assert on specific package names/identifiers, not just count

2. **`test_list_packages_filter_multi_license`**
   - Doc comment: `/// Verifies that comma-separated license filter returns packages matching any listed license.`
   - Given: Same test fixtures
   - When: `GET /api/v2/package?license=MIT,Apache-2.0`
   - Then: Response status is 200; returned packages have either `MIT` or `Apache-2.0` license; assert on specific values

3. **`test_list_packages_no_license_filter`**
   - Doc comment: `/// Verifies that omitting the license parameter returns all packages unchanged.`
   - Given: Same test fixtures
   - When: `GET /api/v2/package` (no license parameter)
   - Then: Response status is 200; all packages are returned; count matches total fixture count; assert on specific items

4. **`test_list_packages_invalid_license`**
   - Doc comment: `/// Verifies that an invalid license value returns 400 Bad Request.`
   - Given: Same test fixtures
   - When: `GET /api/v2/package?license=` (empty value or invalid characters)
   - Then: Response status is 400

**Conventions applied:**
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern from sibling tests
- Validate `total_count`, `items.len()`, and specific item field values
- Follow `test_<endpoint>_<scenario>` naming
- Include given-when-then section comments in each test body
- Value-based assertions (assert on specific license values, not just counts)

### Module registration

- Add `mod package_license_filter;` to `tests/api/mod.rs` (or the test harness entry point) so the new test file is compiled and discovered by `cargo test`.

### Documentation impact

- If `docs/api.md` documents the `GET /api/v2/package` endpoint, add the `license` query parameter to its documentation with:
  - Parameter name: `license`
  - Type: `string` (optional)
  - Description: "Filter by SPDX license identifier. Supports comma-separated values for OR matching."
  - Example: `?license=MIT` or `?license=MIT,Apache-2.0`

---

## Step 7 — Run Tests

```bash
cargo test
```

Fix any failures before proceeding.

---

## Step 8 — Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| `GET /api/v2/package?license=MIT` returns only MIT packages | Covered by `test_list_packages_filter_single_license` |
| `GET /api/v2/package?license=MIT,Apache-2.0` returns matching packages | Covered by `test_list_packages_filter_multi_license` |
| No license parameter returns all packages | Covered by `test_list_packages_no_license_filter` |
| Response shape (`PaginatedResults<PackageSummary>`) unchanged | All tests deserialize into the existing response type |
| Invalid license values return 400 | Covered by `test_list_packages_invalid_license` |

---

## Step 9 — Self-Verification

### Scope containment

Expected modified/created files:
- `modules/fundamental/src/package/endpoints/list.rs` (modified) — in scope
- `modules/fundamental/src/package/service/mod.rs` (modified) — in scope
- `tests/api/package_license_filter.rs` (created) — in scope

Possible out-of-scope files that might need changes:
- `tests/api/mod.rs` — to register the new test module (justified: required for test discovery)
- `docs/api.md` — to document the new query parameter (justified: documentation currency)

### Sensitive-pattern check

No passwords, API keys, secrets, or `.env` references expected in the diff.

### Data-flow trace

- **Input**: HTTP query parameter `license` enters via Axum extractor in `list.rs`
- **Validation**: Empty/invalid values caught and returned as `400 Bad Request`
- **Processing**: Parameter forwarded to `PackageService::list()`, which calls `apply_filter` to build SQL IN clause with JOIN to `package_license` table
- **Output**: Filtered `PaginatedResults<PackageSummary>` returned as JSON response

All stages connected. **COMPLETE.**

### Contract & sibling parity

- Adding an optional `license: Option<String>` field to the query struct is backward-compatible (serde default is `None`)
- Adding an optional parameter to `PackageService::list()` requires updating all callers — the endpoint handler is the primary caller
- Sibling parity with advisory severity filter: same pattern (optional field, `apply_filter`, conditional JOIN)

### CI checks

Would run verification commands extracted from `CONVENTIONS.md` (e.g., `cargo fmt --check`, `cargo clippy`, `cargo test`).

---

## Step 10 — Commit and Push

```bash
git add modules/fundamental/src/package/endpoints/list.rs \
       modules/fundamental/src/package/service/mod.rs \
       tests/api/package_license_filter.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add license filter to package list endpoint

Support filtering packages by SPDX license identifier via the
\`license\` query parameter on GET /api/v2/package. Accepts both
single-value and comma-separated multi-value input.

Implements TC-9203"
```

```bash
git push -u origin TC-9203
gh pr create --title "feat(api): add license filter to package list endpoint" \
  --body "## Summary
- Add \`license\` query parameter to \`GET /api/v2/package\` for filtering by SPDX identifier
- Support comma-separated values for OR matching (e.g., \`?license=MIT,Apache-2.0\`)
- Add integration tests covering single, multi, no-filter, and invalid-input scenarios

Implements [TC-9203](https://redhat.atlassian.net/browse/TC-9203)"
```

## Step 11 — Update Jira

Would execute:
1. Update custom field `customfield_10875` with PR URL (ADF inlineCard format)
2. Add comment with PR link, summary of changes, and confirmation of no deviations
3. Transition TC-9203 to "In Review"
