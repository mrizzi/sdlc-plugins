## Repository
trustify-backend

## Target Branch
main

## Description
Document the new `GET /api/v2/sbom/{id}/license-report` endpoint and the license policy configuration. This documentation task covers the endpoint path, path parameters, response schema, status codes, license policy configuration format, and usage examples for both basic license report generation and the CI/CD automated compliance gate use case.

This task addresses the documentation signals from the Feature's Documentation Considerations section:
- **Doc Impact**: New Content
- **User purpose**: Compliance officers need to understand how to configure policies and interpret reports
- **Reference material**: SPDX license list, existing package data model documentation

additional_fields: { "labels": ["ai-generated-jira"], "priority": "Major", "fixVersions": "RHTPA 1.5.0" }

## Acceptance Criteria
- [ ] REST API reference includes the `GET /api/v2/sbom/{id}/license-report` endpoint
- [ ] Documentation covers: endpoint path, path parameter (SBOM ID), response schema
- [ ] Response schema is documented: `{ "groups": [{ "license": "MIT", "packages": [{ "name": "...", "version": "...", "transitive": false }], "compliant": true }] }`
- [ ] Status codes 200 (success) and 404 (SBOM not found) are documented
- [ ] License policy configuration format is documented with examples of allowed/denied lists
- [ ] Documentation explains how to customize the license policy for organization-specific requirements
- [ ] At least one usage example is provided for both manual report review and CI/CD pipeline integration

## Test Requirements
- [ ] Documentation renders correctly and all code examples are syntactically valid
- [ ] Endpoint path and response shape match the actual implementation
- [ ] License policy configuration examples are valid JSON

## Dependencies
- Depends on: Task 3 -- Implement license-report REST endpoint
