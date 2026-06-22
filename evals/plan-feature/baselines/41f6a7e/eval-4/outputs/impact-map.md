# Repository Impact Map — TC-9004: Add License Compliance Report Endpoint

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. This feature is additive within a single repository: it introduces a new endpoint and supporting service without modifying existing API contracts, database schemas, or cross-repo dependencies. Each task can be merged independently without leaving `main` in a broken state.

## Impact Map

```
trustify-backend:
  changes:
    - Add license policy configuration model (JSON config file for allowed/denied licenses)
    - Add LicenseReportService with logic to aggregate package licenses from existing sbom_package and package_license data, walk transitive dependencies, and group by license with policy compliance flags
    - Add GET /api/v2/sbom/{id}/license-report endpoint returning grouped license compliance report
    - Add integration tests for the license report endpoint covering compliant, non-compliant, and transitive dependency scenarios
    - Add documentation for the license report endpoint and policy configuration
```
