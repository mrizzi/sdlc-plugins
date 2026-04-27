# Repository Impact Map — TC-9004: Add License Compliance Report Endpoint

## trustify-backend

### changes
- Add license policy configuration model and loader (JSON config file for allowed/denied licenses)
- Add license report model structs (`LicenseGroup`, `LicenseReport`) for the API response
- Add license report service that aggregates package-license data from existing tables, walks transitive dependencies, and evaluates compliance against the configured policy
- Add `GET /api/v2/sbom/{id}/license-report` endpoint that returns grouped license data with compliance flags
- Register the new endpoint route in the SBOM endpoints module and server route mounting
- Add integration tests for the license report endpoint covering compliant, non-compliant, transitive dependency, empty SBOM, and performance scenarios
- Add documentation for the license report endpoint and license policy configuration
