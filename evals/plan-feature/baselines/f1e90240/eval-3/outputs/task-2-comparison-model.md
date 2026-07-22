# Task 2: Add SBOM comparison model types

- **Jira parent**: TC-9003
- **Priority**: Critical
- **Fix Versions**: RHTPA 1.5.0
- **Dependencies**: Task 1

## Repository

trustify-backend

## Target Branch

TC-9003

## Description

Define the Rust data structures that represent the result of comparing two SBOMs. These model types are the contract between the backend comparison service and the REST endpoint, and they also define the JSON response shape consumed by the frontend.

The comparison result contains six diff categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. Each category has its own struct with fields matching the API contract specified in the feature requirements.

## Files to Create

- `modules/fundamental/src/sbom/model/comparison.rs` -- Structs: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`

## Files to Modify

- `modules/fundamental/src/sbom/model/mod.rs` -- Add `pub mod comparison;` declaration

## Acceptance Criteria

- [ ] `SbomComparisonResult` struct contains fields for all six diff categories (`added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`)
- [ ] Each category struct has the correct fields matching the API contract:
  - `AddedPackage`: name, version, license, advisory_count
  - `RemovedPackage`: name, version, license, advisory_count
  - `VersionChange`: name, left_version, right_version, direction (enum: upgrade/downgrade)
  - `NewVulnerability`: advisory_id, severity, title, affected_package
  - `ResolvedVulnerability`: advisory_id, severity, title, previously_affected_package
  - `LicenseChange`: name, left_license, right_license
- [ ] All structs derive `Serialize`, `Deserialize`, `Clone`, `Debug`
- [ ] Module compiles without errors

## Test Requirements

- Unit tests verifying serialization round-trip for `SbomComparisonResult` with sample data.
- Test that `VersionChange.direction` serializes to lowercase `"upgrade"` / `"downgrade"` strings.

## Implementation Notes

Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `details.rs`. Each struct should derive `serde::Serialize` and `serde::Deserialize`. Use `#[serde(rename_all = "snake_case")]` on enums for consistent JSON output.

The `direction` field on `VersionChange` should be a `Direction` enum with variants `Upgrade` and `Downgrade`, with serde rename to snake_case.

## Applicable Conventions

- **Module pattern** (model/ + service/ + endpoints/): Applies: task modifies `modules/fundamental/src/sbom/model/` matching the convention's module structure scope.
