## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the SBOM comparison data model types and diff computation service method to support the `GET /api/v2/sbom/compare` endpoint. The service computes a structured diff between two SBOMs by comparing their packages, advisory associations, and license data. All computation is done on-the-fly from existing data — no new database tables are required.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Struct definitions for SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, and LicenseChange

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new comparison model module
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `compare_sboms(left_id, right_id)` method to SbomService that fetches both SBOMs' package lists, advisory associations, and license data, then computes the diff

## Implementation Notes
Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for struct definitions — derive `Serialize`, `Deserialize`, `Debug`, and `Clone`.

The `compare_sboms` method should:
1. Fetch package lists for both SBOMs using the existing PackageService in `modules/fundamental/src/package/service/mod.rs`
2. Fetch advisory associations using the existing AdvisoryService in `modules/fundamental/src/advisory/service/advisory.rs`
3. Compute set differences for added/removed packages by comparing package name sets
4. Detect version changes by matching packages present in both SBOMs with differing versions
5. Compute new/resolved vulnerabilities by comparing advisory ID sets between the two SBOMs
6. Detect license changes by comparing the `license` field on PackageSummary for packages present in both SBOMs

Use the existing query helpers in `common/src/db/query.rs` for database queries. Wrap errors using `Result<T, AppError>` with `.context()` as established in `common/src/error.rs`.

The response shape must match the Figma design contract:
```json
{
  "added_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
  "removed_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
  "version_changes": [{ "name": "...", "left_version": "...", "right_version": "...", "direction": "upgrade" }],
  "new_vulnerabilities": [{ "advisory_id": "...", "severity": "critical", "title": "...", "affected_package": "..." }],
  "resolved_vulnerabilities": [{ "advisory_id": "...", "severity": "...", "title": "...", "previously_affected_package": "..." }],
  "license_changes": [{ "name": "...", "left_license": "...", "right_license": "..." }]
}
```

The `direction` field in VersionChange should be computed by comparing semver ordering: if right > left, "upgrade"; if right < left, "downgrade".

Performance target: p95 < 1s for SBOMs with up to 2000 packages each. Prefer batch queries over per-package queries to minimize database round-trips.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Existing SBOM summary struct; use as reference for field naming and serialization patterns
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — Existing detail struct; reuse the pattern for deriving serde traits
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Contains `license` field needed for license change detection
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Contains `severity` field needed for vulnerability severity reporting
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Existing service; add the compare method here following the established pattern of fetch/list methods
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — Error enum for consistent error handling

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct is defined with all six diff category fields (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
- [ ] `compare_sboms` method correctly identifies packages added in the right SBOM but not in the left
- [ ] `compare_sboms` method correctly identifies packages removed (present in left, absent in right)
- [ ] `compare_sboms` method correctly detects version changes with upgrade/downgrade direction
- [ ] `compare_sboms` method correctly identifies new and resolved vulnerabilities by comparing advisory associations
- [ ] `compare_sboms` method correctly detects license changes for packages present in both SBOMs
- [ ] All model structs derive `Serialize`, `Deserialize`, `Debug`, `Clone`
- [ ] Method returns `Result<SbomComparisonResult, AppError>`

## Test Requirements
- [ ] Unit test: compare two SBOMs where one has additional packages — verify added_packages contains the extras
- [ ] Unit test: compare two SBOMs where one has removed packages — verify removed_packages is correct
- [ ] Unit test: compare two SBOMs with same package at different versions — verify version_changes with correct direction
- [ ] Unit test: compare two SBOMs with differing advisory associations — verify new_vulnerabilities and resolved_vulnerabilities
- [ ] Unit test: compare two SBOMs where a shared package has different licenses — verify license_changes

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
