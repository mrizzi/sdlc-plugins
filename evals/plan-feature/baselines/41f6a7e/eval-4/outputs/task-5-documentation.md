# Task 5 — Document license report endpoint and policy configuration

## Repository
trustify-backend

## Target Branch
main

## Description
Add documentation for the new license compliance report endpoint and the license policy configuration. This covers API usage, response schema, policy file format, and configuration instructions for compliance teams and CI/CD integration.

## Files to Modify
- `README.md` — Add section describing the license compliance report feature, endpoint, and policy configuration

## Implementation Notes
- Inspect the existing `README.md` to understand the current documentation structure and style before adding content
- Documentation should cover:
  1. **Endpoint reference**: `GET /api/v2/sbom/{id}/license-report` with request/response examples
  2. **Response schema**: describe the LicenseReport JSON structure with field descriptions
  3. **License policy configuration**: explain the `config/license-policy.json` format, how to customize allowed/denied/review lists, and the default_policy behavior
  4. **CI/CD integration**: brief guide on using the endpoint as a compliance gate (check `compliant: false` in response groups)
  5. **SPDX license identifiers**: note that license identifiers follow the SPDX specification
- Per docs/constraints.md section 5.2: read existing documentation before modifying

## Documentation Updates
- `README.md` — Add new section covering the license report endpoint, response schema, policy configuration format, and CI/CD integration usage

## Acceptance Criteria
- [ ] README.md includes documentation for the license report endpoint with request/response examples
- [ ] License policy configuration format is documented with field descriptions
- [ ] CI/CD integration usage is described
- [ ] Documentation follows the existing style and tone of the README

## Test Requirements
- [ ] Verify all documented endpoint paths and response fields match the actual implementation
- [ ] Verify the example license-policy.json in the documentation matches the actual default config file

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint
