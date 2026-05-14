# Repository Impact Map — TC-9003: SBOM Comparison View

## Workflow Mode

**Mode:** `feature-branch`

**Rationale:** The frontend comparison page requires a new backend endpoint (`GET /api/v2/sbom/compare`) that does not yet exist. Neither side functions independently — the frontend page cannot render comparison results without the backend diff endpoint, and the backend endpoint has no consumer without the frontend page. This satisfies atomicity indicator #4 (tightly coupled feature components).

**Interdependent tasks:** All frontend tasks depend on the backend comparison endpoint task. Merging the frontend without the backend would result in a broken comparison page; merging the backend alone is safe but incomplete.

---

## Impact Map

```
trustify-backend:
  changes:
    - Add SbomComparison response model with diff categories (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
    - Add comparison service method to SbomService that computes a structured diff between two SBOMs by comparing their package sets, advisory associations, and license mappings
    - Add GET /api/v2/sbom/compare?left={id1}&right={id2} endpoint that validates inputs and delegates to the comparison service
    - Add integration tests for the comparison endpoint covering: basic diff, identical SBOMs, missing SBOM IDs, large SBOM comparisons

trustify-ui:
  changes:
    - Add TypeScript interfaces for the comparison API response shape and add a fetchSbomComparison() API client function in the API layer
    - Add React Query hook useSbomComparison for the comparison endpoint
    - Add SbomComparePage with header toolbar (SBOM selectors, Compare button, Export dropdown) and diff sections using PatternFly ExpandableSection, Badge, and Table components per Figma specifications
    - Add route definition for /sbom/compare in the router
    - Add checkbox selection to SbomListPage with a "Compare selected" action that navigates to the comparison page
    - Add unit and E2E tests for the comparison page
```
