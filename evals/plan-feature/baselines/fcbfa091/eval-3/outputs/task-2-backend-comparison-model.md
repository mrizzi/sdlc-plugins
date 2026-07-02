## additional_fields
```
{ "labels": ["ai-generated-jira"], "priority": {"name": "Critical"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }
```

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Define the Rust data model structs for the SBOM comparison result. These structs represent the structured diff between two SBOMs, covering six categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. The models will be consumed by the comparison service (Task 3) and serialized as the JSON response by the comparison endpoint (Task 4).

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Comparison result structs: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new model module

## Implementation Notes
Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for struct definition conventions (derive macros, serde attributes, field naming).

The `SbomComparisonResult` struct contains six `Vec` fields: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`.

Sub-struct field definitions:
- `AddedPackage` / `RemovedPackage`: `name: String`, `version: String`, `license: String`, `advisory_count: usize`
- `VersionChange`: `name: String`, `left_version: String`, `right_version: String`, `direction: String` (values: "upgrade" or "downgrade")
- `NewVulnerability`: `advisory_id: String`, `severity: String`, `title: String`, `affected_package: String`
- `ResolvedVulnerability`: `advisory_id: String`, `severity: String`, `title: String`, `previously_affected_package: String`
- `LicenseChange`: `name: String`, `left_license: String`, `right_license: String`

All structs must derive `Serialize`, `Deserialize`, `Clone`, `Debug` and use `#[serde(rename_all = "snake_case")]` to match the API contract from the Figma design specification.

No new database tables required — these are computed structs, not SeaORM entities.

Per CONVENTIONS.md §Module pattern: each domain module follows `model/ + service/ + endpoints/` structure. The comparison model belongs in `modules/fundamental/src/sbom/model/` alongside existing `summary.rs` and `details.rs`.
Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Example of model struct pattern with serde derives and field conventions
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — Example of detailed model struct with nested types
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Contains severity field pattern to reference for vulnerability structs
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Contains license field pattern to reference for package structs

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct is defined with all six diff category `Vec` fields
- [ ] All sub-structs (`AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`) are defined with correct fields
- [ ] All structs derive `Serialize`, `Deserialize`, `Clone`, `Debug` and use `snake_case` field naming
- [ ] Module is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] JSON serialization output matches the expected API response shape from the Figma design specification

## Test Requirements
- [ ] Verify that `SbomComparisonResult` can be serialized to JSON matching the expected API response shape
- [ ] Verify that an empty `SbomComparisonResult` (all empty Vecs) serializes correctly
- [ ] Verify that `VersionChange.direction` serializes as "upgrade" or "downgrade" string values

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
