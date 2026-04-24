# Repository Impact Map — TC-9004: Add License Compliance Report Endpoint

## trustify-backend

### changes

- Add license policy configuration model: define a `LicensePolicy` struct that loads a JSON config file listing allowed and denied license identifiers
- Add license report model: create `LicenseReportGroup` and `LicenseReport` response structs representing packages grouped by license with compliance flags
- Add license report service: implement `LicenseReportService` that aggregates license data from existing `package_license` and `sbom_package` entities, walks transitive dependencies, groups packages by license, and evaluates each group against the configured license policy
- Add license report endpoint: register `GET /api/v2/sbom/{id}/license-report` in the SBOM endpoints module, calling the license report service and returning the structured report
- Add integration tests: create tests for the license report endpoint covering compliant SBOMs, non-compliant SBOMs, transitive dependency inclusion, missing SBOM (404), and performance with large package sets
- Add default license policy configuration file: create a default `license-policy.json` at the repository root or config directory with a starter set of compliant/non-compliant license categories
