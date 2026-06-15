# Repository Impact Map — TC-9003: SBOM Comparison View

## Workflow Mode

**Mode:** `feature-branch`

**Rationale:** The frontend comparison page requires a new backend endpoint (`GET /api/v2/sbom/compare`) that does not yet exist. Neither side functions independently — the frontend cannot render comparison results without the backend diff endpoint, and the backend endpoint provides no user value without the frontend UI. This matches atomicity indicator #4 (tightly coupled feature components). All intermediate tasks target the `TC-9003` feature branch; bookend tasks target `main`.

## Impact Map

```
trustify-backend:
  changes:
    - Add SBOM comparison diff model structs (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)
    - Add SBOM comparison service method to compute structured diff between two SBOMs using existing package, advisory, and license data
    - Add GET /api/v2/sbom/compare endpoint with left/right query parameters
    - Add integration tests for the comparison endpoint

trustify-ui:
  changes:
    - Add TypeScript interfaces for the SBOM comparison API response types
    - Add API client function to call GET /api/v2/sbom/compare
    - Add React Query hook for the comparison endpoint
    - Add SbomComparePage with SBOM selectors, diff sections, empty state, and loading state
    - Add route definition for /sbom/compare
    - Add MSW mock handlers and component tests for the comparison page
```
