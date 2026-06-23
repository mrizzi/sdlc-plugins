# Task 5 — Document the license report endpoint and policy configuration

## Repository
trustify-backend

## Target Branch
main

## Description
Add documentation for the new license compliance report endpoint and the license policy configuration. This covers API usage, policy file format, and integration with CI/CD pipelines for automated compliance gating.

## Files to Modify
- `README.md` — add a section or reference to the license compliance report feature

## Files to Create
- `docs/license-compliance.md` — comprehensive documentation covering: endpoint usage (`GET /api/v2/sbom/{id}/license-report`), response schema, license policy configuration file format, how to customize the policy, and examples for CI/CD integration

## Implementation Notes
- Follow the documentation style established in `README.md` for structure and tone.
- Include a complete example of the policy JSON configuration file with annotations explaining each field.
- Include a curl example showing the endpoint request and a sample response.
- Include a CI/CD pipeline snippet demonstrating the automated compliance gate use case (UC-2 from the feature description).
- Per constraints doc section 2 (Commit Rules): use Conventional Commits format with `docs` type, reference TC-9004 in the footer, and include `--trailer="Assisted-by: Claude Code"`.

## Documentation Updates
- `README.md` — add reference to the license compliance feature and link to the detailed documentation
- `docs/license-compliance.md` — new file with full endpoint and configuration documentation

## Acceptance Criteria
- [ ] Documentation covers the endpoint path, HTTP method, request parameters, and response schema
- [ ] Documentation includes a complete license policy configuration example
- [ ] Documentation includes a curl command example with sample response
- [ ] Documentation explains how to use the endpoint in a CI/CD pipeline for automated compliance gating
- [ ] README.md references the new documentation

## Test Requirements
- [ ] Documentation renders correctly in Markdown viewers
- [ ] All example commands and JSON snippets are syntactically valid

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint

[sdlc-workflow] Description digest: sha256-md:d72746cf99e05f1df31e9ad1d5e4afddc1a48888584ab1da2563cd5def9059e9
