# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

changes:
  - Add SBOM comparison diff model types (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)
  - Add SBOM comparison service method to SbomService that computes structured diff between two SBOMs using existing package, advisory, and license data
  - Add GET /api/v2/sbom/compare endpoint with left and right query parameters
  - Add integration tests for the comparison endpoint covering added/removed packages, version changes, vulnerability changes, and license changes

## trustify-ui

changes:
  - Add TypeScript interfaces for the SBOM comparison API response types
  - Add API client function fetchSbomComparison() in rest.ts
  - Add React Query hook useSbomComparison for the comparison endpoint
  - Add SbomComparePage with SBOM selectors, Compare button, and diff section layout using PatternFly ExpandableSection, Table, Badge, Select, and EmptyState components
  - Add route definition for /sbom/compare in routes.tsx
  - Add unit tests for SbomComparePage with MSW mock handlers
  - Add URL-shareable comparison state using query parameters (left, right)

## Workflow Mode

**Selected mode: `feature-branch`**

**Rationale:** Atomicity indicator #4 (Tightly coupled feature components) is present — the frontend comparison page requires the new backend `GET /api/v2/sbom/compare` endpoint that does not yet exist. Merging the frontend page to `main` without the backend endpoint would result in a broken comparison page. Additionally, atomicity indicator #2 (Breaking API changes) applies — the frontend depends on a specific API response shape that must be defined and available before the frontend can function.

**Interdependent tasks:** All frontend tasks (API client, hook, comparison page, routing) depend on the backend comparison endpoint being available. The backend model, service, and endpoint tasks are prerequisites for the frontend implementation tasks.
