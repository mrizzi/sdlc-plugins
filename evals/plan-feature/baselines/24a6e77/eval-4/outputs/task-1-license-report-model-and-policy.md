# Task 1 — Add License Report Model and Policy Configuration

## Repository
trustify-backend

## Description
Define the response model for the license compliance report and the license policy configuration schema. The report model represents packages grouped by license type with a compliance flag per group. The policy configuration is a JSON file that declares which licenses are allowed or denied, loaded at service startup.

This task lays the data-model foundation that the service layer (Task 2) and endpoint (Task 3) will build upon.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — `LicenseReportGroup` and `LicenseReport` response structs
- `license-policy.json` — Default license policy configuration file at the repository root (or a documented config directory)

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to expose the new module

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs`: each model file defines a struct that derives `Serialize`, `Deserialize`, and `Clone`.
- The `LicenseReport` struct should contain:
  - `groups: Vec<LicenseReportGroup>` — one entry per distinct license
- The `LicenseReportGroup` struct should contain:
  - `license: String` — SPDX license identifier
  - `packages: Vec<PackageSummary>` — packages using this license (reuse existing `PackageSummary` from `modules/fundamental/src/package/model/summary.rs`)
  - `compliant: bool` — whether this license is compliant with the configured policy
- The license policy JSON schema should support at minimum:
  - `allowed_licenses: Vec<String>` — allowlist of SPDX identifiers (if non-empty, only these are compliant)
  - `denied_licenses: Vec<String>` — denylist of SPDX identifiers (always non-compliant)
- Define a `LicensePolicy` struct (with `Serialize`, `Deserialize`) to deserialize the config file.
- Per constraints doc section 5 (Code Change Rules): keep changes scoped to the files listed above.

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — existing struct representing a package with its license field; reuse directly in `LicenseReportGroup.packages` rather than defining a new package representation
- `common/src/error.rs::AppError` — use for policy file loading errors (e.g., missing or malformed config)

## Acceptance Criteria
- [ ] `LicenseReport` and `LicenseReportGroup` structs compile and are exported from the sbom model module
- [ ] `LicensePolicy` struct can deserialize a well-formed `license-policy.json` file
- [ ] A default `license-policy.json` file exists with documented schema
- [ ] The response shape matches the spec: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`

## Test Requirements
- [ ] Unit test that `LicensePolicy` correctly deserializes a sample JSON policy with both allowed and denied lists
- [ ] Unit test that `LicensePolicy` returns a deserialization error for malformed JSON
- [ ] Unit test that `LicenseReport` serializes to the expected JSON shape
