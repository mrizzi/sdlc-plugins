# Repository Impact Map — TC-9003: SBOM Comparison View

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. The backend endpoint (`GET /api/v2/sbom/compare`) is purely additive and does not break existing functionality — it can be merged to `main` independently. The frontend comparison page is a new route (`/sbom/compare`) that adds a new page without modifying existing pages. Cross-repo dependency is sequential (frontend depends on backend being deployed), not atomic (both can land independently without breaking `main`). No coordinated schema migrations, breaking API changes, or cross-cutting refactors are involved.

## Impact Map

```
trustify-backend:
  changes:
    - Add SBOM comparison diff model structs (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)
    - Add SbomService comparison method to compute on-the-fly diff between two SBOMs using existing package, advisory, and license data
    - Add GET /api/v2/sbom/compare endpoint with left/right query parameters
    - Add integration tests for the comparison endpoint covering added/removed packages, version changes, vulnerability diffs, and license changes

trustify-ui:
  changes:
    - Add TypeScript interfaces for the SBOM comparison API response types
    - Add API client function for the comparison endpoint (fetchSbomComparison)
    - Add React Query hook for SBOM comparison (useSbomComparison)
    - Add SbomComparePage component with header toolbar (SBOM selectors, Compare button, Export dropdown)
    - Add diff section components (AddedPackages, RemovedPackages, VersionChanges, NewVulnerabilities, ResolvedVulnerabilities, LicenseChanges) using PatternFly ExpandableSection and Table
    - Add empty state and loading state for the comparison page
    - Add route definition for /sbom/compare
    - Add checkbox selection to SbomListPage with "Compare selected" action
    - Add unit tests and MSW mock handlers for the comparison page
```
