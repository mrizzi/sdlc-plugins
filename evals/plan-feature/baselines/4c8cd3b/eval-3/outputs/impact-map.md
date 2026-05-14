# Repository Impact Map — TC-9003: SBOM Comparison View

## Workflow Mode

**Selected mode:** `feature-branch`

**Rationale:** Atomicity indicators present:
- **Tightly coupled feature components:** The frontend comparison page (`/sbom/compare`) requires the new backend `GET /api/v2/sbom/compare` endpoint. Neither side functions independently — the frontend would call a non-existent endpoint if merged alone, and the backend endpoint has no consumer if merged alone.
- **Breaking API changes:** The frontend depends on a specific response shape from the new comparison endpoint. Partial delivery would leave the integration broken on `main`.

**Interdependent tasks:** All frontend tasks depend on the backend comparison endpoint task. The comparison page, React Query hook, and API client function all require the backend endpoint to exist.

---

## Impact Map

```
trustify-backend:
  changes:
    - Add SBOM comparison diff model structs (SbomComparisonResult, PackageDiff, VulnerabilityDiff, LicenseDiff, VersionChange)
    - Add SBOM comparison service function that computes the diff between two SBOMs
    - Add GET /api/v2/sbom/compare endpoint with left/right query parameters
    - Add integration tests for the comparison endpoint

trustify-ui:
  changes:
    - Add TypeScript interfaces for the comparison API response types
    - Add API client function for the comparison endpoint
    - Add React Query hook for SBOM comparison data fetching
    - Add SbomComparePage with header toolbar (SBOM selectors, Compare button, Export dropdown)
    - Add diff section components (AddedPackages, RemovedPackages, VersionChanges, NewVulnerabilities, ResolvedVulnerabilities, LicenseChanges)
    - Add route definition for /sbom/compare
    - Add checkbox selection to SbomListPage for multi-select and "Compare selected" action
    - Add unit tests and MSW mock handlers for the comparison page
```
