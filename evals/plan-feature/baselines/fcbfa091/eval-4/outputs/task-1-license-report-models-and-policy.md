## Repository
trustify-backend

## Target Branch
main

## Description
Add the data model structs for the license compliance report and the license policy configuration. This task creates the foundational types that the service and endpoint layers will consume: `LicenseComplianceReport` (the top-level response), `LicenseGroup` (one group per distinct license), and `LicensePolicy` (the configurable allow/deny list of license identifiers). A default license policy JSON file is also added to the repository.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — Defines `LicenseComplianceReport`, `LicenseGroup`, and related structs with Serialize/Deserialize derives
- `modules/fundamental/src/sbom/model/license_policy.rs` — Defines `LicensePolicy` struct for loading and evaluating license allow/deny rules
- `license-policy.json` — Default license policy configuration file at the repository root

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` and `pub mod license_policy;` declarations

## Implementation Notes
Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs`. Each model struct should derive `Clone`, `Debug`, `Serialize`, `Deserialize`, and use `utoipa::ToSchema` for OpenAPI generation if the crate uses it.

The `LicenseComplianceReport` struct should contain:
- `sbom_id`: the SBOM identifier
- `groups`: `Vec<LicenseGroup>` — packages grouped by license
- `total_packages`: count of all packages evaluated
- `non_compliant_count`: count of packages with non-compliant licenses

The `LicenseGroup` struct should contain:
- `license`: `String` — the SPDX license identifier
- `packages`: `Vec<PackageLicenseEntry>` — packages using this license
- `compliant`: `bool` — whether this license passes the policy check

The `LicensePolicy` struct should:
- Load from the `license-policy.json` config file
- Support both an allow-list and a deny-list mode
- Provide a `fn is_compliant(&self, license: &str) -> bool` method

Reference the existing `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` which includes a `license` field -- the report model's `PackageLicenseEntry` should include the package name/purl and license.

Per CONVENTIONS.md (Key Conventions from repository structure): follow the model/ + service/ + endpoints/ module pattern.
Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` and `modules/fundamental/src/sbom/model/license_policy.rs` matching the convention's `.rs` module file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Reference for struct layout, derive macros, and serialization patterns
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Contains the `license` field; reuse the package identifier pattern for `PackageLicenseEntry`

## Acceptance Criteria
- [ ] `LicenseComplianceReport` and `LicenseGroup` structs are defined with appropriate serde derives
- [ ] `LicensePolicy` struct can be deserialized from a JSON config file
- [ ] `LicensePolicy::is_compliant()` correctly evaluates license identifiers against allow/deny lists
- [ ] Default `license-policy.json` contains a reasonable set of common permissive licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) as allowed
- [ ] Model module re-exports are added to `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Unit test: `LicensePolicy` deserialization from JSON string
- [ ] Unit test: `is_compliant` returns true for allowed licenses and false for denied licenses
- [ ] Unit test: `LicenseComplianceReport` serialization produces expected JSON structure with `groups`, `compliant` flags

## additional_fields
- labels: ai-generated-jira
- priority: Major
- fixVersions: RHTPA 1.5.0
