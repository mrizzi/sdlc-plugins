## Repository
trustify-backend

## Target Branch
main

## Description
Define the Rust model types for the SBOM comparison result. These types represent the structured diff between two SBOMs: added/removed packages, version changes, new/resolved vulnerabilities, and license changes. They will be serialized as JSON by the comparison endpoint.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Struct definitions for `SbomComparisonResult`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, and `LicenseChange`, all deriving `Serialize` and `Deserialize`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new model module

## API Changes
- No endpoint changes in this task (model only)

## Implementation Notes
Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` where structs derive `serde::Serialize`, `serde::Deserialize`, and `Clone`.

Define the following structs:

```rust
pub struct SbomComparisonResult {
    pub added_packages: Vec<PackageDiff>,
    pub removed_packages: Vec<PackageDiff>,
    pub version_changes: Vec<VersionChange>,
    pub new_vulnerabilities: Vec<VulnerabilityDiff>,
    pub resolved_vulnerabilities: Vec<VulnerabilityDiff>,
    pub license_changes: Vec<LicenseChange>,
}

pub struct PackageDiff {
    pub name: String,
    pub version: String,
    pub license: Option<String>,
    pub advisory_count: u32,
}

pub struct VersionChange {
    pub name: String,
    pub left_version: String,
    pub right_version: String,
    pub direction: String, // "upgrade" or "downgrade"
}

pub struct VulnerabilityDiff {
    pub advisory_id: String,
    pub severity: String,
    pub title: String,
    pub affected_package: String,
}

pub struct LicenseChange {
    pub name: String,
    pub left_license: String,
    pub right_license: String,
}
```

Use `serde(rename_all = "snake_case")` on enums/structs as is conventional in the codebase.

Per Key Conventions (Module pattern): Place model types under `model/` within the `sbom` module. Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` matching the convention's model directory scope.

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct is defined with all six diff category fields
- [ ] All sub-types (`PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`) are defined
- [ ] All structs derive `Serialize`, `Deserialize`, `Clone`
- [ ] Module is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles with `cargo check`

## Test Requirements
- [ ] `cargo check` passes with the new model types
- [ ] Verify `serde_json::to_string` round-trip on `SbomComparisonResult` in a unit test

## Dependencies
- Depends on: None — this is the first task

[sdlc-workflow] Description digest: sha256-md:828d2660c04d111dfe8c9e560a238e3d2d141654ce5d901e31c66150aad2d80f
