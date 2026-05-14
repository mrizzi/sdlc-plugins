# Task 6 — Document license report endpoint and policy configuration

## Repository
trustify-backend

## Target Branch
main

## Description
Update project documentation to cover the new license compliance report endpoint and the license policy configuration. This includes documenting the API endpoint, request/response format, and how to customize the license policy JSON file for different organizational compliance requirements.

## Files to Modify
- `README.md` — add a section documenting the license report endpoint (`GET /api/v2/sbom/{id}/license-report`), its response format, and the license policy configuration

## Implementation Notes
- Review the existing `README.md` structure and add documentation in a style consistent with existing endpoint documentation.
- Document the following:
  1. **Endpoint**: `GET /api/v2/sbom/{id}/license-report` — purpose, path parameters, response shape
  2. **Response format**: describe the `LicenseReport` JSON structure including `groups`, `license`, `packages`, `compliant` fields
  3. **License policy configuration**: explain the `config/license-policy.json` file format, how to add allowed/denied licenses, and the `default_policy` behavior
  4. **Use cases**: brief examples for compliance officers (manual review) and CI/CD pipelines (automated compliance gate)
- Per constraints doc section 5.1: changes must be scoped to the files listed above.
- Per constraints doc section 4.9: this task covers documentation updates for the new public API and configuration.

## Acceptance Criteria
- [ ] `README.md` documents the `GET /api/v2/sbom/{id}/license-report` endpoint with path, method, and response format
- [ ] `README.md` explains the license policy configuration file format and customization
- [ ] Documentation includes at least one example response JSON snippet
- [ ] Documentation is consistent in style with existing README content

## Test Requirements
- [ ] Verify documentation renders correctly in Markdown (no broken formatting)
- [ ] Verify all referenced file paths (`config/license-policy.json`) are accurate

## Dependencies
- Depends on: Task 4 — Add GET /api/v2/sbom/{id}/license-report endpoint
