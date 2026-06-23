# Task 6 — Document license compliance report endpoint and policy configuration

## Repository
trustify-backend

## Target Branch
main

## Description
Add documentation for the new license compliance report endpoint and the license policy configuration. This covers the API endpoint usage (request/response format), how to configure the license policy JSON file, and how to interpret the compliance report output. This documentation serves compliance officers who need to configure policies and CI/CD pipeline engineers who integrate the endpoint into automated workflows.

## Files to Modify
- `README.md` — Add a section describing the license compliance report feature, including the endpoint path, expected response format, and a link to the policy configuration documentation

## Files to Create
- `docs/license-compliance.md` — Comprehensive documentation covering: endpoint usage (`GET /api/v2/sbom/{id}/license-report`), response schema with example JSON, license policy configuration file format and schema, how to customize the policy for different organizational needs, and examples for CI/CD integration

## Implementation Notes
- Document the endpoint: `GET /api/v2/sbom/{id}/license-report`
  - Path parameters: `id` (SBOM identifier)
  - Response shape with example JSON
  - HTTP status codes: 200 (success), 404 (SBOM not found)
- Document the license policy configuration:
  - JSON schema for `config/default-license-policy.json`
  - Fields: `allowed_licenses`, `denied_licenses`, `default_policy`
  - How to customize the policy for different organizational needs
  - Reference to the SPDX license list for valid identifiers
- Document the CI/CD integration use case: how to call the endpoint and check for `compliant: false` to fail a build
- Include a curl example showing the endpoint request and a sample response
- Follow existing documentation patterns in the repository (check `README.md` style and any existing docs/ files)

## Documentation Updates
- `README.md` — Add reference to the license compliance feature and link to the detailed documentation
- `docs/license-compliance.md` — New file with full endpoint and configuration documentation

## Acceptance Criteria
- [ ] README.md includes a section about the license compliance report feature
- [ ] License policy configuration guide explains the JSON schema with examples
- [ ] CI/CD integration workflow is documented with a concrete example
- [ ] All documented endpoint paths and response shapes match the actual implementation

## Test Requirements
- [ ] Manual review: verify all documented paths and response shapes match the implemented endpoint
- [ ] Manual review: verify the license policy JSON examples are valid and parseable

## Dependencies
- Depends on: Task 4 — Add GET /api/v2/sbom/{id}/license-report endpoint

[sdlc-workflow] Description digest: sha256-md:28ace16fc1e4763786231fa0b897bd781273b2cacaae69046fd4cccd65db11aa