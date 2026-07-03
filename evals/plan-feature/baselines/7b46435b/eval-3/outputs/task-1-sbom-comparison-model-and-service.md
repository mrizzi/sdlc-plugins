## Repository
trustify-backend

## Target Branch
main

## Description
Create the SBOM comparison diff model types and service method. This task introduces an `SbomComparisonResult` response struct and supporting sub-structs for each diff category (added/removed packages, version changes, new/resolved vulnerabilities, license changes). It also adds a `compare_sboms` method to `SbomService` that accepts two SBOM IDs, queries the existing `sbom_package`, `package`, `package_license`, `sbom_advisory`, and `advisory` entities, and computes the set differences between the two SBOMs. No new database tables are required -- the diff is computed on-the-fly from existing data.

additional_fields: { "labels": ["ai-generated-jira"], "priority": "Critical", "fixVersions": "RHTPA 1.5.0" }

## Files to Create
- `modules/fundamental/src/sbom/model/compare.rs` -- `SbomComparisonResult` struct with fields: added_packages (Vec<PackageDiff>), removed_packages (Vec<PackageDiff>), version_changes (Vec<VersionChange>), new_vulnerabilities (Vec<VulnerabilityDiff>), resolved_vulnerabilities (Vec<VulnerabilityDiff>), license_changes (Vec<LicenseChange>); plus sub-structs `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- add `pub mod compare;` and re-export `SbomComparisonResult`
- `modules/fundamental/src/sbom/service/sbom.rs` -- add `compare_sboms(&self, left_id: Uuid, right_id: Uuid) -> Result<SbomComparisonResult, AppError>` method that queries packages, advisories, and licenses for both SBOMs and computes set differences

## API Changes
- `SbomComparisonResult` -- NEW response model: `{ added_packages: [...], removed_packages: [...], version_changes: [...], new_vulnerabilities: [...], resolved_vulnerabilities: [...], license_changes: [...] }`

## Implementation Notes
Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary` struct) for struct layout and derive macros. The new structs should derive `Serialize`, `Deserialize`, `Clone`, `Debug`, and `utoipa::ToSchema`.

The comparison algorithm should:
1. Load packages for both SBOMs by querying `sbom_package` joined with `package` (see `entity/src/sbom_package.rs` and `entity/src/package.rs`)
2. Compute package set differences using package name as the key:
   - Added: present in right SBOM but not left
   - Removed: present in left SBOM but not right
   - Version changes: present in both but with different versions (use `entity/src/package.rs` version field)
3. Load advisories for both SBOMs via `sbom_advisory` joined with `advisory` (see `entity/src/sbom_advisory.rs` and `entity/src/advisory.rs`)
4. Compute vulnerability diff: new = in right only, resolved = in left only; include severity from `AdvisorySummary` (see `modules/fundamental/src/advisory/model/summary.rs`)
5. Load license data via `entity/src/package_license.rs` and diff by package name

Use the same `Result<T, AppError>` error handling pattern with `.context()` wrapping from `common/src/error.rs`. Return 404 if either SBOM ID does not exist (check using existing `SbomService` fetch methods in `modules/fundamental/src/sbom/service/sbom.rs`).

Per CONVENTIONS.md §Error Handling: all service methods return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` module scope.

Per CONVENTIONS.md §Module Pattern: each domain module follows `model/ + service/ + endpoints/` structure.
Applies: task creates `modules/fundamental/src/sbom/model/compare.rs` matching the convention's `.rs` module scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` -- existing model struct; follow the same derive macro pattern and struct layout
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- contains the severity field definition; reuse the severity enum or string mapping for the vulnerability diff
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- existing service with fetch/list methods; add the comparison method here
- `common/src/error.rs::AppError` -- standard error type for all service methods
- `entity/src/sbom_package.rs` -- SBOM-Package join table entity; use for querying packages per SBOM
- `entity/src/package_license.rs` -- Package-License mapping entity; use for license diff computation
- `common/src/db/query.rs` -- shared query builder helpers for filtering and pagination

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct exists with all six diff category fields
- [ ] Sub-structs `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange` exist with appropriate fields
- [ ] `SbomService::compare_sboms` method compiles and returns correct diff results from the database
- [ ] Packages are compared by name as the key, with version changes detected separately from added/removed
- [ ] Advisory deduplication is applied (each advisory counted once per SBOM)
- [ ] Returns 404 error if either SBOM ID does not exist

## Test Requirements
- [ ] Unit test: `SbomComparisonResult` serializes to expected JSON shape matching the API response structure
- [ ] Unit test: comparison of two identical SBOMs returns empty diff arrays for all six categories
- [ ] Unit test: comparison correctly identifies added, removed, and version-changed packages

## Verification Commands
- `cargo build -p trustify-fundamental` -- compiles without errors
- `cargo test -p trustify-fundamental compare` -- unit tests pass
