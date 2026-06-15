# Task 1: Define license compliance report model structs

## Repository

trustify-backend

## Target Branch

main

## Description

Define the response model structs for the license compliance report feature. The endpoint `GET /api/v2/sbom/{id}/license-report` will return a structured JSON response grouping packages by license type with a compliance flag per group. This task creates the data model layer that the service and endpoint layers will depend on.

The response structure is:

```json
{
  "groups": [
    {
      "license": "MIT",
      "packages": [
        { "name": "serde", "version": "1.0.197", "purl": "pkg:cargo/serde@1.0.197" }
      ],
      "compliant": true
    }
  ],
  "summary": {
    "total_packages": 42,
    "total_licenses": 5,
    "compliant_count": 4,
    "non_compliant_count": 1
  }
}
```

## Files to Create

- `modules/fundamental/src/sbom/model/license_report.rs` -- Contains `LicenseReport`, `LicenseGroup`, `LicensePackageRef`, and `LicenseReportSummary` structs, all deriving `Serialize` and `Deserialize`.

## Files to Modify

- `modules/fundamental/src/sbom/model/mod.rs` -- Add `pub mod license_report;` and re-export the new structs.

## Implementation Notes

- Follow the existing model pattern seen in `modules/fundamental/src/sbom/model/summary.rs` and `details.rs`: structs derive `Clone`, `Debug`, `Serialize`, `Deserialize`, and use `serde` attributes for field naming.
- `LicensePackageRef` should include `name: String`, `version: String`, and `purl: Option<String>` fields to reference packages without duplicating the full `PackageSummary`.
- `LicenseGroup` should include `license: String`, `packages: Vec<LicensePackageRef>`, and `compliant: bool`.
- `LicenseReport` should include `groups: Vec<LicenseGroup>` and `summary: LicenseReportSummary`.
- `LicenseReportSummary` should include `total_packages`, `total_licenses`, `compliant_count`, and `non_compliant_count` as `usize` fields.

## Acceptance Criteria

- [ ] `LicenseReport`, `LicenseGroup`, `LicensePackageRef`, and `LicenseReportSummary` structs are defined and publicly exported
- [ ] All structs derive `Serialize` and `Deserialize` for JSON serialization
- [ ] Structs are re-exported from the SBOM model module
- [ ] Code compiles without warnings (`cargo check`)

## Test Requirements

- No dedicated tests for this task. The structs will be validated through service-layer unit tests (Task 2) and integration tests (Task 4).

[Description digest: sha256-md:a3f1d8e2c4b90671f5e83ca92d01b6f748ea35c9d20f74a1b86e53c9f0124d87 would be posted as a comment]
