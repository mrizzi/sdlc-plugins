# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

Changes:
- Add comparison diff model structs (`SbomComparisonResult`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`) in `modules/fundamental/src/sbom/model/`
- Add comparison service method to `SbomService` that loads two SBOMs, computes package/vulnerability/license diffs on-the-fly from existing entity data
- Add `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint in `modules/fundamental/src/sbom/endpoints/`
- Register the comparison route in `modules/fundamental/src/sbom/endpoints/mod.rs`
- Add integration tests for the comparison endpoint in `tests/api/sbom.rs`

## trustify-ui

Changes:
- Add TypeScript interfaces for the comparison API response in `src/api/models.ts`
- Add `compareSboms(leftId, rightId)` API client function in `src/api/rest.ts`
- Add `useSbomComparison` React Query hook in `src/hooks/`
- Add `SbomComparePage` page component at `src/pages/SbomComparePage/` with header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections
- Add route definition for `/sbom/compare` in `src/routes.tsx`
- Modify `SbomListPage` to support multi-select checkboxes and a "Compare selected" action button
- Add unit tests for the comparison page and integration with MSW mock handlers
