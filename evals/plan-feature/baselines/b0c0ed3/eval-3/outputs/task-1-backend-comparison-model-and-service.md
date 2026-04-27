## Repository
trustify-backend

## Description
Add the data model and service logic for computing a structured diff between two SBOMs. This task introduces the comparison result types and a new service method on `SbomService` that loads package, advisory, and license data for two SBOMs, then computes a categorized diff (added/removed packages, version changes, new/resolved vulnerabilities, license changes). The diff is computed on-the-fly from existing data — no new database tables are required.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Structs for the comparison result: `SbomComparisonResult`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new model module
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `compare(left_id, right_id) -> Result<SbomComparisonResult, AppError>` method to `SbomService`

## API Changes
- None (this task adds internal service logic only; the endpoint is added in Task 2)

## Implementation Notes
Follow the existing module pattern in `modules/fundamental/src/sbom/model/` where `summary.rs` defines `SbomSummary` and `details.rs` defines `SbomDetails`. The new `comparison.rs` follows the same conventions: derive `Serialize`, `Deserialize`, and `Clone` on all structs.

The `SbomComparisonResult` struct should contain six fields matching the API response shape specified in the feature:
```rust
pub struct SbomComparisonResult {
    pub added_packages: Vec<PackageDiff>,
    pub removed_packages: Vec<PackageDiff>,
    pub version_changes: Vec<VersionChange>,
    pub new_vulnerabilities: Vec<VulnerabilityDiff>,
    pub resolved_vulnerabilities: Vec<VulnerabilityDiff>,
    pub license_changes: Vec<LicenseChange>,
}
```

The `compare` method on `SbomService` should:
1. Load packages for both SBOMs using `PackageService::fetch` (see `modules/fundamental/src/package/service/mod.rs`)
2. Load advisories for both SBOMs using `AdvisoryService::fetch` (see `modules/fundamental/src/advisory/service/advisory.rs`)
3. Compute set differences for packages, version changes, advisory diffs, and license changes
4. Return the result wrapped in `Result<SbomComparisonResult, AppError>`

Use the existing error handling pattern: all fallible operations should use `.context()` wrapping as established in `common/src/error.rs`.

The `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` includes a `license` field — use this for license change detection. The `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` includes a `severity` field — use this for vulnerability diff severity reporting.

Per the non-functional requirements, the comparison must handle SBOMs with up to 2000 packages each at p95 < 1s. Use HashMaps keyed by package name for O(n) diff computation rather than nested iteration.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Reference for struct definition patterns and serde derives used in this module
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — Reference for complex model structs with nested types
- `modules/fundamental/src/package/service/mod.rs::PackageService` — Provides package listing by SBOM; reuse to load package sets for both left and right SBOMs
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — Provides advisory listing; reuse to load advisories associated with each SBOM
- `common/src/error.rs::AppError` — Standard error type; use for all error returns in the compare method

## Acceptance Criteria
- [ ] `SbomComparisonResult` and all nested diff structs are defined in `modules/fundamental/src/sbom/model/comparison.rs`
- [ ] All structs derive `Serialize`, `Deserialize`, and `Clone`
- [ ] `SbomService::compare(left_id, right_id)` returns a fully populated `SbomComparisonResult`
- [ ] Added packages are those present in the right SBOM but not in the left
- [ ] Removed packages are those present in the left SBOM but not in the right
- [ ] Version changes list packages present in both SBOMs with differing versions, including upgrade/downgrade direction
- [ ] New vulnerabilities are advisories affecting the right SBOM but not the left
- [ ] Resolved vulnerabilities are advisories affecting the left SBOM but not the right
- [ ] License changes list packages present in both SBOMs whose license field differs
- [ ] The method returns `AppError` for invalid or non-existent SBOM IDs

## Test Requirements
- [ ] Unit test: comparing two SBOMs where the right has additional packages produces correct `added_packages`
- [ ] Unit test: comparing two SBOMs where the left has packages not in the right produces correct `removed_packages`
- [ ] Unit test: packages present in both with different versions appear in `version_changes` with correct direction
- [ ] Unit test: advisories unique to the right SBOM appear in `new_vulnerabilities`
- [ ] Unit test: advisories unique to the left SBOM appear in `resolved_vulnerabilities`
- [ ] Unit test: packages with changed licenses appear in `license_changes`
- [ ] Unit test: comparing identical SBOMs returns all empty vectors
- [ ] Unit test: non-existent SBOM ID returns an appropriate error
