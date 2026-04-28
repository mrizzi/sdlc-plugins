# Repository Impact Map — TC-9003: SBOM Comparison View

```
trustify-backend:
  changes:
    - Add SbomComparisonResult response model with diff categories (added/removed packages, version changes, new/resolved vulnerabilities, license changes)
    - Add comparison service method to SbomService that computes a structured diff between two SBOMs on-the-fly
    - Add GET /api/v2/sbom/compare endpoint with left/right query parameters
    - Add integration tests for the comparison endpoint covering normal diffs, empty diffs, and error cases

trustify-ui:
  changes:
    - Add TypeScript interfaces for the comparison API response shape
    - Add API client function for the comparison endpoint and React Query hook
    - Add SbomComparePage with header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections
    - Add diff section components (AddedPackages, RemovedPackages, VersionChanges, NewVulnerabilities, ResolvedVulnerabilities, LicenseChanges) using PatternFly ExpandableSection and Table
    - Add route definition for /sbom/compare with URL query parameter support
    - Add checkbox selection to SbomListPage with "Compare selected" action
    - Add unit tests for comparison page and components, MSW handlers for mock data, and E2E test for comparison workflow
```
