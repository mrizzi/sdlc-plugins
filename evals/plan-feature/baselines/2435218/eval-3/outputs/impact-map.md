# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

changes:
  - Add SBOM comparison diff response model structs (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange) in the sbom model module
  - Add comparison diffing logic in SbomService that fetches packages, advisories, and licenses for two SBOMs and computes a structured diff
  - Add GET /api/v2/sbom/compare endpoint with left/right query parameters that calls the diff service and returns the comparison result
  - Add integration tests for the comparison endpoint covering added/removed packages, version changes, vulnerability diffs, license changes, error cases (missing SBOM IDs, same SBOM), and performance with large package sets

## trustify-ui

changes:
  - Add TypeScript interfaces for the comparison API response shape (SbomComparisonResult and nested types) in the API models file
  - Add API client function compareSboms(leftId, rightId) in the REST client module
  - Add React Query hook useSbomComparison for the comparison endpoint
  - Create SbomComparePage component at /sbom/compare with header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes) following Figma design
  - Add route definition for /sbom/compare in the routes file
  - Add checkbox selection to SbomListPage and a "Compare selected" action that navigates to the comparison page with selected SBOM IDs as URL query params
  - Add unit tests (Vitest + RTL) and E2E tests (Playwright) for the comparison page covering empty state, loading state, diff rendering, URL-shareable comparisons, and large diff virtualization
