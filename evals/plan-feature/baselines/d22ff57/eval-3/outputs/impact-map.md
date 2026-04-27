# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

Changes:
- Add SBOM comparison diff model structs (`SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`) in `modules/fundamental/src/sbom/model/`
- Add SBOM comparison service method to `SbomService` that loads two SBOMs with their packages, advisories, and licenses, then computes the structured diff
- Add `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint in `modules/fundamental/src/sbom/endpoints/`
- Register the new comparison route in `modules/fundamental/src/sbom/endpoints/mod.rs`
- Add integration tests for the comparison endpoint in `tests/api/`

## trustify-ui

Changes:
- Add TypeScript interfaces for the comparison API response in `src/api/models.ts`
- Add API client function `compareSboms(leftId, rightId)` in `src/api/rest.ts`
- Add React Query hook `useSbomComparison` in `src/hooks/`
- Add comparison page route `/sbom/compare` in `src/routes.tsx`
- Create `SbomComparePage` page component with header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes)
- Add SBOM selection checkboxes and "Compare selected" action to the existing `SbomListPage`
- Add unit tests for the comparison page and integration with MSW mock handlers
