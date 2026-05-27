# Repository Impact Map — TC-9003: SBOM Comparison View

## Workflow Mode

**Selected mode:** `feature-branch`

**Rationale:** This feature exhibits two atomicity indicators:

1. **Tightly coupled feature components (indicator #4):** The frontend comparison page (`/sbom/compare`) requires the new backend `GET /api/v2/sbom/compare` endpoint. Neither side functions independently — the frontend page cannot render without the backend diff response, and the backend endpoint has no consumer without the frontend UI.
2. **Breaking API changes (indicator #2):** The frontend tasks depend on a backend API endpoint that does not yet exist on `main`. Merging the frontend first would leave the comparison page calling a non-existent endpoint; merging the backend first is safe but leaves dead code until the frontend lands.

**Interdependent tasks:** All frontend tasks (API types, hook, comparison page, SBOM list selection) depend on the backend tasks (comparison model/service, comparison endpoint) being available on the feature branch.

---

## Impact Map

```
trustify-backend:
  changes:
    - Add SBOM comparison diff model structs (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)
    - Add SbomService::compare method that computes the structured diff between two SBOMs using existing package, advisory, and license data
    - Add GET /api/v2/sbom/compare endpoint with left/right query parameters that returns the comparison result
    - Add integration tests for the comparison endpoint

trustify-ui:
  changes:
    - Add TypeScript interfaces for the SBOM comparison API response types
    - Add API client function compareSboms(leftId, rightId) in rest.ts
    - Add React Query hook useSbomComparison for the comparison endpoint
    - Add SbomComparePage with header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections using PatternFly ExpandableSection, Badge, Table, Select, EmptyState, and Skeleton components
    - Add route definition for /sbom/compare in routes.tsx
    - Add SBOM selection checkboxes and "Compare selected" button to SbomListPage
    - Add unit tests for comparison page components and E2E test for comparison workflow
```
