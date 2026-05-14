## Repository
trustify-backend

## Target Branch
main

## Description
Add the license policy configuration model and the license compliance report response models. The license policy defines which licenses are allowed, denied, or flagged for review, and is loaded from a JSON configuration file in the repository. The report models define the API response structure for the license compliance report endpoint.

## Files to Create
- `common/src/model/license_policy.rs` — Rust structs for the license policy configuration (`LicensePolicy`, `PolicyRule`) with serde deserialization from JSON, plus a loader function that reads the policy from a configurable file path
- `modules/fundamental/src/sbom/model/license_report.rs` — Rust structs for the license report response (`LicenseReport`, `LicenseReportGroup`) with serde serialization

## Files to Modify
- `common/src/model/mod.rs` — Add `pub mod license_policy;` to expose the new policy module
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to expose the new report model module

## Implementation Notes
- **License policy structure:** Define a `LicensePolicy` struct containing a `Vec<PolicyRule>` where each `PolicyRule` has a `license` field (SPDX identifier string, e.g., "MIT", "GPL-3.0-only") and a `compliance` field (enum: `Allowed`, `Denied`, `Review`). Include a default policy that treats unlisted licenses as `Review`.
- **Policy loading:** Implement a `LicensePolicy::load(path: &Path) -> Result<Self, AppError>` method that reads and deserializes a JSON file. Follow the error handling pattern used in `common/src/error.rs` — return `Result<T, AppError>` with `.context()` wrapping from anyhow.
- **Report model structure:** Define `LicenseReport` with a `groups: Vec<LicenseReportGroup>` field. Each `LicenseReportGroup` has: `license: String` (SPDX identifier), `packages: Vec<PackageSummary>` (reuse the existing `PackageSummary` from `modules/fundamental/src/package/model/summary.rs`), and `compliant: bool` (derived from the policy evaluation).
- **Serialization:** Both the policy and report models must derive `serde::Serialize` and `serde::Deserialize`. The report models are serialized in API responses; the policy model is deserialized from the config file.
- **Reuse `PackageSummary`:** The `LicenseReportGroup.packages` field should use the existing `PackageSummary` struct from `modules/fundamental/src/package/model/summary.rs` rather than defining a new package representation.

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Existing package summary struct that includes a `license` field; reuse as the package representation within each license group
- `common/src/error.rs::AppError` — Existing error type implementing `IntoResponse`; use for policy loading errors

## Acceptance Criteria
- [ ] `LicensePolicy` struct can be deserialized from a JSON file containing license rules
- [ ] `LicensePolicy::load()` returns a meaningful `AppError` when the file is missing or malformed
- [ ] `LicenseReport` and `LicenseReportGroup` structs are defined with serde serialization
- [ ] `LicenseReportGroup` uses `PackageSummary` from the existing package model
- [ ] Both new modules are publicly exported from their parent `mod.rs` files

## Test Requirements
- [ ] Unit test: deserialize a valid `LicensePolicy` JSON string with allowed, denied, and review rules
- [ ] Unit test: deserialize an empty policy (no rules) and verify default behavior treats all licenses as review
- [ ] Unit test: verify `LicensePolicy::load()` returns an error for a nonexistent file path
- [ ] Unit test: serialize a `LicenseReport` with multiple groups and verify the JSON structure matches the expected format `{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }] }`
