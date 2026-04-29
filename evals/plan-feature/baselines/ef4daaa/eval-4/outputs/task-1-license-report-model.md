# Task 1 -- Add License Report Model and Policy Configuration

## Repository
trustify-backend

## Description
Define the data model structs for the license compliance report and the license policy
configuration. The report groups packages by license type and flags non-compliant licenses
based on a configurable policy. The policy is stored as a JSON configuration file in the
repository, specifying allowed and denied license identifiers (using SPDX license IDs).

This task lays the foundation for the license report service and endpoint (Tasks 2 and 3).

## Files to Modify
- `modules/fundamental/src/sbom/mod.rs` -- add `license_report` sub-module declaration

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` -- LicenseGroup and LicenseReport structs
- `license-policy.json` -- default license policy configuration file at the repo root

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and
  `modules/fundamental/src/sbom/model/details.rs` for struct definitions and serde derives.
- The `LicenseReport` struct should contain a `groups` field: `Vec<LicenseGroup>`.
- The `LicenseGroup` struct should contain:
  - `license: String` -- the SPDX license identifier
  - `packages: Vec<PackageSummary>` -- packages using this license (reuse the existing
    `PackageSummary` from `modules/fundamental/src/package/model/summary.rs`)
  - `compliant: bool` -- whether this license is compliant with the policy
- The policy configuration struct (`LicensePolicy`) should support:
  - `allowed_licenses: Vec<String>` -- allowlist of SPDX IDs (if non-empty, only these are compliant)
  - `denied_licenses: Vec<String>` -- denylist of SPDX IDs (these are always non-compliant)
- Use `serde::Deserialize` for loading the policy from JSON.
- Reference the existing `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs`
  which already includes a `license` field -- this is the data source for grouping.
- Per constraints doc section 5: implementation must follow patterns found in existing code.

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` -- already contains
  `license` field; reuse this struct in LicenseGroup.packages rather than defining a new type
- `common/src/model/paginated.rs::PaginatedResults` -- reference for response wrapper patterns
  (though the report is not paginated, it demonstrates the project's serialization conventions)

## Acceptance Criteria
- [ ] `LicenseReport` and `LicenseGroup` structs are defined with serde Serialize/Deserialize
- [ ] `LicensePolicy` struct is defined with serde Deserialize for JSON loading
- [ ] A default `license-policy.json` file exists at the repo root with a reasonable default policy
- [ ] The model structs are exported from the sbom module
- [ ] The response shape matches the specification: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`

## Test Requirements
- [ ] Unit test: `LicensePolicy` deserializes correctly from a JSON string with both allowed and denied lists
- [ ] Unit test: `LicenseReport` serializes to the expected JSON shape matching the API contract
- [ ] Unit test: empty policy (no allowed/denied) treats all licenses as compliant

## Documentation Updates
- `license-policy.json` -- include inline comments or a companion `LICENSE-POLICY.md` explaining
  the policy format, SPDX license identifiers, and how to customize
