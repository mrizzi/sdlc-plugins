# Task 5 — Document license report endpoint and policy configuration

## Repository
trustify-backend

## Description
Add documentation for the new license compliance report endpoint and the license policy configuration. This covers API usage documentation for compliance officers and CI/CD integration, as well as configuration reference for the license policy JSON file. This is a cross-cutting documentation task that consolidates documentation needs from the implementation tasks.

## Files to Modify
- `README.md` — Add a section describing the license compliance report feature, including the endpoint path, usage examples, and a link to the policy configuration reference.

## Files to Create
- `docs/license-policy.md` — Configuration reference for the `license-policy.json` file. Documents the schema (allowed, denied, default_policy fields), SPDX license identifier format, and examples of common policy configurations (permissive-only, copyleft-allowed, custom).

## Documentation Updates
- `README.md` — Add a "License Compliance Report" section under the API documentation describing: endpoint URL (`GET /api/v2/sbom/{id}/license-report`), response shape, usage examples with curl, and CI/CD integration guidance (how to use the endpoint as an automated compliance gate).
- `docs/license-policy.md` — New file: full configuration reference for the license policy JSON file.

## Implementation Notes
- Review existing README.md structure to determine the appropriate location for the new section.
- Include a curl example showing a typical request and response for the license report endpoint.
- Include a CI/CD integration example showing how to call the endpoint and check for non-compliant licenses in a pipeline script.
- Document the JSON schema for `license-policy.json` with field descriptions, types, and default values.
- Include a table of common SPDX license identifiers for reference (MIT, Apache-2.0, GPL-2.0, GPL-3.0, AGPL-3.0, BSD-2-Clause, BSD-3-Clause, LGPL-2.1, MPL-2.0).

## Acceptance Criteria
- [ ] README.md contains a section describing the license report endpoint with usage examples
- [ ] `docs/license-policy.md` documents the complete policy configuration schema
- [ ] Documentation includes a CI/CD integration example
- [ ] SPDX license identifier reference is included
- [ ] Configuration examples cover at least three policy scenarios (permissive-only, copyleft-allowed, custom)

## Test Requirements
- [ ] Documentation review: verify all file paths and endpoint URLs in the documentation are accurate
- [ ] Documentation review: verify curl examples use the correct request format and show realistic response shapes

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint
