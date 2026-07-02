## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the data model structs and diff computation service for SBOM comparison. The model defines the structured diff response (added/removed packages, version changes, new/resolved vulnerabilities, license changes). The service computes the diff on-the-fly by querying existing package, advisory, and license data for both SBOMs and comparing them -- no new database tables are needed.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- add `pub mod comparison;` to export the new comparison model module
- `modules/fundamental/src/sbom/service/mod.rs` -- add `pub mod compare;` to export the new comparison service module

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` -- structs: `SbomComparison`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`; all derive `Serialize, Deserialize, Clone, Debug`
- `modules/fundamental/src/sbom/service/compare.rs` -- `SbomCompareService` with `compare(left_id, right_id, db) -> Result<SbomComparison, AppError>` method; loads packages for both SBOMs via `PackageService`, advisories via `AdvisoryService`, then diffs

## API Changes
None (service layer only; endpoint added in Task 4)

## Implementation Notes
- Follow the existing module pattern: model structs in `model/`, service logic in `service/`.
- Reuse `PackageService` from `modules/fundamental/src/package/service/mod.rs` to fetch packages for each SBOM.
- Reuse `AdvisoryService` from `modules/fundamental/src/advisory/service/advisory.rs` to fetch advisories linked to each SBOM.
- Reuse `PackageSummary` from `modules/fundamental/src/package/model/summary.rs` which includes the `license` field needed for license change detection.
- Reuse `AdvisorySummary` from `modules/fundamental/src/advisory/model/summary.rs` which includes the `severity` field needed for vulnerability classification.
- Diff algorithm: build HashMaps keyed by package name for each SBOM, then iterate to classify packages as added, removed, version-changed, or license-changed. For vulnerabilities, diff advisory sets by advisory ID.
- The `direction` field on `VersionChange` should be "upgrade" or "downgrade" based on semver comparison.
- Per CONVENTIONS.md §Error Handling: wrap all fallible operations with `.context()` and return `Result<T, AppError>`. Applies: task modifies `modules/fundamental/src/sbom/service/compare.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `modules/fundamental/src/package/service/mod.rs::PackageService` -- fetches package lists for an SBOM; reuse to get left/right package sets
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` -- fetches advisories linked to an SBOM; reuse to get left/right advisory sets
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` -- includes name, version, license fields needed for comparison
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- includes advisory_id, severity, title fields needed for vulnerability diff
- `common/src/error.rs::AppError` -- standard error type; use for all error returns

## Acceptance Criteria
- [ ] `SbomComparison` struct serializes to the JSON shape specified in the feature description (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
- [ ] `SbomCompareService::compare()` correctly identifies added packages (in right but not left)
- [ ] `SbomCompareService::compare()` correctly identifies removed packages (in left but not right)
- [ ] `SbomCompareService::compare()` correctly identifies version changes with upgrade/downgrade direction
- [ ] `SbomCompareService::compare()` correctly identifies new and resolved vulnerabilities
- [ ] `SbomCompareService::compare()` correctly identifies license changes
- [ ] All errors are wrapped with `.context()` per Error Handling conventions

## Test Requirements
- [ ] Unit test: comparing two empty SBOMs returns all-empty diff sections
- [ ] Unit test: comparing an SBOM with packages against an empty SBOM returns all packages as removed
- [ ] Unit test: packages with same name but different versions appear in version_changes with correct direction
- [ ] Unit test: advisories present only in right SBOM appear as new_vulnerabilities
- [ ] Unit test: license changes are detected when same package has different license strings

## Verification Commands
- `cargo test -p trustify-fundamental -- sbom::service::compare` -- all comparison service unit tests pass
- `cargo check -p trustify-fundamental` -- no compilation errors

## Dependencies
- Depends on: Task 1 -- Create feature branch (trustify-backend)

## Additional Fields
- priority: Critical
- fixVersions: RHTPA 1.5.0
- labels: ai-generated-jira
