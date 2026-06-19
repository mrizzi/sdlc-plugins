## Repository
trustify-backend

## Target Branch
main

## Description
Document the license compliance report endpoint and license policy configuration. This covers API usage (request/response format, status codes), policy file schema and customization, and integration with CI/CD pipelines for automated compliance gating.

## Files to Modify
- `README.md` — Add a section documenting the license report endpoint and license policy configuration

## Documentation Updates
- `README.md` — Add "License Compliance Report" section covering: endpoint URL and method, request parameters (SBOM ID), response JSON schema, license policy configuration file format and customization instructions, example curl commands, CI/CD integration guidance for automated compliance gating

## Implementation Notes
- Reference the response shape: `{ groups: [{ license: string, packages: [{ name: string, version: string }], compliant: bool }] }`.
- Document the `license-policy.json` configuration file: its location, schema (`approved_licenses`, `denied_licenses`, `default_policy`), and how to customize it for different organizational compliance requirements.
- Include an example of using the endpoint in a CI/CD pipeline to fail builds on non-compliant licenses (checking for `compliant: false` in the response).
- Document the supported HTTP status codes: 200 (success), 404 (SBOM not found).

## Acceptance Criteria
- [ ] README documents the `GET /api/v2/sbom/{id}/license-report` endpoint with request/response details
- [ ] README documents the `license-policy.json` configuration format and customization
- [ ] README includes at least one example curl command showing endpoint usage
- [ ] README describes how to use the endpoint for CI/CD compliance gating

## Test Requirements
- [ ] Manual review: documentation accurately reflects the implemented API and configuration

## Dependencies
- Depends on: Task 3 — Add license report endpoint and register route
