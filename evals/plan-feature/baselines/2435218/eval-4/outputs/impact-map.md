# Repository Impact Map — TC-9004: Add License Compliance Report Endpoint

## trustify-backend

### Changes

- Add license compliance report response model (`LicenseReportGroup`, `LicenseReport`) in the SBOM module's model directory
- Add license policy configuration model and loader to read a JSON-based policy file defining allowed/denied license lists
- Add license report service logic in the SBOM module's service directory that aggregates package-license data across the full dependency tree (including transitive dependencies), groups packages by license, and flags non-compliant licenses against the configured policy
- Add `GET /api/v2/sbom/{id}/license-report` endpoint in the SBOM module's endpoints directory
- Register the new endpoint route in the SBOM endpoints module and ensure it is mounted via server main
- Add a default license policy JSON configuration file to the repository
- Add integration tests for the license report endpoint covering compliant SBOMs, non-compliant SBOMs, transitive dependencies, and missing SBOM error cases
- Add API documentation for the new endpoint and license policy configuration
