## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the SBOM comparison diff model structs and service logic to compute a structured diff between two SBOMs. The service fetches packages, advisories, and licenses for both SBOMs using the existing SbomService, PackageService, and AdvisoryService, then computes added/removed packages, version changes, new/resolved vulnerabilities, and license changes. No new database tables are required — the diff is computed on-the-fly from existing data.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Diff result structs: SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange
- `modules/fundamental/src/sbom/service/comparison.rs` — SbomComparisonService with a `compare(left_id, right_id)` method that computes the diff

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new model module
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod comparison;` to expose the new service module
- `modules/fundamental/src/sbom/mod.rs` — Re-export comparison types if needed for endpoint use

## Implementation Notes
- Follow the existing module pattern: each domain module uses `model/ + service/ + endpoints/` structure. The comparison model goes in `model/comparison.rs` and the service in `service/comparison.rs`.
- Reuse `SbomService` (in `modules/fundamental/src/sbom/service/sbom.rs`) to fetch SBOM details for both left and right IDs.
- Reuse `PackageService` (in `modules/fundamental/src/package/service/mod.rs`) to list packages per SBOM.
- Reuse `AdvisoryService` (in `modules/fundamental/src/advisory/service/advisory.rs`) to find advisories linked to each SBOM.
- Use `PackageSummary` (in `modules/fundamental/src/package/model/summary.rs`) which includes the `license` field for license change detection.
- Use `AdvisorySummary` (in `modules/fundamental/src/advisory/model/summary.rs`) which includes the `severity` field for vulnerability classification.
- All handlers return `Result<T, AppError>` with `.context()` wrapping — follow the error handling pattern in `common/src/error.rs`.
- The comparison must handle SBOMs with up to 2000 packages each with p95 response time under 1 second. Use HashMaps keyed by package name for O(n) diff computation rather than nested loops.
- Per the non-functional requirements, no new database tables should be created. Compute the diff entirely from existing entity data (sbom, package, sbom_package, advisory, sbom_advisory, package_license).
- The `SbomComparisonResult` struct should be serializable (derive `Serialize`) for JSON response output.
- The `direction` field in `VersionChange` should be an enum with values `Upgrade` and `Downgrade`, determined by comparing semver versions where possible.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Provides fetch and list operations for SBOMs; use to retrieve SBOM details for both comparison sides
- `modules/fundamental/src/package/service/mod.rs::PackageService` — Provides package listing; use to get packages per SBOM for diff computation
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — Provides advisory listing and search; use to find advisories linked to each SBOM
- `common/src/model/paginated.rs::PaginatedResults` — Standard response wrapper used by list endpoints; reference for response type patterns
- `common/src/error.rs::AppError` — Standard error enum; use for all error returns in comparison service

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct contains fields for all six diff categories: added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes
- [ ] Each diff category struct contains the fields specified in the API response shape (see feature requirements)
- [ ] `SbomComparisonService::compare(left_id, right_id)` returns a populated `SbomComparisonResult` by diffing actual SBOM data
- [ ] Service correctly identifies packages present only in the right SBOM as "added" and only in the left as "removed"
- [ ] Service correctly detects version changes for packages present in both SBOMs
- [ ] Service correctly identifies new vulnerabilities (advisories in right but not left) and resolved vulnerabilities (in left but not right)
- [ ] Service correctly detects license changes for packages present in both SBOMs
- [ ] All error paths use `AppError` with `.context()` wrapping

## Test Requirements
- [ ] Unit tests for the comparison logic covering: two identical SBOMs (empty diff), completely disjoint SBOMs (all added/removed), SBOMs with overlapping packages at different versions
- [ ] Test that version direction classification correctly identifies upgrades vs downgrades
- [ ] Test that new and resolved vulnerabilities are correctly classified based on advisory presence

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main (trustify-backend)