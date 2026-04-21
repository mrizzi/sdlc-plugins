# Repository Impact Map — TC-9003: SBOM Comparison View

trustify-backend:
  changes:
    - Add SbomComparisonResult model with diff categories (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
    - Add comparison service method in SbomService to compute diff between two SBOMs by loading their packages, advisories, and licenses
    - Add GET /api/v2/sbom/compare endpoint accepting left and right query parameters, returning structured diff
    - Add integration tests for the comparison endpoint covering normal diff, identical SBOMs, and not-found cases

trustify-ui:
  changes:
    - Add TypeScript interfaces for the comparison API response shape
    - Add API client function to call the comparison endpoint
    - Add React Query hook for the comparison query
    - Add SbomComparePage with header toolbar (two SBOM selectors, Compare button, Export dropdown) per Figma
    - Add collapsible diff section components (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes) per Figma
    - Add route definition for /sbom/compare
    - Add "Compare selected" action to SbomListPage for selecting two SBOMs
    - Add unit and E2E tests for the comparison page
