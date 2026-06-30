# Implementation Plan: TC-9201 -- Add advisory severity aggregation service and endpoint

## Step 0 -- Validate Project Configuration

Verified CLAUDE.md contains the required sections:
- **Repository Registry**: trustify-backend is registered with Serena instance `serena_backend` at path `./`
- **Jira Configuration**: Project key TC, Cloud ID 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Code Intelligence**: Serena instance `serena_backend` configured with rust-analyzer language server

All project configuration sections are present and valid.

## Step 1 -- Fetch and Parse Jira Task TC-9201

Parsed structured sections from the task description:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM, returning counts per severity level (Critical, High, Medium, Low) and a total.
- **Files to Modify**: advisory/service/advisory.rs, advisory/endpoints/mod.rs, advisory/model/mod.rs
- **Files to Create**: advisory/model/severity_summary.rs, advisory/endpoints/severity_summary.rs, tests/api/advisory_summary.rs
- **API Changes**: GET /api/v2/sbom/{id}/advisory-summary (NEW)
- **Implementation Notes**: Follow existing endpoint and service patterns, use sbom_advisory join table, count by severity from AdvisorySummary, return AppError with .context()
- **Acceptance Criteria**: Correct severity counts, 404 for missing SBOM, deduplication, zero defaults, performance under 200ms
- **Test Requirements**: Valid SBOM counts, 404 for non-existent, all-zeros for empty, deduplication
- **Dependencies**: None

## Step 1.5 -- Verify Description Integrity

Check for a description digest comment on TC-9201 with marker `[sdlc-workflow] Description digest:`. No digest comment was found on the Jira issue. Per backward compatibility policy, log a warning and proceed without blocking execution. The absence of a digest comment does not prevent implementation.

> WARNING: No description digest comment found on TC-9201. Proceeding without integrity verification (backward compatibility).

## Step 4 -- Understand the Code

### Sibling file analysis

Before making any changes, read and analyze existing sibling files to understand conventions:

1. **Read `modules/fundamental/src/advisory/endpoints/get.rs`** -- Inspect the existing GET endpoint handler to understand the pattern for path parameter extraction (via `Path<Id>`), service method invocation, JSON response return, and error handling. This establishes the template for the new severity_summary endpoint handler.

2. **Read `modules/fundamental/src/advisory/service/advisory.rs`** -- Inspect the existing AdvisoryService implementation to understand the method signature pattern (`&self, id: Id, tx: &Transactional<'_>`), how database queries are structured, and how results are returned. The new `severity_summary` method must follow this same pattern.

3. **Read `modules/fundamental/src/advisory/model/summary.rs`** -- Inspect the AdvisorySummary struct to understand how the `severity` field is defined, which will be used to count advisories by severity level.

4. **Read `common/src/error.rs`** -- Inspect the AppError enum and its IntoResponse implementation to understand the error handling pattern. All service and endpoint methods return `Result<T, AppError>` and use `.context()` for error wrapping.

5. **Read `modules/fundamental/src/advisory/endpoints/mod.rs`** -- Inspect route registration to understand how to add the new route following existing `Router::new().route("/path", get(handler))` patterns.

6. **Read CONVENTIONS.md** at the repository root for any additional project-wide conventions.

### Key conventions discovered

- Module structure: each domain follows `model/ + service/ + endpoints/` pattern
- Error handling: `Result<T, AppError>` with `.context()` wrapping throughout
- Endpoint pattern: extract path params via `Path<Id>`, call service method, return `Json(result)`
- Route registration in each module's `endpoints/mod.rs`
- Integration tests in `tests/api/` using real PostgreSQL test database

## Step 5 -- Create Branch

1. Fetch latest from origin and check out the target branch: `git checkout main && git pull origin main`
2. Create and switch to implementation branch: `git checkout -b TC-9201`

The branch is named after the Jira issue ID (TC-9201), branching from the target branch `main`.

## Step 6 -- Implement Changes

### Files to Create (3 files)

#### 1. `modules/fundamental/src/advisory/model/severity_summary.rs`

New file defining the SeveritySummary response struct.

- Define `SeveritySummary` struct with fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`
- Derive `Serialize`, `Deserialize`, `Debug`, `Clone`, `Default`, `utoipa::ToSchema`
- Implement a constructor or builder method that takes a collection of severity values and aggregates counts
- Follow the same derive and attribute patterns visible in the sibling `summary.rs` and `details.rs` model files

See: `outputs/file-1-description.md`

#### 2. `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

New file implementing the GET handler for `/api/v2/sbom/{id}/advisory-summary`.

- Define an async handler function `severity_summary` that extracts `Path(id): Path<Id>` and calls `AdvisoryService::severity_summary`
- Return `Json(SeveritySummary)` on success
- Return `AppError` (404) when SBOM is not found
- Follow the exact pattern from the sibling `get.rs` endpoint handler

See: `outputs/file-2-description.md`

#### 3. `tests/api/advisory_summary.rs`

New integration test file for the advisory summary endpoint.

- Test: valid SBOM with known advisories returns correct severity counts per level
- Test: non-existent SBOM ID returns 404 status
- Test: SBOM with no advisories returns `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`
- Test: duplicate advisory links are deduplicated in the count
- Follow the existing test pattern from sibling `tests/api/advisory.rs` and `tests/api/sbom.rs`

See: `outputs/file-3-description.md`

### Files to Modify (3 files)

#### 4. `modules/fundamental/src/advisory/service/advisory.rs`

Add a `severity_summary` method to AdvisoryService.

- Method signature: `pub async fn severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<SeveritySummary, AppError>`
- Query the `sbom_advisory` join table to find all advisories linked to the given SBOM ID
- Load each advisory's severity from AdvisorySummary
- Deduplicate by advisory ID
- Count occurrences per severity level (Critical, High, Medium, Low)
- Return SeveritySummary with counts and total
- Use `.context("Failed to fetch severity summary")` for error wrapping

See: `outputs/file-4-description.md`

#### 5. `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new severity summary route.

- Add `mod severity_summary;` to import the new endpoint module
- Add `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))` to the Router chain, following the pattern of existing route registrations

See: `outputs/file-5-description.md`

#### 6. `modules/fundamental/src/advisory/model/mod.rs`

Register the new model module.

- Add `pub mod severity_summary;` line to expose the SeveritySummary struct from the model module
- Place it alongside the existing `pub mod summary;` and `pub mod details;` declarations

See: `outputs/file-6-description.md`

## Step 10 -- Commit and Push

### Commit message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes service method, response model,
and integration tests.

Refs: TC-9201
```

### Commit command

```bash
git add \
  modules/fundamental/src/advisory/model/severity_summary.rs \
  modules/fundamental/src/advisory/endpoints/severity_summary.rs \
  tests/api/advisory_summary.rs \
  modules/fundamental/src/advisory/service/advisory.rs \
  modules/fundamental/src/advisory/endpoints/mod.rs \
  modules/fundamental/src/advisory/model/mod.rs

git commit -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes service method, response model,
and integration tests.

Refs: TC-9201" --trailer='Assisted-by: Claude Code'
```

### Push and open PR

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "..."
```

The PR targets the `main` branch (the Target Branch from the task description) and references TC-9201.
