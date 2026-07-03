## Repository
trustify-backend

## Target Branch
main

## Description
Document the new SBOM comparison endpoint and comparison UI workflow. The Feature description's Documentation Considerations section indicates "New Content" is needed: document the comparison endpoint for API consumers (endpoint path, parameters, response schema, status codes) and the comparison UI workflow for end users (selecting SBOMs, viewing diffs, sharing comparison URLs). Reference the existing SBOM detail page documentation and package/advisory data model docs as context.

Doc impact type: New Content.
Details: API consumers need endpoint reference; UI users need a guide for the comparison workflow. Reference material includes existing SBOM detail page documentation and package/advisory data model docs.

additional_fields: { "labels": ["ai-generated-jira"], "priority": "Critical", "fixVersions": "RHTPA 1.5.0" }

## Acceptance Criteria
- [ ] API reference documentation includes the `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint
- [ ] Documentation covers: endpoint path, query parameters (left, right as SBOM UUIDs), response schema with all six diff categories
- [ ] Status codes 200 (success), 400 (missing parameters), and 404 (SBOM not found) are documented
- [ ] Response JSON shape is documented with field descriptions for each diff category (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
- [ ] At least one usage example is provided showing a comparison API call and response
- [ ] Comparison UI workflow is documented for end users: selecting SBOMs from list page, viewing diff sections, sharing comparison URL

## Test Requirements
- [ ] Documentation renders correctly and all code examples are syntactically valid
- [ ] Endpoint path, parameters, and response shape match the actual implementation
- [ ] UI workflow documentation accurately reflects the comparison page behavior

## Dependencies
- Depends on: Task 2 -- Implement SBOM comparison REST endpoint
- Depends on: Task 5 -- Create SBOM comparison page
