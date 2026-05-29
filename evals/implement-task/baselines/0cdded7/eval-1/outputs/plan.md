# Implementation Plan: TC-9201 -- Add advisory severity aggregation service and endpoint

## Task Summary

**Jira Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Parent Issue**: is incorporated by TC-9001

## Step 1: Extract Target Branch

The task specifies **Target Branch: main**. The implementation branch will be created from `main`.

## Step 2: Inspect Before Modify (Sibling Analysis)

Before making any changes, the following existing files are read and analyzed to discover conventions and patterns:

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- Inspected to understand the endpoint handler pattern: async function signature with `Path<Id>` extraction, service call delegation, `Result<Json<T>, AppError>` return type, and `.context()` error wrapping. This is the primary template for the new severity summary endpoint.

2. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Inspected to understand the service method pattern: `pub async fn` methods on `AdvisoryService` taking `&self`, entity identifiers, and `&Transactional<'_>`, returning `Result<T, anyhow::Error>`. The existing `fetch` and `list` methods serve as templates for the new `severity_summary` method.

3. **`modules/fundamental/src/advisory/model/summary.rs`** -- Inspected to understand the model struct pattern (derive macros, field visibility) and critically to confirm the `severity: String` field on `AdvisorySummary` that will be used for aggregation counting.

4. **`common/src/error.rs`** -- Inspected to understand the `AppError` enum, its variants (`NotFound`, `Internal`), the `IntoResponse` implementation, and how `.context()` from anyhow integrates with the error type.

5. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Inspected to understand route registration patterns for adding the new route.

6. **`entity/src/sbom_advisory.rs`** -- Inspected to understand the join table structure for linking SBOMs to advisories, which is needed for the aggregation query.

Full conventions are documented in `outputs/conventions.md`.

## Step 3: Branch Creation

Create branch from the Target Branch (`main`):

```
git checkout main
git pull origin main
git checkout -b TC-9201
```

Branch name: **TC-9201** (matches Jira key per workflow conventions).

## Step 4: Scope -- Files to Modify and Create

Strictly scoped to the task description's "Files to Modify" and "Files to Create" sections:

### Files to Modify (3)
1. `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
2. `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
3. `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`

### Files to Create (3)
4. `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
5. `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
6. `tests/api/advisory_summary.rs` -- integration tests

### Files Explicitly Excluded
- `server/src/main.rs` -- task confirms "no changes needed (routes auto-mount via module registration)"

## Step 5: Implementation Details

See individual `file-N-description.md` files for detailed changes to each file.

### Implementation Order

1. Create the model struct first (`severity_summary.rs` model) -- no dependencies
2. Register the model module (`model/mod.rs` modification)
3. Add the service method (`advisory.rs` modification) -- depends on model
4. Create the endpoint handler (`severity_summary.rs` endpoint) -- depends on service + model
5. Register the route (`endpoints/mod.rs` modification) -- depends on endpoint handler
6. Write integration tests (`advisory_summary.rs`) -- depends on everything above

## Step 6: Commit Plan

### Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated severity counts (critical, high, medium, low, total) for
all advisories linked to a given SBOM. Includes SeveritySummary model,
AdvisoryService.severity_summary method, and integration tests.

TC-9201
```

The commit will be created with:
```
git commit --trailer='Assisted-by: Claude Code'
```

This uses Conventional Commits format (`feat(advisory): description`), includes TC-9201 in the footer for Jira linkage, and the `--trailer` flag appends the `Assisted-by: Claude Code` trailer.

## Step 7: Verification

After implementation, the following verification steps would be performed:
- `cargo check` -- ensure compilation passes
- `cargo test --test advisory_summary` -- run the new integration tests
- `cargo clippy` -- ensure no lint warnings
- Manual review that all acceptance criteria are addressed
