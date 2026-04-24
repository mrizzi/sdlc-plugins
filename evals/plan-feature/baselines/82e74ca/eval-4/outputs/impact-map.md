# Repository Impact Map — TC-9004: Add License Compliance Report Endpoint

## trustify-backend

### changes:
- Add license policy configuration file (`license-policy.json`) defining compliant and non-compliant license categories
- Create `license_report` module under `modules/fundamental/src/` following the existing `model/ + service/ + endpoints/` module pattern
- Implement `LicenseReportService` to aggregate package-license data from existing tables, walk transitive dependencies, and flag non-compliant licenses against the configured policy
- Implement `GET /api/v2/sbom/{id}/license-report` endpoint returning packages grouped by license type with compliance flags
- Add license report model structs (`LicenseGroup`, `LicenseReport`) for the API response shape
- Add integration tests for the license report endpoint in `tests/api/`
- Document the new endpoint and license policy configuration
