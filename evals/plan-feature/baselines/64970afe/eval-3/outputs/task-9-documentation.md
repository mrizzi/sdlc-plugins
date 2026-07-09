## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Document the new SBOM comparison endpoint and the comparison UI workflow. The feature adds:
- A new backend API endpoint: `GET /api/v2/sbom/compare?left={id1}&right={id2}`
- A new frontend comparison page at `/sbom/compare`

**Doc impact type:** New Content

The documentation should cover:
- API endpoint reference for the comparison endpoint (path, HTTP method, query parameters, response shape with all six diff categories)
- UI workflow guide for the comparison page (selecting SBOMs, reading diff sections, sharing comparison URLs)
- Reference material: existing SBOM detail page documentation, package/advisory data model docs

**User purpose:**
- API consumers need endpoint reference documentation
- UI users need a guide for the comparison workflow

## Acceptance Criteria
- [ ] API documentation covers the `GET /api/v2/sbom/compare` endpoint with request parameters and response schema
- [ ] API documentation includes example request and response JSON
- [ ] UI documentation covers the comparison workflow (selecting SBOMs, triggering comparison, navigating diff sections)
- [ ] UI documentation covers URL shareability (how to share comparison links)
- [ ] Documentation is consistent with the implemented feature behavior
- [ ] Documentation references the six diff categories: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes

## Test Requirements
- [ ] Verify all API endpoint documentation matches the actual endpoint behavior (path, params, response shape)
- [ ] Verify UI workflow documentation matches the actual page behavior
- [ ] Verify documentation is complete and covers both API and UI aspects of the feature

## Dependencies
- Depends on: Task 2 — Add SBOM comparison model types and diff service
- Depends on: Task 3 — Add SBOM comparison REST endpoint
- Depends on: Task 6 — Implement SBOM comparison page with diff sections
- Depends on: Task 7 — Add route registration and SBOM list page compare trigger
