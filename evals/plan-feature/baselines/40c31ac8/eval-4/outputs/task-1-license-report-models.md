## Repository
trustify-backend

## Target Branch
main

## Description
Define the response model structs for the license compliance report and the license policy configuration struct. The report groups packages by license type and includes a compliance flag per group. The policy defines which licenses are considered non-compliant (a deny-list approach) and is loaded from a JSON configuration file in the repository.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod license_report;` declaration to expose the new model module

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — define `LicenseReport`, `LicenseGroup`, and `LicensePolicy` structs with serde Serialize/Deserialize derives

## Implementation Notes
Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs`. Each struct should derive `Clone`, `Debug`, `Serialize`, and `Deserialize`.

The `LicenseReport` struct should contain:
- `groups: Vec<LicenseGroup>` — one entry per distinct license
- `total_packages: usize` — total package count
- `non_compliant_count: usize` — number of groups flagged non-compliant

The `LicenseGroup` struct should contain:
- `license: String` — SPDX license identifier
- `packages: Vec<PackageSummary>` — packages with this license (reuse `PackageSummary` from `modules/fundamental/src/package/model/summary.rs`)
- `compliant: bool` — whether this license passes policy

The `LicensePolicy` struct should contain:
- `denied_licenses: Vec<String>` — list of SPDX identifiers that are non-compliant
- A `fn is_compliant(&self, license: &str) -> bool` method that checks whether a license is not in the denied list

Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` for any fallible operations in policy loading, with `.context()` wrapping for error messages. Applies: task modifies `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Module pattern: follow the `model/ + service/ + endpoints/` directory structure for the new license report module. Applies: task modifies `modules/fundamental/src/sbom/model/mod.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — reuse this struct in the `LicenseGroup.packages` field rather than defining a new package representation
- `common/src/error.rs::AppError` — use for policy file loading errors

## Acceptance Criteria
- [ ] `LicenseReport`, `LicenseGroup`, and `LicensePolicy` structs are defined with serde derives
- [ ] `LicensePolicy` has an `is_compliant` method that checks licenses against the denied list
- [ ] `license_report` module is declared in `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without errors (`cargo check -p trustify-fundamental`)

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors

## Additional Fields
- priority: Major
- fixVersions: RHTPA 1.5.0
- labels: ai-generated-jira
