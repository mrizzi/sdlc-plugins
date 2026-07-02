## additional_fields
```
{ "labels": ["ai-generated-jira"], "priority": {"name": "Critical"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }
```

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Document the SBOM comparison feature covering both the backend API endpoint and the frontend comparison UI. The Feature description identifies this as "New Content" documentation:

- **Doc impact type**: New Content
- **User purpose**: API consumers need endpoint reference for the comparison endpoint; UI users need a guide for the comparison workflow
- **Reference material**: Existing SBOM detail page documentation, package/advisory data model docs

The documentation should cover:
1. The `GET /api/v2/sbom/compare` endpoint — request parameters, response shape, error codes, and performance characteristics
2. The comparison UI workflow — how to select SBOMs, interpret diff sections, and share comparison URLs
3. Integration with the SBOM list page — how to use checkbox selection for comparison

## Acceptance Criteria
- [ ] API endpoint documentation covers request parameters (`left`, `right`), response shape (all six diff categories), and error responses (400, 404)
- [ ] UI workflow documentation describes the comparison page layout, SBOM selector usage, and diff section interpretation
- [ ] URL-shareable comparison is documented with example URLs
- [ ] Documentation references the existing SBOM detail page documentation for context
- [ ] Performance characteristics are noted (p95 < 1s for SBOMs with up to 2000 packages)

## Test Requirements
- [ ] Verify documentation accurately reflects the implemented endpoint behavior
- [ ] Verify UI workflow description matches the actual comparison page layout and interactions
- [ ] Verify example URLs and API calls in the documentation are correct and functional

## Dependencies
- Depends on: Task 4 — Backend comparison endpoint (endpoint must be implemented before documenting)
- Depends on: Task 6 — Frontend comparison page (UI must be implemented before documenting the workflow)
- Depends on: Task 7 — Frontend SBOM list and tests (list page changes must be implemented before documenting)
