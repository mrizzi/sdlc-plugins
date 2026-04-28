# Repository Impact Map -- TC-9003: SBOM Comparison View

```
trustify-backend:
  changes:
    - Add SbomComparisonResult response model with diff categories (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
    - Add comparison diff method to SbomService that computes a structured diff between two SBOMs on-the-fly using existing package, advisory, and license data
    - Add GET /api/v2/sbom/compare endpoint with left and right query parameters, returning the SbomComparisonResult
    - Add integration tests for the comparison endpoint covering normal diffs, empty diffs, invalid IDs, and same-SBOM comparisons

trustify-ui:
  changes:
    - Add TypeScript interfaces for the comparison API response and add API client function and React Query hook for the comparison endpoint
    - Add SbomComparePage with header toolbar (SBOM selectors, Compare button, Export dropdown) and vertically stacked collapsible diff sections per Figma design
    - Add diff section components (AddedPackagesSection, RemovedPackagesSection, VersionChangesSection, NewVulnerabilitiesSection, ResolvedVulnerabilitiesSection, LicenseChangesSection) using PatternFly ExpandableSection, Badge, and Table with virtualized rows for large diffs
    - Add route definition for /sbom/compare with URL query parameter support for left and right SBOM IDs
    - Add checkbox selection to SbomListPage with "Compare selected" button that navigates to comparison page with selected IDs
    - Add unit tests with MSW handlers and mock fixtures, and E2E test for the full comparison workflow
```
