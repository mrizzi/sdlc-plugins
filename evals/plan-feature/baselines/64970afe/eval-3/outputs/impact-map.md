# Repository Impact Map — TC-9003: SBOM comparison view

## trustify-backend

changes:
  - Add SBOM comparison result model types (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange) in the sbom model module
  - Add comparison diff service that computes structured diffs between two SBOMs by querying existing package, advisory, and license data via SeaORM joins
  - Add GET /api/v2/sbom/compare?left={id1}&right={id2} endpoint with query parameter extraction and route registration
  - Add integration tests for the comparison endpoint covering added/removed packages, version changes, new/resolved vulnerabilities, and license changes

## trustify-ui

changes:
  - Add TypeScript interfaces for the SBOM comparison API response types in the API models layer
  - Add API client function for the comparison endpoint in the REST client layer
  - Add React Query hook (useSbomComparison) for fetching comparison data
  - Implement SBOM comparison page at /sbom/compare with header toolbar (SBOM selectors, Compare button, Export dropdown), six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes), empty state, and loading state — all using PatternFly 5 components per Figma design
  - Add route registration for /sbom/compare with lazy-loaded page component
  - Add checkbox selection and "Compare selected" button to the SBOM list page for triggering comparison navigation
  - Add unit tests (Vitest + RTL) and E2E tests (Playwright) for the comparison page, with MSW mock handlers for the comparison endpoint

## Workflow Mode

**Selected mode:** `feature-branch`

**Rationale:** Atomicity indicator #4 (Tightly coupled feature components) is present. The frontend comparison page (`/sbom/compare`) requires the new backend comparison endpoint (`GET /api/v2/sbom/compare`). Neither side functions independently — the frontend page would have no endpoint to call, and the backend endpoint has no consumer without the frontend. Merging either side alone to main would leave incomplete functionality.

**Interdependent tasks:**
- Frontend Task 6 (comparison page UI) depends on Backend Task 3 (comparison endpoint) — the page calls the endpoint directly
- Frontend Task 5 (API types and hook) depends on the backend response shape defined in Task 2 (model types)

The `workflow:feature-branch` label will be applied to the TC-9003 feature issue.

## Excluded requirements

None. All requirements from the Feature description (both MVP and non-MVP) can be decomposed into actionable tasks. The non-MVP "Export diff as JSON or CSV" requirement is included in the comparison page UI task with a non-MVP annotation.
