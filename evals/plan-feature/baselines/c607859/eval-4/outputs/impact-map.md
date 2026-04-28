# Repository Impact Map -- TC-9004: Add License Compliance Report Endpoint

## trustify-backend

### changes

- Add license policy configuration model: define a `LicensePolicy` struct that loads a configurable JSON policy file listing allowed and denied SPDX license identifiers
- Add license report response models: create `LicenseReportGroup` and `LicenseReport` structs representing packages grouped by license type with per-group compliance flags
- Add license report service: implement a `LicenseReportService` that aggregates license data from existing `package_license` and `sbom_package` entities, walks transitive dependencies via the SBOM package graph, groups packages by license, and evaluates each group against the configured license policy
- Add license report endpoint: register `GET /api/v2/sbom/{id}/license-report` in the SBOM endpoints module, invoking the license report service and returning the structured compliance report
- Add integration tests: create endpoint-level integration tests covering compliant SBOMs, non-compliant SBOMs, transitive dependency inclusion, missing SBOM (404), and performance for large package sets
- Add default license policy configuration file: create a default `license-policy.json` with a starter set of allowed and denied license categories
