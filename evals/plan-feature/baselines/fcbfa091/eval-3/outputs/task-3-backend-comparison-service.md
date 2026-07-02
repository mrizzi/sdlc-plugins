## additional_fields
```
{ "labels": ["ai-generated-jira"], "priority": {"name": "Critical"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }
```

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Implement the SBOM comparison service logic that computes a structured diff between two SBOMs. The service fetches package lists, advisory associations, and license data for both SBOMs from existing services, then computes the six diff categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. The diff is computed on-the-fly with no new database tables, meeting the p95 < 1s response time requirement for SBOMs with up to 2000 packages each.

## Files to Create
- `modules/fundamental/src/sbom/service/comparison.rs` — `SbomComparisonService` with `compare(left_id, right_id) -> Result<SbomComparisonResult, AppError>` method

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod comparison;` to expose the new service module

## Implementation Notes
The comparison service method should:
1. Fetch packages for both SBOMs using `PackageService` from `modules/fundamental/src/package/service/mod.rs`
2. Fetch advisories for both SBOMs using `AdvisoryService` from `modules/fundamental/src/advisory/service/advisory.rs`
3. Compute set differences for packages (by name) to determine added and removed packages
4. For packages present in both SBOMs, compare versions to detect version changes and classify direction as "upgrade" or "downgrade" using semantic version comparison
5. Compute advisory differences: advisories affecting right but not left are "new vulnerabilities"; advisories affecting left but not right are "resolved vulnerabilities"
6. Compare license fields for packages present in both SBOMs to detect license changes
7. Populate advisory_count on added/removed packages by counting advisories associated with each package

Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` for method signatures, error handling, and database access patterns. All service methods should return `Result<T, AppError>` using `.context()` wrapping for errors.

Use the query helpers from `common/src/db/query.rs` for any database queries needed to fetch package and advisory data.

Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping. Follow this pattern for all comparison service methods.
Applies: task creates `modules/fundamental/src/sbom/service/comparison.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Module pattern: each domain module follows `model/ + service/ + endpoints/` structure. The comparison service belongs in `modules/fundamental/src/sbom/service/` alongside existing `sbom.rs`.
Applies: task creates `modules/fundamental/src/sbom/service/comparison.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Existing SBOM service with fetch and list methods; reference for service method patterns and database access
- `modules/fundamental/src/package/service/mod.rs::PackageService` — Fetch package lists for a given SBOM; reuse for retrieving packages to compare
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — Fetch advisories associated with SBOM packages; reuse for vulnerability diff computation
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination; reuse for bulk package/advisory queries
- `common/src/error.rs::AppError` — Standard error type with `.context()` chaining

## Acceptance Criteria
- [ ] `SbomComparisonService::compare()` accepts two SBOM IDs and returns `Result<SbomComparisonResult, AppError>`
- [ ] Added packages are correctly identified (in right SBOM but not in left)
- [ ] Removed packages are correctly identified (in left SBOM but not in right)
- [ ] Version changes are detected with correct upgrade/downgrade direction classification
- [ ] New vulnerabilities are identified (advisories affecting right but not left)
- [ ] Resolved vulnerabilities are identified (advisories affecting left but not right)
- [ ] License changes are detected for packages present in both SBOMs
- [ ] Advisory count is populated for added and removed packages
- [ ] Returns appropriate AppError for non-existent SBOM IDs
- [ ] Handles the case where both SBOMs are identical (returns empty diff)

## Test Requirements
- [ ] Unit test: compare two SBOMs with known package differences returns correct added/removed packages
- [ ] Unit test: compare two SBOMs with version changes returns correct direction classification
- [ ] Unit test: compare two identical SBOMs returns empty diff (all categories empty)
- [ ] Unit test: compare with non-existent SBOM ID returns appropriate error
- [ ] Unit test: advisory counts are correctly populated on added/removed packages
- [ ] Unit test: license changes are detected when package license differs between SBOMs

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Backend comparison model structs (SbomComparisonResult and sub-structs must be defined)
