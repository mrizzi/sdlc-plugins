# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

Changes:
- Add SBOM comparison diff model structs (`SbomComparisonResult`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`) in `modules/fundamental/src/sbom/model/`
- Add SBOM comparison service method in `modules/fundamental/src/sbom/service/sbom.rs` that computes a structured diff between two SBOMs by comparing their packages, advisories, and licenses
- Add `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint in `modules/fundamental/src/sbom/endpoints/`
- Register the comparison route in `modules/fundamental/src/sbom/endpoints/mod.rs`
- Add integration tests for the comparison endpoint in `tests/api/sbom.rs`

## trustify-ui

Changes:
- Add TypeScript interfaces for the SBOM comparison response in `src/api/models.ts`
- Add API client function `compareSboms(leftId, rightId)` in `src/api/rest.ts`
- Add React Query hook `useSbomComparison` in `src/hooks/`
- Create `SbomComparePage` component at `src/pages/SbomComparePage/` with header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections
- Create page-specific sub-components: diff section tables for added/removed packages, version changes, new/resolved vulnerabilities, and license changes
- Add route `/sbom/compare` in `src/routes.tsx`
- Add checkbox selection and "Compare selected" button to `SbomListPage`
- Add unit tests for the comparison page and components
- Add MSW mock handler for the comparison endpoint

## Workflow Mode

**Mode: feature-branch**

**Rationale:** Atomicity indicator #4 (Tightly coupled feature components) applies. The frontend comparison page requires the new backend `GET /api/v2/sbom/compare` endpoint that does not yet exist. Merging the frontend to main without the backend endpoint would result in a broken comparison page. Merging the backend endpoint to main first would add unused API surface. Both sides must land together for a coherent feature delivery.

**Interdependent tasks:** All frontend tasks depend on the backend comparison endpoint task. The backend endpoint and frontend page are tightly coupled — neither functions independently in a meaningful way for end users.
