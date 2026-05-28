# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

Changes:
- Add SBOM comparison diff model types (structs for added/removed packages, version changes, new/resolved vulnerabilities, license changes) in `modules/fundamental/src/sbom/model/`
- Add SBOM comparison service logic in `modules/fundamental/src/sbom/service/` to compute structured diffs from existing package, advisory, and license data
- Add `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint in `modules/fundamental/src/sbom/endpoints/`
- Add integration tests for the comparison endpoint in `tests/api/`

## trustify-ui

Changes:
- Add TypeScript interfaces for the comparison API response shape in `src/api/models.ts`
- Add API client function `compareSboms(leftId, rightId)` in `src/api/rest.ts`
- Add React Query hook `useSbomComparison` in `src/hooks/`
- Add `SbomComparePage` with header toolbar (SBOM selectors, Compare button, Export dropdown) and six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes) per Figma design
- Add route `/sbom/compare` in `src/routes.tsx`
- Add "Compare selected" checkbox and button functionality to `SbomListPage`
- Add MSW mock handler, unit tests, and E2E tests for the comparison page

## Workflow Mode

**Selected mode:** `feature-branch`

**Rationale:** Atomicity indicator 4 (Tightly coupled feature components) is present. The frontend comparison page at `/sbom/compare` requires the new backend `GET /api/v2/sbom/compare` endpoint that does not yet exist. Neither side functions independently — the frontend cannot render comparison data without the backend endpoint, and the backend endpoint provides no user-facing value without the frontend comparison UI. Merging either side alone to `main` would leave the codebase with a non-functional feature.

**Interdependent tasks:** The frontend comparison page task depends on the backend comparison endpoint task. Both must land on the feature branch before merging to `main`.
