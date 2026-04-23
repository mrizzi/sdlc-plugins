## Repository
trustify-backend

## Description
Define the data model structs for the license compliance report and implement the license policy loader/evaluator. The report model represents packages grouped by license with a compliance flag per group. The policy module reads a JSON configuration file that declares which licenses are allowed, denied, or require review, and evaluates each license group against it.

## Files to Modify
- `modules/fundamental/src/sbom/mod.rs` -- add `pub mod license_report;` declaration to register the new submodule

## Files to Create
- `modules/fundamental/src/sbom/license_report/mod.rs` -- module root; re-exports model, policy, service, and endpoints submodules
- `modules/fundamental/src/sbom/license_report/model.rs` -- defines `LicenseGroup` (license name, list of packages, compliant flag) and `LicenseReport` (list of groups, overall compliant flag) structs with Serialize derives
- `modules/fundamental/src/sbom/license_report/policy.rs` -- defines `LicensePolicy` struct (allowed_licenses, denied_licenses), `load_policy(path)` function to read from a JSON config file, and `evaluate(license: &str) -> bool` method that returns whether a license is compliant
- `license-policy.json` -- default policy file at the repository root with a starter set of allowed SPDX licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) and denied licenses (GPL-3.0-only, AGPL-3.0-only)

## API Changes
- None in this task (model and policy only; endpoint comes in Task 3)

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `details.rs` -- use `#[derive(Clone, Debug, Serialize, Deserialize)]` and keep structs in a dedicated model file.
- The `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` includes a `license` field -- the report model should reference or align with this representation.
- The policy evaluator should be a pure function with no database dependency so it can be unit-tested independently.
- Use `serde_json::from_reader` to load the policy JSON file. Accept the policy path as a configurable parameter (with a default fallback to `license-policy.json` in the working directory).

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` -- contains the `license` field that the report groups by
- `common/src/error.rs::AppError` -- use for error propagation if the policy file is missing or malformed

## Acceptance Criteria
- [ ] `LicenseReport` and `LicenseGroup` structs are defined with appropriate Serialize derives
- [ ] `LicensePolicy` can be deserialized from a JSON file
- [ ] `LicensePolicy::evaluate` correctly classifies allowed and denied licenses
- [ ] A default `license-policy.json` exists in the repository root with starter SPDX license entries
- [ ] The `license_report` submodule is registered in `modules/fundamental/src/sbom/mod.rs`

## Test Requirements
- [ ] Unit test: `LicensePolicy::evaluate` returns `true` for an allowed license (e.g., "MIT")
- [ ] Unit test: `LicensePolicy::evaluate` returns `false` for a denied license (e.g., "GPL-3.0-only")
- [ ] Unit test: `LicensePolicy::evaluate` handles an unknown license not in either list (define expected behavior: default-deny or default-allow based on policy config)
- [ ] Unit test: `load_policy` returns an error for a missing or malformed JSON file
- [ ] Unit test: `LicenseReport` serializes to the expected JSON shape `{ groups: [{ license, packages, compliant }] }`

## Dependencies
- None (this is the foundational task)
