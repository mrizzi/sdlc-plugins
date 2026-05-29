# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

changes:
  - Add SBOM comparison diff model types (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)
  - Add SBOM comparison service method to compute structured diff between two SBOMs using existing package, advisory, and license data
  - Add GET /api/v2/sbom/compare endpoint with left/right query parameters
  - Add integration tests for the comparison endpoint

## trustify-ui

changes:
  - Add TypeScript interfaces for the SBOM comparison API response types
  - Add API client function to call GET /api/v2/sbom/compare
  - Add React Query hook for the comparison endpoint
  - Add SBOM comparison page with side-by-side diff sections using PatternFly components (Select, ExpandableSection, Badge, Table, EmptyState)
  - Add route for /sbom/compare with URL query parameter support
  - Add checkbox selection to SBOM list page and "Compare selected" button
  - Add tests for comparison page and hook

## Workflow Mode

**Mode:** `feature-branch`

**Rationale:** Atomicity indicator #4 (tightly coupled feature components) is present. The frontend comparison page requires the new backend `GET /api/v2/sbom/compare` endpoint that does not yet exist. Merging the frontend without the backend would result in a broken comparison page. Merging the backend endpoint alone is harmless but provides no user value without the frontend. Additionally, indicator #2 (breaking API changes) applies: the frontend depends on a specific response shape from a new backend endpoint.

**Interdependent tasks:** All frontend tasks (API types, hook, comparison page, SBOM list page modifications) depend on the backend comparison endpoint task. The feature must ship atomically via the TC-9003 feature branch.
