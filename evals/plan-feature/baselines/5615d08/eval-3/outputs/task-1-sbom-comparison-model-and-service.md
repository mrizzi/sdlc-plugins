## Repository
trustify-backend

## Description
Implement the domain model and service logic for SBOM comparison. This task introduces the data structures that represent a structured diff between two SBOMs (added/removed packages, version changes, new/resolved vulnerabilities, and license changes) and the service method that computes the diff on-the-fly from existing package, advisory, and license data. No new database tables are required; the diff is computed by querying both SBOMs' related entities and comparing them in memory.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Structs for the comparison result: `SbomComparison`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`
- `modules/fundamental/src/sbom/service/compare.rs` — `SbomService::compare()` method implementation that fetches packages, advisories, and licenses for both SBOMs and computes the diff

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new model module
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod compare;` to expose the new service module

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `details.rs` for struct definitions. Each struct should derive `Serialize, Deserialize, Clone, Debug`.
- The `SbomComparison` struct should contain six fields matching the API response shape defined in the feature requirements: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`.
- The `PackageDiff` struct should include `name: String`, `version: String`, `license: String`, `advisory_count: u64` — matching the `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` which already has `license` field.
- The `VulnerabilityDiff` struct should include `advisory_id: String`, `severity: String`, `title: String`, `affected_package: String` — matching fields from `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` which has a `severity` field.
- The `VersionChange` struct should include `name: String`, `left_version: String`, `right_version: String`, `direction: String` (either "upgrade" or "downgrade").
- The `LicenseChange` struct should include `name: String`, `left_license: String`, `right_license: String`.
- In the `compare` service method, use `PackageService` from `modules/fundamental/src/package/service/mod.rs` to fetch package lists for each SBOM, and `AdvisoryService` from `modules/fundamental/src/advisory/service/advisory.rs` to fetch advisories linked to each SBOM.
- Use the SBOM-Package join table entity at `entity/src/sbom_package.rs` and the SBOM-Advisory join table at `entity/src/sbom_advisory.rs` to query relationships.
- Use query helpers from `common/src/db/query.rs` for any filtering operations.
- Return `Result<SbomComparison, AppError>` following the error pattern in `common/src/error.rs`.
- For performance (p95 < 1s for 2000 packages), load all packages for both SBOMs in two bulk queries, then diff in memory using HashMaps keyed by package name.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Extend this service with the comparison method to keep SBOM-related logic co-located
- `modules/fundamental/src/package/service/mod.rs::PackageService` — Reuse to fetch package lists per SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — Reuse to fetch advisories per SBOM
- `common/src/error.rs::AppError` — Use the existing error type for all error returns
- `entity/src/sbom_package.rs` — SBOM-Package join entity for querying packages belonging to an SBOM
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join entity for querying advisories linked to an SBOM

## Acceptance Criteria
- [ ] `SbomComparison` struct serializes to JSON matching the expected response shape from the feature spec
- [ ] `SbomService::compare(left_id, right_id)` returns correct diff when given two SBOM IDs with overlapping and non-overlapping packages
- [ ] Added packages are those in the right SBOM but not in the left
- [ ] Removed packages are those in the left SBOM but not in the right
- [ ] Version changes are detected for packages present in both SBOMs with different versions
- [ ] Direction field correctly identifies upgrades vs downgrades
- [ ] New vulnerabilities are advisories affecting the right SBOM but not the left
- [ ] Resolved vulnerabilities are advisories affecting the left SBOM but not the right
- [ ] License changes are detected for packages present in both SBOMs with different licenses
- [ ] Method returns `AppError` for invalid SBOM IDs

## Test Requirements
- [ ] Unit test: comparing two SBOMs where the right has additional packages returns them in `added_packages`
- [ ] Unit test: comparing two SBOMs where the left has packages not in the right returns them in `removed_packages`
- [ ] Unit test: package present in both SBOMs with different versions appears in `version_changes` with correct direction
- [ ] Unit test: advisory linked to right SBOM but not left appears in `new_vulnerabilities`
- [ ] Unit test: advisory linked to left SBOM but not right appears in `resolved_vulnerabilities`
- [ ] Unit test: package with changed license appears in `license_changes`
- [ ] Unit test: comparing an SBOM with itself returns empty diff

## Verification Commands
- `cargo test -p trustify-fundamental -- sbom::compare` — All comparison service unit tests pass
