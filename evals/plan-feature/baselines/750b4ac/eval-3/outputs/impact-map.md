# Repository Impact Map — TC-9003: SBOM Comparison View

## Workflow Mode

**Mode:** `feature-branch`

**Rationale:** Atomicity indicator #4 (tightly coupled feature components) is present. The frontend comparison page (`/sbom/compare`) requires the new backend endpoint `GET /api/v2/sbom/compare` which does not yet exist. The frontend cannot function without the backend endpoint, and the backend endpoint serves no purpose without the frontend consumer. Merging either side independently would leave `main` with dead code or broken references.

**Interdependent tasks:** All frontend tasks (API types, hooks, comparison page) depend on the backend comparison endpoint task. The frontend comparison page also depends on the frontend API layer tasks.

---

## Impact Map

trustify-backend:
  changes:
    - Add SBOM comparison diff model types (SbomComparisonResult, added/removed/changed package structs, vulnerability diff structs, license change structs)
    - Add SbomService comparison method to compute structured diff between two SBOMs using existing package, advisory, and license data
    - Add GET /api/v2/sbom/compare endpoint with left/right query parameters returning the structured diff response
    - Add integration tests for the comparison endpoint covering added/removed packages, version changes, new/resolved vulnerabilities, and license changes

trustify-ui:
  changes:
    - Add TypeScript interfaces for the SBOM comparison API response shape
    - Add API client function for the comparison endpoint and React Query hook
    - Add SbomComparePage with SBOM selectors, compare button, collapsible diff sections, and empty/loading states per Figma design
    - Add route registration for /sbom/compare
    - Add checkbox selection and "Compare selected" action to SbomListPage
    - Add unit tests for the comparison page and E2E test for the comparison workflow
