# Task 5 — Document license report endpoint and policy configuration

## Repository
trustify-backend

## Description
Add documentation for the new license compliance report feature covering the REST endpoint usage, response schema, license policy configuration format, and CI/CD integration for automated compliance gates. This is a cross-cutting documentation task that spans the work done in Tasks 1-4.

## Files to Modify
- `README.md` — Add a section on the license compliance report feature, referencing the endpoint and policy configuration

## Files to Create
- `docs/license-compliance.md` — Comprehensive documentation covering: endpoint path and method, request/response examples, license policy JSON schema and configuration guide, compliance flag semantics, CI/CD pipeline integration example

## Implementation Notes
- Reference the SPDX license list for license identifier conventions
- Include a complete example of the `license-policy.json` configuration file showing allowed, denied, and review-required license lists
- Include a sample `curl` command demonstrating how to call the endpoint
- Include a sample response body showing the grouped license data structure with both compliant and non-compliant groups
- Document the CI/CD integration use case (UC-2): show how to use the endpoint in a pipeline to fail builds with non-compliant licenses
- Per constraints doc section 4.9: this task covers documentation updates for the new public API and configuration introduced by the feature

## Acceptance Criteria
- [ ] License report endpoint is documented with path, method, and response schema
- [ ] License policy JSON configuration format is fully documented with examples
- [ ] CI/CD pipeline integration workflow is documented
- [ ] Sample request and response are provided
- [ ] README.md references the new documentation

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint
