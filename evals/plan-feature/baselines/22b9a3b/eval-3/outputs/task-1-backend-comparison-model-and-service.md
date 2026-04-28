## Repository
trustify-backend

## Description
Add the SBOM comparison response model and service method that computes a structured diff between two SBOMs. The service loads both SBOMs with their associated packages, advisories, and licenses, then computes six diff categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. The diff is computed on-the-fly from existing data without new database tables.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Defines `SbomComparisonResult` and its sub-structs (`AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`)
- `modules/fundamental/src/sbom/service/compare.rs` — Implements the `compare_sboms(left_id, right_id)` method on `SbomService`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new model module
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod compare;` to expose the new service module

## API Changes
- `GET /api/v2/sbom/compare?left={id}&right={id}` — NEW: Returns `SbomComparisonResult` (this task creates the model and service; the endpoint is wired in Task 2)

## Implementation Notes
Follow the existing module pattern in `modules/fundamental/src/sbom/`. The model structs live in `model/` and the service logic lives in `service/`.

**Model structs** — define `SbomComparisonResult` with `serde::Serialize` and `utoipa::ToSchema` derives, matching the response shape from the feature spec:
```
SbomComparisonResult {
    added_packages: Vec<AddedPackage>,
    removed_packages: Vec<RemovedPackage>,
    version_changes: Vec<VersionChange>,
    new_vulnerabilities: Vec<NewVulnerability>,
    resolved_vulnerabilities: Vec<ResolvedVulnerability>,
    license_changes: Vec<LicenseChange>,
}
```

Follow the pattern established by `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs` and `SbomDetails` in `modules/fundamental/src/sbom/model/details.rs` for derive macros and struct conventions.

**Service method** — add `compare_sboms` to `SbomService` in a new file `service/compare.rs`. The method should:
1. Fetch both SBOMs using the existing `SbomService::fetch` method in `modules/fundamental/src/sbom/service/sbom.rs`
2. Return `AppError::NotFound` (from `common/src/error.rs`) if either SBOM ID is invalid
3. Load packages for both SBOMs via `PackageService` in `modules/fundamental/src/package/service/mod.rs`
4. Load advisories for both SBOMs via `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`
5. Compute set differences for each diff category using package name as the join key
6. For version changes, classify direction as "upgrade" or "downgrade" using semver comparison
7. For vulnerability diffs, include severity from `AdvisorySummary.severity` field (see `modules/fundamental/src/advisory/model/summary.rs`)
8. For license changes, compare `PackageSummary.license` field (see `modules/fundamental/src/package/model/summary.rs`)

**Error handling** — return `Result<SbomComparisonResult, AppError>` following the `.context()` wrapping pattern used throughout the codebase (see `common/src/error.rs`).

**Performance** — per non-functional requirements, the comparison must complete in p95 < 1s for SBOMs with up to 2000 packages each. Collect packages into `HashMap<String, PackageSummary>` keyed by package name for O(n) diff computation rather than O(n*m) nested iteration.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing fetch/list methods to load SBOM data
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing service to load packages for an SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — existing service to load advisories for an SBOM
- `common/src/error.rs::AppError` — standard error type with `IntoResponse` implementation
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct derive conventions

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct is defined with all six diff categories matching the API response shape in the feature spec
- [ ] `SbomService::compare_sboms(left_id, right_id)` returns a correctly computed diff for two valid SBOM IDs
- [ ] Returns `AppError::NotFound` when either SBOM ID does not exist
- [ ] Added packages are those in the right SBOM but not in the left
- [ ] Removed packages are those in the left SBOM but not in the right
- [ ] Version changes include direction classification (upgrade/downgrade)
- [ ] New vulnerabilities are advisories affecting the right SBOM but not the left
- [ ] Resolved vulnerabilities are advisories affecting the left SBOM but not the right
- [ ] License changes capture packages whose license differs between the two SBOMs

## Test Requirements
- [ ] Unit test: comparing two SBOMs with known package sets produces correct added/removed/changed lists
- [ ] Unit test: comparing identical SBOMs returns empty diff categories
- [ ] Unit test: comparing with a non-existent SBOM ID returns appropriate error
- [ ] Unit test: version change direction is correctly classified (upgrade vs downgrade)
- [ ] Unit test: vulnerability diff correctly separates new vs resolved advisories
- [ ] Unit test: license changes are detected when the same package has different licenses across SBOMs
