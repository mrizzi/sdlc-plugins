# Repository Impact Map — TC-9003: SBOM Comparison View

## Workflow Mode

**Mode:** `feature-branch`

**Rationale:** Atomicity indicator present — tightly coupled feature components. The frontend comparison page (`/sbom/compare`) requires the new backend endpoint `GET /api/v2/sbom/compare` which does not yet exist. Merging the frontend without the backend would result in a broken page calling a non-existent endpoint. Merging the backend without the frontend delivers no user-visible value but is not broken. Both sides must land together for a functional feature.

**Interdependent tasks:** Backend comparison endpoint (service + endpoint tasks) and frontend comparison page are tightly coupled — the frontend cannot function without the backend endpoint.

---

```
trustify-backend:
  changes:
    - Add SBOM comparison diff model types (SbomComparisonResult, PackageDiff, VersionChange, VulnerabilityDiff, LicenseChange)
    - Implement SBOM comparison service logic in SbomService to compute diffs between two SBOMs
    - Add GET /api/v2/sbom/compare endpoint with query parameters left and right
    - Add integration tests for the comparison endpoint

trustify-ui:
  changes:
    - Add TypeScript interfaces for the comparison API response shape
    - Add API client function for the comparison endpoint
    - Add React Query hook for SBOM comparison
    - Create SbomComparePage with header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections
    - Add route for /sbom/compare in route definitions
    - Add SBOM selection checkboxes and "Compare selected" button on SbomListPage
```
