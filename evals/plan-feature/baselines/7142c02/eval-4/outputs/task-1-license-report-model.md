## Repository
trustify-backend

## Target Branch
main

## Description
Define the data model structs for the license compliance report and the license policy configuration schema. This establishes the foundational types that the service and endpoint layers will use.

The license report groups packages by license type and includes a compliance flag per group based on a configurable policy. The policy defines which licenses are allowed, denied, or require review.

## Jira Metadata
- **Priority**: Major
- **Fix Versions**: RHTPA 1.5.0

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — Define `LicenseReport`, `LicenseGroup`, and `LicensePackageRef` structs with Serialize derives for JSON response. Define `LicensePolicy` and `LicensePolicyEntry` structs with Deserialize derives for policy file parsing.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to expose the new module.

## Implementation Notes
Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs`. All model structs should derive `Clone, Debug, Serialize` at minimum. The response struct should mirror this JSON shape:

```json
{
  "sbom_id": "uuid",
  "groups": [
    {
      "license": "MIT",
      "packages": [{ "name": "serde", "version": "1.0.0", "transitive": false }],
      "compliant": true
    }
  ],
  "summary": {
    "total_packages": 100,
    "compliant_count": 95,
    "non_compliant_count": 5,
    "policy_name": "default"
  }
}
```

The `LicensePolicy` struct should support loading from a JSON config file with this shape:

```json
{
  "name": "default",
  "allowed_licenses": ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause"],
  "denied_licenses": ["GPL-3.0", "AGPL-3.0"],
  "default_policy": "review"
}
```

Reuse `serde` and `serde_json` for serialization, consistent with existing entity definitions in `entity/src/package.rs` and `entity/src/package_license.rs`.

Per CONVENTIONS.md §Module Pattern: follow `model/ + service/ + endpoints/` structure for the license report domain types. Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's module file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Follow the same struct layout, derive macros, and documentation patterns
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — Reference for nested struct composition patterns
- `entity/src/package_license.rs` — Existing license data entity that the report will aggregate from

## Acceptance Criteria
- [ ] `LicenseReport` struct contains an `sbom_id`, a `Vec<LicenseGroup>`, and a `summary` field
- [ ] `LicenseGroup` struct contains `license` (String), `packages` (Vec<LicensePackageRef>), and `compliant` (bool)
- [ ] `LicensePackageRef` struct contains `name`, `version`, and `transitive` (bool) fields
- [ ] `LicensePolicy` struct supports deserialization from the policy JSON schema with `allowed_licenses`, `denied_licenses`, and `default_policy` fields
- [ ] All structs derive appropriate serde traits and compile without errors
- [ ] Model module is re-exported from `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Unit test: `LicenseReport` serializes to the expected JSON structure
- [ ] Unit test: `LicensePolicy` deserializes from a valid policy JSON string
- [ ] Unit test: `LicensePolicy` deserialization fails gracefully on invalid input (missing required fields)

## Dependencies
- Depends on: None

[sdlc-workflow] Description digest: sha256-md:fca685f1399537131e273f2dd223163e2eaa881e977685131ae53728a70220f5
