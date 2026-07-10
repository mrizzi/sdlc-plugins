## Repository
trustify-backend

## Target Branch
main

## Description
Document the new license compliance report endpoint (`GET /api/v2/sbom/{id}/license-report`)
and the license policy configuration. The Feature's Documentation Considerations indicate
"New Content" is needed with doc impact type: New Content.

**Doc impact type:** New Content

**Details from Documentation Considerations:**
- User purpose: Compliance officers need to understand how to configure policies and
  interpret reports
- Reference material: SPDX license list, existing package data model documentation

This task covers:
- Documenting the endpoint's request/response contract
- Documenting the license policy JSON configuration format and how to customize it
- Providing examples of API usage for compliance workflows (manual and CI/CD integration)

**Feature reference:** TC-9004

## Acceptance Criteria
- [ ] Endpoint documentation covers the request path, parameters, and response schema
- [ ] License policy configuration format is documented with examples
- [ ] Documentation explains how to customize the denied license list
- [ ] Usage examples cover both manual compliance review and CI/CD pipeline integration
- [ ] Documentation is accurate and consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify the documented request/response examples match the actual API behavior
- [ ] Verify the documented policy configuration format matches the implemented schema
- [ ] Verify all code examples in the documentation are syntactically correct

## Dependencies
- Depends on: Task 1 — Add license report model types
- Depends on: Task 2 — Add license policy configuration
- Depends on: Task 3 — Add license report service
- Depends on: Task 4 — Add license report endpoint
- Depends on: Task 5 — Add license report integration tests
