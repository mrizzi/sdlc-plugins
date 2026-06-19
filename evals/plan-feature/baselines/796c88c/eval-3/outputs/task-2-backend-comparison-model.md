## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Define the Rust structs that represent the SBOM comparison result. These model types will be returned by the comparison service and serialized as JSON by the comparison endpoint. The response shape must match the contract defined in the Figma design context: six diff categories (added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, license changes), each containing a list of typed entries.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Comparison result structs: `SbomComparison`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new module

## Implementation Notes
Follow the existing model pattern in `modules/fundamental/src/sbom/model/`. Each struct should derive `Serialize`, `Deserialize`, `Clone`, `Debug`, and `PartialEq`.

Struct definitions:

```rust
#[derive(Serialize, Deserialize, Clone, Debug, PartialEq)]
pub struct SbomComparison {
    pub added_packages: Vec<AddedPackage>,
    pub removed_packages: Vec<RemovedPackage>,
    pub version_changes: Vec<VersionChange>,
    pub new_vulnerabilities: Vec<NewVulnerability>,
    pub resolved_vulnerabilities: Vec<ResolvedVulnerability>,
    pub license_changes: Vec<LicenseChange>,
}
```

- `AddedPackage` / `RemovedPackage`: fields `name: String`, `version: String`, `license: String`, `advisory_count: u32`
- `VersionChange`: fields `name: String`, `left_version: String`, `right_version: String`, `direction: String` (values: "upgrade" or "downgrade")
- `NewVulnerability` / `ResolvedVulnerability`: fields `advisory_id: String`, `severity: String`, `title: String`, `affected_package: String` (use `previously_affected_package` for resolved)
- `LicenseChange`: fields `name: String`, `left_license: String`, `right_license: String`

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Reference for struct conventions (derive macros, field naming)
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — Reference for struct conventions
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Contains `license` field pattern
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Contains `severity` field pattern

## Acceptance Criteria
- [ ] `SbomComparison` struct and all sub-structs are defined in `comparison.rs`
- [ ] All structs derive `Serialize`, `Deserialize`, `Clone`, `Debug`, `PartialEq`
- [ ] Module is exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Project compiles successfully (`cargo check`)

## Test Requirements
- [ ] Struct serialization produces the expected JSON shape matching the API contract

## Dependencies
- Depends on: Task 1 — Create feature branch
