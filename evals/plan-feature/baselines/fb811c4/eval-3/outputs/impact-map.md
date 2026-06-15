# Impact Map: TC-9003 SBOM Comparison View

## Workflow Mode

**feature-branch** -- The frontend comparison page requires a new backend diffing endpoint that does not yet exist. Neither side functions independently, making this a tightly coupled cross-repo feature requiring a shared feature branch.

trustify-backend:
  changes:
    - Add SbomComparison model structs (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange) in modules/fundamental/src/sbom/model/
    - Add comparison service method to SbomService that loads two SBOMs by ID, diffs their packages, advisories, and licenses, and returns SbomComparisonResult
    - Add GET /api/v2/sbom/compare endpoint with left/right query parameters in modules/fundamental/src/sbom/endpoints/
    - Add integration tests for the comparison endpoint in tests/api/sbom.rs

trustify-ui:
  changes:
    - Add SbomComparisonResult TypeScript interface and fetchSbomComparison() API client function in src/api/
    - Add useSbomComparison React Query hook in src/hooks/ and register /sbom/compare route in src/routes.tsx
    - Build SbomComparePage with PatternFly Select dropdowns for SBOM selection, ExpandableSection diff sections with Badge count indicators, composable Table for each diff category, EmptyState for initial load, Skeleton loading states, and Export Dropdown (per Figma design context)
