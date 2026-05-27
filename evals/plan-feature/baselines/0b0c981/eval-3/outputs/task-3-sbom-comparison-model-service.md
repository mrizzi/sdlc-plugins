## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the SBOM comparison diff model structs and the `SbomService::compare` method that computes a structured diff between two SBOMs. The diff covers six categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. The comparison is computed on-the-fly from existing package, advisory, and license data — no new database tables are introduced.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Diff model structs: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to export the new model module
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `compare(left_id, right_id)` method to `SbomService`

## Implementation Notes
Follow the existing model/service pattern established in the `sbom` module:
- Model structs go in `modules/fundamental/src/sbom/model/` alongside `summary.rs` and `details.rs`. Each struct should derive `Serialize`, `Deserialize`, `Clone`, and `Debug`.
- The `compare` method belongs in `modules/fundamental/src/sbom/service/sbom.rs` alongside existing `fetch` and `list` methods. It should accept two SBOM IDs, load their associated packages via the `sbom_package` join table (`entity/src/sbom_package.rs`), and compute set differences.
- For vulnerability diff: query the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) to find advisories linked to each SBOM, then compute the set difference. Use `AdvisorySummary` from `modules/fundamental/src/advisory/model/summary.rs` for severity information.
- For license diff: use the `package_license` entity (`entity/src/package_license.rs`) to compare license assignments per package between the two SBOMs.
- For version changes: compare packages present in both SBOMs by name, detect version differences, and classify direction as "upgrade" or "downgrade" using semantic version comparison.
- Use `PackageSummary` from `modules/fundamental/src/package/model/summary.rs` for the `license` field on added/removed package entries.
- Return `Result<SbomComparisonResult, AppError>` using the error type from `common/src/error.rs`, with `.context()` wrapping on database calls.
- The response shape must match the contract specified in the feature requirements:
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
- Performance: the comparison must handle SBOMs with up to 2000 packages each with p95 < 1s. Use efficient set operations (e.g., `HashMap`-based lookups) rather than nested iteration.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with `fetch` and `list` methods; add the `compare` method here following the same pattern
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — existing SBOM model struct to reference for struct conventions (derive macros, field naming)
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — provides severity field needed for vulnerability diff entries
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — provides license field for package diff entries
- `common/src/error.rs::AppError` — error handling pattern used across all service methods
- `entity/src/sbom_package.rs` — join table entity for SBOM-to-package relationships
- `entity/src/sbom_advisory.rs` — join table entity for SBOM-to-advisory relationships
- `entity/src/package_license.rs` — entity for package license mappings

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct and all sub-structs are defined in `modules/fundamental/src/sbom/model/comparison.rs`
- [ ] `SbomService::compare(left_id, right_id)` method computes a correct diff across all six categories
- [ ] Added packages are those present in the right SBOM but absent from the left
- [ ] Removed packages are those present in the left SBOM but absent from the right
- [ ] Version changes detect packages present in both SBOMs with different versions and classify direction
- [ ] New vulnerabilities are advisories affecting the right SBOM but not the left
- [ ] Resolved vulnerabilities are advisories affecting the left SBOM but not the right
- [ ] License changes detect packages whose license differs between the two SBOMs
- [ ] Method returns `AppError` for invalid SBOM IDs (not found)
- [ ] No new database tables or migrations are introduced

## Test Requirements
- [ ] Unit test: compare two SBOMs with known package sets and verify all six diff categories produce correct results
- [ ] Unit test: compare identical SBOMs and verify all diff categories are empty
- [ ] Unit test: compare with a non-existent SBOM ID returns an appropriate error
- [ ] Unit test: verify version change direction classification (upgrade vs downgrade)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main (trustify-backend)

[sdlc-workflow] Description digest: sha256:39ba327039d11fda1bfb05ff2396a265c113a8b1fc367177b3bf85031fe63a3e
