## Repository
trustify-backend

## Description
Add the license policy configuration model and the license report response models needed by the compliance report feature. The license policy is a JSON configuration file that defines lists of allowed and denied licenses, enabling organizations to customize their compliance rules. The report models define the structured response shape for the license report endpoint.

## Files to Create
- `common/src/model/license_policy.rs` — LicensePolicy struct that deserializes from a JSON config file, containing allowed_licenses and denied_licenses lists, and a method to evaluate whether a given SPDX license identifier is compliant
- `modules/fundamental/src/sbom/model/license_report.rs` — LicenseReportGroup struct (license name, list of packages, compliant flag) and LicenseReport struct (list of LicenseReportGroup entries) for the API response
- `license-policy.json` — Default license policy configuration file at the repository root with a starter set of common compliant licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) and an empty denied list

## Files to Modify
- `common/src/model/mod.rs` — Add `pub mod license_policy;` to expose the new module
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to expose the new report models

## Implementation Notes
- Follow the existing model pattern used in `common/src/model/paginated.rs` for struct definition style (derive Serialize, Deserialize, Clone, Debug)
- The LicensePolicy struct should implement a `fn is_compliant(&self, license_id: &str) -> bool` method that checks the license identifier against the allowed and denied lists. If denied_licenses is non-empty and contains the license, return false. If allowed_licenses is non-empty and does not contain the license, return false. Otherwise return true.
- The LicenseReport response model should follow the pattern of existing response structs like `SbomDetails` in `modules/fundamental/src/sbom/model/details.rs` — derive Serialize/Deserialize and use serde attributes for consistent JSON field naming
- The LicenseReportGroup struct fields: `license: String`, `packages: Vec<PackageSummary>`, `compliant: bool` — reuse the existing `PackageSummary` struct from `modules/fundamental/src/package/model/summary.rs`
- The LicenseReport struct fields: `groups: Vec<LicenseReportGroup>`
- The license policy JSON config file should be loaded at service initialization time, not per-request, for performance
- Per constraints doc section 5: all code must follow patterns referenced in implementation notes

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults` — demonstrates the established pattern for response model structs (derive macros, serde attributes)
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — demonstrates domain-specific response model pattern within the SBOM module
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — reuse directly as the package representation within license report groups

## Acceptance Criteria
- [ ] LicensePolicy struct can be deserialized from a JSON file containing `allowed_licenses` and `denied_licenses` string arrays
- [ ] LicensePolicy.is_compliant() correctly returns true for allowed licenses, false for denied licenses, and handles the case where both lists are empty (default: compliant)
- [ ] LicenseReport and LicenseReportGroup structs serialize to JSON matching the specified response shape: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`
- [ ] Default license-policy.json file is valid JSON and deserializes successfully into LicensePolicy
- [ ] New modules are properly exported from their parent mod.rs files

## Test Requirements
- [ ] Unit test: LicensePolicy deserialization from valid JSON
- [ ] Unit test: LicensePolicy.is_compliant() returns true for an allowed license
- [ ] Unit test: LicensePolicy.is_compliant() returns false for a denied license
- [ ] Unit test: LicensePolicy.is_compliant() returns false for an unlisted license when allowed_licenses is non-empty
- [ ] Unit test: LicensePolicy.is_compliant() returns true when both lists are empty (permissive default)
- [ ] Unit test: LicenseReport serializes to expected JSON structure

## Verification Commands
- `cargo build -p common` — compiles without errors
- `cargo build -p trustify-module-fundamental` — compiles without errors
- `cargo test -p common` — all tests pass including new license policy tests
