# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

changes:
- Add SBOM comparison diff model structs (`SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`) in `modules/fundamental/src/sbom/model/`
- Add SBOM comparison diff service logic in `modules/fundamental/src/sbom/service/` that computes the structured diff between two SBOMs by querying existing package, advisory, and license data
- Add `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint in `modules/fundamental/src/sbom/endpoints/`
- Register comparison route in `modules/fundamental/src/sbom/endpoints/mod.rs`
- Add integration tests for the comparison endpoint in `tests/api/`

## trustify-ui

changes:
- Add TypeScript interfaces for the SBOM comparison response shape in `src/api/models.ts`
- Add API client function `compareSboms(leftId, rightId)` in `src/api/rest.ts`
- Add React Query hook `useSbomComparison` in `src/hooks/`
- Add `SbomComparePage` page component at `src/pages/SbomComparePage/` with header toolbar (dual SBOM selectors, Compare button, Export dropdown), diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes), empty state, and loading state
- Add route definition for `/sbom/compare` in `src/routes.tsx`
- Add SBOM selection UX (checkboxes + "Compare selected" button) to `src/pages/SbomListPage/SbomListPage.tsx`
- Add MSW mock handler and fixture data for the comparison endpoint in `tests/mocks/`
- Add unit tests for the comparison page in `src/pages/SbomComparePage/`
