# Task 1 — Backend SBOM comparison model and service

## Repository
trustify-backend

## Description
Create the data model structs and service method for computing a structured SBOM comparison diff. This is the core backend logic that takes two SBOM IDs, loads their packages and associated advisories/licenses, and computes the diff on-the-fly without creating any new database tables. The diff must include: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Defines `SbomComparisonResult`, `PackageDiffEntry`, `VersionChangeEntry`, `VulnerabilityDiffEntry`, and `LicenseChangeEntry` structs with Serialize derives

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new model module
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `compare(left_id, right_id)` method to `SbomService`

## API Changes
- Internal service API: `SbomService::compare(left_id: Uuid, right_id: Uuid) -> Result<SbomComparisonResult, AppError>` — NEW

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `details.rs` — these define domain structs with `#[derive(Serialize, Deserialize, Debug)]` and are organized as separate files under the `model/` directory.
- The `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs` already has `fetch` and `list` methods that demonstrate how to query the database using SeaORM and return typed results with `AppError` error handling.
- Use `PackageService` from `modules/fundamental/src/package/service/mod.rs` to fetch packages for each SBOM, keyed by package name. Use `AdvisoryService` from `modules/fundamental/src/advisory/service/advisory.rs` to fetch advisories associated with each SBOM.
- The `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` includes a `license` field — use this for license change detection.
- The `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` includes a `severity` field — use this for vulnerability diff entries.
- Compute the diff by building hash maps of packages keyed by name for both SBOMs, then comparing the sets. No new database tables are required per the non-functional requirements.
- Performance: the comparison must handle SBOMs with up to 2000 packages each within p95 < 1s. Use efficient set operations (HashSet/HashMap) rather than nested loops.
- Error handling: return `AppError` with `.context()` wrapping, consistent with the existing `SbomService` methods.
- The response shape must match the API contract specified in the feature:
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

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with database query patterns to follow for the new `compare` method
- `modules/fundamental/src/package/service/mod.rs::PackageService` — fetch packages associated with an SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — fetch advisories associated with an SBOM
- `common/src/error.rs::AppError` — standard error handling enum
- `entity/src/sbom_package.rs` — SBOM-to-package join table entity for querying packages by SBOM
- `entity/src/sbom_advisory.rs` — SBOM-to-advisory join table entity for querying advisories by SBOM
- `entity/src/package_license.rs` — Package-to-license mapping entity

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct is defined with all six diff categories as fields
- [ ] Each diff category uses a typed entry struct (`PackageDiffEntry`, `VersionChangeEntry`, `VulnerabilityDiffEntry`, `LicenseChangeEntry`)
- [ ] `SbomService::compare()` correctly identifies added packages (present in right, absent in left)
- [ ] `SbomService::compare()` correctly identifies removed packages (present in left, absent in right)
- [ ] `SbomService::compare()` correctly identifies version changes with upgrade/downgrade direction
- [ ] `SbomService::compare()` correctly identifies new vulnerabilities (advisories affecting right but not left)
- [ ] `SbomService::compare()` correctly identifies resolved vulnerabilities (advisories affecting left but not right)
- [ ] `SbomService::compare()` correctly identifies license changes for packages present in both SBOMs
- [ ] All error paths return `AppError` with context messages
- [ ] No new database tables are created

## Test Requirements
- [ ] Unit test: comparison of two SBOMs where one has additional packages returns correct `added_packages` and `removed_packages`
- [ ] Unit test: comparison where a shared package has different versions returns correct `version_changes` with direction
- [ ] Unit test: comparison where right SBOM has a new advisory returns correct `new_vulnerabilities`
- [ ] Unit test: comparison where left SBOM has an advisory not in right returns correct `resolved_vulnerabilities`
- [ ] Unit test: comparison where a shared package has a different license returns correct `license_changes`
- [ ] Unit test: comparison of identical SBOMs returns empty diff categories
- [ ] Unit test: error case when left or right SBOM ID does not exist

## Dependencies
- None — this is the foundational task
