# Task 1 — Add SBOM comparison model and service

## Repository
trustify-backend

## Target Branch
main

## Description
Add the data model types and service logic for computing a structured diff between two SBOMs. The service accepts two SBOM IDs, loads their associated packages, advisories, and licenses from the existing database, and produces a comparison result containing six diff categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. No new database tables are required — the diff is computed in-memory from existing entity data.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Comparison result struct and per-category diff structs (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)
- `modules/fundamental/src/sbom/service/compare.rs` — Comparison service logic: load packages and advisories for both SBOMs, compute set differences, detect version changes and license changes

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new model module
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod compare;` to expose the new service module

## Implementation Notes
- Follow the existing module pattern: model types in `model/` and service logic in `service/`. See `modules/fundamental/src/sbom/model/summary.rs` for the struct definition pattern (derive Serialize, Deserialize) and `modules/fundamental/src/sbom/service/sbom.rs` for the service method pattern.
- The SbomComparisonResult struct should contain six Vec fields matching the API response shape from the feature requirements:
  - `added_packages: Vec<AddedPackage>` — packages in right SBOM but not left
  - `removed_packages: Vec<RemovedPackage>` — packages in left SBOM but not right
  - `version_changes: Vec<VersionChange>` — packages in both with different versions (include direction: upgrade/downgrade)
  - `new_vulnerabilities: Vec<NewVulnerability>` — advisories affecting right but not left (include severity from AdvisorySummary)
  - `resolved_vulnerabilities: Vec<ResolvedVulnerability>` — advisories affecting left but not right
  - `license_changes: Vec<LicenseChange>` — packages whose license differs between left and right
- Use SeaORM queries to load package lists for each SBOM via the `sbom_package` join table (`entity/src/sbom_package.rs`), advisories via the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`), and license data via `package_license` (`entity/src/package_license.rs`).
- Reuse `PackageSummary` fields (name, version, license) from `modules/fundamental/src/package/model/summary.rs` and `AdvisorySummary` fields (severity) from `modules/fundamental/src/advisory/model/summary.rs` when constructing diff entries.
- All service methods should return `Result<T, AppError>` using `.context()` wrapping per the error handling convention. See `common/src/error.rs` for the `AppError` enum.
- Per CONVENTIONS.md §Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/sbom/service/compare.rs` matching the convention's Rust service file scope.
- Per CONVENTIONS.md §Module pattern: each domain module follows `model/ + service/ + endpoints/` structure.
  Applies: task creates files in `modules/fundamental/src/sbom/model/` and `modules/fundamental/src/sbom/service/` matching the convention's module structure scope.
- Non-functional requirement: comparison must complete in <1s for SBOMs with up to 2000 packages each. Design the diff algorithm with this in mind — use HashMaps keyed by package name for O(n) lookups rather than nested iteration.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with methods to fetch SBOM details and associated data; reuse its database query patterns for loading SBOM packages
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — existing struct with name, version, and license fields; reference its field definitions when creating diff entry structs
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — existing struct with severity field; reference for vulnerability diff entries
- `common/src/error.rs::AppError` — standard error type for all service returns
- `entity/src/sbom_package.rs` — SBOM-Package join table entity for loading packages per SBOM
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for loading advisories per SBOM
- `entity/src/package_license.rs` — Package-License mapping entity for loading license data

## Acceptance Criteria
- [ ] SbomComparisonResult and all six per-category diff structs are defined with Serialize/Deserialize derives
- [ ] Service method accepts two SBOM IDs and returns a populated SbomComparisonResult
- [ ] Added/removed packages are correctly identified by set difference on package names
- [ ] Version changes detect packages present in both SBOMs with differing versions and include upgrade/downgrade direction
- [ ] New and resolved vulnerabilities are identified by comparing advisory sets between the two SBOMs
- [ ] License changes detect packages whose license field differs between the two SBOMs
- [ ] All error paths return AppError with descriptive context messages

## Test Requirements
- [ ] Unit test: given two disjoint package sets, all packages from left appear in removed_packages and all from right in added_packages
- [ ] Unit test: given overlapping packages with version differences, version_changes correctly identifies direction (upgrade vs downgrade)
- [ ] Unit test: given advisories unique to each SBOM, new_vulnerabilities and resolved_vulnerabilities are correctly populated
- [ ] Unit test: given packages with changed licenses, license_changes entries are correct
- [ ] Unit test: comparing an SBOM with itself returns empty diff in all categories

## Dependencies
- None
