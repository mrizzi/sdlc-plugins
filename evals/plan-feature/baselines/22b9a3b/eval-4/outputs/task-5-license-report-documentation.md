## Repository
trustify-backend

## Description
Document the new license compliance report endpoint and the license policy configuration. This is a dedicated documentation task covering the cross-cutting documentation needs of the license report feature, including API usage, policy configuration, and CI/CD integration guidance.

## Files to Modify
- `README.md` — Add a section describing the license compliance report feature, linking to detailed documentation

## Files to Create
- `docs/license-compliance.md` — Comprehensive documentation covering: endpoint usage (`GET /api/v2/sbom/{id}/license-report`), response schema, license policy configuration (format of `license-policy.json`, how to customize allowed/denied lists), CI/CD integration examples (using the endpoint as a compliance gate in pipelines)

## Implementation Notes
- Review the existing README.md to understand the documentation style and structure before adding new content
- The documentation should cover three audiences: compliance officers (how to read the report), DevOps engineers (how to integrate into CI/CD pipelines), and administrators (how to configure the license policy)
- Document the response schema with an example JSON response showing the `groups` array with `license`, `packages`, and `compliant` fields
- Document the license policy configuration file format with examples of common policies (e.g., permissive-only, deny-GPL, custom allow/deny lists)
- Include an example of using the endpoint as a CI/CD compliance gate (curl command + jq to check for non-compliant groups)
- Per constraints doc section 4.9: this task covers documentation updates for the new public API and configuration

## Acceptance Criteria
- [ ] README.md references the license compliance report feature with a link to detailed documentation
- [ ] docs/license-compliance.md documents the endpoint path, HTTP method, and response schema
- [ ] docs/license-compliance.md documents the license policy configuration file format with examples
- [ ] docs/license-compliance.md includes a CI/CD integration example
- [ ] Documentation is clear enough for a user unfamiliar with the feature to configure a policy and use the endpoint

## Test Requirements
- [ ] Verify all documented endpoint paths match the actual implementation
- [ ] Verify the documented response schema example matches the actual LicenseReport struct serialization

## Dependencies
- Depends on: Task 3 — License report API endpoint
