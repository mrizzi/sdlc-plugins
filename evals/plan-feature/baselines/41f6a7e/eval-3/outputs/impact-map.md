# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

Changes:
- Add SBOM comparison diff model structs (SbomComparisonResult with added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
- Add SBOM comparison service logic to compute structured diffs between two SBOMs on-the-fly from existing package and advisory data
- Add `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint returning the structured diff response
- Add integration tests for the comparison endpoint covering happy path, edge cases, and performance with large SBOMs

## trustify-ui

Changes:
- Add TypeScript interfaces for the SBOM comparison API response types
- Add API client function `compareSboms(leftId, rightId)` calling the new backend endpoint
- Add React Query hook `useSbomComparison` for the comparison API call
- Add SBOM comparison page at `/sbom/compare` with header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections per Figma design
- Add route definition for `/sbom/compare` in the router
- Add "Compare selected" action to the SBOM list page for selecting two SBOMs
- Add unit tests for the comparison page components and E2E test for the comparison workflow

---

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** Atomicity indicator #4 (tightly coupled feature components) is present. The frontend comparison page requires the new backend `GET /api/v2/sbom/compare` endpoint to function. Neither side delivers user value independently — the backend endpoint has no consumer without the frontend, and the frontend page cannot render comparison data without the backend endpoint. Merging either side alone to `main` would leave dead code or a broken UI.

**Interdependent tasks:**
- The backend comparison endpoint task and the frontend comparison page task are tightly coupled — the frontend task depends on the backend endpoint existing and returning the expected response shape.
- The frontend SBOM list page modification (adding "Compare selected" button) depends on the comparison page route existing.
