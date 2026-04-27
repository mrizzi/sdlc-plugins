# Task 1 — SBOM comparison diff model and service logic

## Repository
trustify-backend

## Description
Add the data model structs and service logic for computing a structured diff between two SBOMs. This task creates the response types that represent the comparison result and implements the diffing algorithm in SbomService. The diff computes six categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. The diff is computed on-the-fly from existing package, advisory, and license data — no new database tables are required.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — re-export new comparison model module
- `modules/fundamental/src/sbom/service/sbom.rs` — add `compare` method to SbomService

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — comparison result structs (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)

## API Changes
- None at this layer (service only — endpoint is Task 2)

## Implementation Notes
- Follow the existing model module pattern: `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs` and `SbomDetails` in `modules/fundamental/src/sbom/model/details.rs` demonstrate the struct and serialization conventions. New structs should derive `Serialize`, `Deserialize`, `Debug`, `Clone` and use `#[serde(rename_all = "snake_case")]`.
- The comparison response shape must match the API contract specified in the feature:
  ```json
  {
    "added_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "removed_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "version_changes": [{ "name": "...", "left_version": "...", "right_version": "...", "direction": "upgrade|downgrade" }],
    "new_vulnerabilities": [{ "advisory_id": "...", "severity": "critical|high|medium|low", "title": "...", "affected_package": "..." }],
    "resolved_vulnerabilities": [{ "advisory_id": "...", "severity": "...", "title": "...", "previously_affected_package": "..." }],
    "license_changes": [{ "name": "...", "left_license": "...", "right_license": "..." }]
  }
  ```
- The `direction` field in `VersionChange` should be an enum with `Upgrade` and `Downgrade` variants, serialized as lowercase strings. Determine direction by comparing semantic version ordering where possible, falling back to lexicographic comparison.
- The `compare` method in `SbomService` should:
  1. Fetch package lists for both SBOMs using existing `PackageService` (see `modules/fundamental/src/package/service/mod.rs`).
  2. Compute set differences using package name as the join key.
  3. Fetch advisories for both SBOMs using `AdvisoryService` (see `modules/fundamental/src/advisory/service/advisory.rs`).
  4. Compute advisory diffs by comparing advisory IDs linked to each SBOM via `sbom_advisory` join table (see `entity/src/sbom_advisory.rs`).
  5. Compute license changes by comparing `license` field on `PackageSummary` (see `entity/src/package_license.rs` for the license mapping entity).
- Use `HashMap` for O(n) diff computation to meet the p95 < 1s performance requirement for SBOMs with up to 2000 packages.
- Error handling: return `Result<SbomComparisonResult, AppError>` using `.context()` wrapping per `common/src/error.rs` conventions.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with fetch and list methods; add the compare method here
- `modules/fundamental/src/package/service/mod.rs::PackageService` — fetch package lists for each SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — fetch advisory lists for each SBOM
- `common/src/model/paginated.rs::PaginatedResults` — existing paginated query pattern for fetching all packages
- `entity/src/sbom_package.rs` — SBOM-Package join table entity for querying packages per SBOM
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for querying advisories per SBOM
- `entity/src/package_license.rs` — Package-License mapping entity for license comparison

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct and all nested types are defined with correct Serde serialization
- [ ] `SbomService::compare(left_id, right_id)` returns a fully populated `SbomComparisonResult`
- [ ] Added packages include those in the right SBOM but not in the left
- [ ] Removed packages include those in the left SBOM but not in the right
- [ ] Version changes correctly identify packages present in both SBOMs with different versions and compute upgrade/downgrade direction
- [ ] New vulnerabilities include advisories affecting the right SBOM but not the left
- [ ] Resolved vulnerabilities include advisories affecting the left SBOM but not the right
- [ ] License changes include packages whose license differs between the two SBOMs
- [ ] Each advisory entry includes severity, title, and affected package name
- [ ] Error case: returns appropriate error when either SBOM ID does not exist

## Test Requirements
- [ ] Unit test: compare two SBOMs with known package differences produces correct added/removed lists
- [ ] Unit test: compare two SBOMs with version changes correctly classifies upgrade vs downgrade
- [ ] Unit test: compare two SBOMs with advisory differences produces correct new/resolved vulnerability lists
- [ ] Unit test: compare two SBOMs with license changes produces correct license diff
- [ ] Unit test: comparing an SBOM with itself produces empty diff (all sections empty)
- [ ] Unit test: comparing with a non-existent SBOM ID returns an error

## Verification Commands
- `cargo build -p trustify-fundamental` — must compile without errors
- `cargo test -p trustify-fundamental` — all tests pass
