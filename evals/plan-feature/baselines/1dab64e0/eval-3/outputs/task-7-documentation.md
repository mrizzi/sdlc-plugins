## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Document the new SBOM comparison endpoint and comparison UI workflow. The Feature description (TC-9003) identifies this as "New Content" documentation impact:
- API consumers need endpoint reference for `GET /api/v2/sbom/compare`
- UI users need a guide for the comparison workflow (selecting SBOMs, reading diff sections, sharing comparison URLs, exporting results)

Documentation Considerations from TC-9003:
- Doc Impact: New Content
- User purpose: API consumers need endpoint reference; UI users need a guide for the comparison workflow
- Reference material: Existing SBOM detail page documentation, package/advisory data model docs

## Acceptance Criteria
- [ ] API endpoint documentation covers `GET /api/v2/sbom/compare` with request parameters, response shape, error codes, and example responses
- [ ] UI workflow documentation covers the comparison page layout, SBOM selection, diff section navigation, URL sharing, and export functionality
- [ ] Documentation is consistent with the implemented feature behavior
- [ ] Documentation references the comparison endpoint's performance characteristics (p95 < 1s for SBOMs with up to 2000 packages)

## Test Requirements
- [ ] Verify API endpoint documentation accurately describes the request parameters (`left`, `right` query params) and response structure
- [ ] Verify UI workflow documentation matches the implemented comparison page behavior
- [ ] Verify example API responses in the documentation match the actual endpoint response shape

## Dependencies
- Depends on: Task 2 — Add SBOM comparison models and diff service
- Depends on: Task 3 — Add SBOM comparison endpoint and integration tests
- Depends on: Task 4 — Add SBOM comparison API types, client function, and hook
- Depends on: Task 5 — Add SBOM comparison page with diff sections
- Depends on: Task 6 — Add compare action to SBOM list page
