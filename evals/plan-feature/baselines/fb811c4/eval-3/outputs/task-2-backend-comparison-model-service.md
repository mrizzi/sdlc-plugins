# Task 2 — Add SBOM comparison model and service

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Define the data model structs for the SBOM comparison result and implement the comparison logic in SbomService. The service loads two SBOMs by ID, retrieves their associated packages (with license info) and advisories, then computes a structured diff covering added/removed packages, version changes, new/resolved vulnerabilities, and license changes. No new database tables are needed -- the diff is computed on-the-fly from existing package, advisory, and license data.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — re-export the new comparison module
- `modules/fundamental/src/sbom/service/sbom.rs` — add `compare()` method to SbomService

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — define SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange structs

## Implementation Notes
Follow the existing model/service pattern in `modules/fundamental/src/sbom/`. The new `comparison.rs` model file sits alongside `summary.rs` and `details.rs`.

**Model structs** (all derive `Serialize`, `Deserialize`, `Clone`, `Debug`, `ToSchema`):
- `SbomComparisonResult` with fields: `added_packages: Vec<AddedPackage>`, `removed_packages: Vec<RemovedPackage>`, `version_changes: Vec<VersionChange>`, `new_vulnerabilities: Vec<NewVulnerability>`, `resolved_vulnerabilities: Vec<ResolvedVulnerability>`, `license_changes: Vec<LicenseChange>`
- `AddedPackage` { name, version, license, advisory_count }
- `RemovedPackage` { name, version, license, advisory_count }
- `VersionChange` { name, left_version, right_version, direction } where direction is "upgrade" or "downgrade"
- `NewVulnerability` { advisory_id, severity, title, affected_package }
- `ResolvedVulnerability` { advisory_id, severity, title, previously_affected_package }
- `LicenseChange` { name, left_license, right_license }

**Service method** `compare(&self, left_id: Uuid, right_id: Uuid) -> Result<SbomComparisonResult, AppError>`:
1. Fetch both SBOMs using existing `SbomService::fetch()`. Return 404 if either does not exist.
2. Load packages for each SBOM via the `sbom_package` join table and `package` entity, including `package_license` mapping.
3. Load advisories for each SBOM via the `sbom_advisory` join table and `advisory` entity (which includes severity).
4. Compute diff by comparing package sets by name, version, and license; advisory sets by advisory ID.
5. Return `SbomComparisonResult` with all diff categories populated.

Use `common/src/db/query.rs` helpers for any filtering needed. Wrap database errors with `.context()` per the project's error handling convention (return `Result<T, AppError>`).

Per CONVENTIONS.md §Error Handling: all service methods return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's error handling scope.

Per CONVENTIONS.md §File Organization: each domain module follows `model/ + service/ + endpoints/` structure.
Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` matching the convention's module structure scope.

## Acceptance Criteria
- [ ] `SbomComparisonResult` and all sub-structs are defined with Serialize/Deserialize/ToSchema derives
- [ ] `SbomService::compare()` correctly computes diffs for added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes
- [ ] Returns 404 AppError when either SBOM ID does not exist
- [ ] Direction field correctly identifies "upgrade" vs "downgrade" for version changes

## Test Requirements
- [ ] Unit test: compare two SBOMs with known package sets, verify each diff category is correctly populated
- [ ] Unit test: compare identical SBOMs returns empty diff in all categories
- [ ] Unit test: nonexistent SBOM ID returns appropriate error

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003

[sdlc-workflow] Description digest: sha256-md:8c874297c5ab4adcef66e6cd894296586056686dfbdabfd9289a5a485bf58821
