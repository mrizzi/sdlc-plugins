# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

Changes:
- Add SBOM comparison diff model structs (SbomComparisonResult with added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
- Add SBOM comparison service logic to compute on-the-fly diffs between two SBOMs using existing package, advisory, and license data
- Add `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint that returns structured diff response
- Add integration tests for the comparison endpoint covering added/removed packages, version changes, vulnerability diffs, license changes, error cases (invalid IDs, same SBOM), and performance with large SBOMs

## trustify-ui

Changes:
- Add TypeScript interfaces for the SBOM comparison API response types (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)
- Add API client function `compareSboms(leftId, rightId)` calling `GET /api/v2/sbom/compare`
- Add React Query hook `useSbomComparison` for the comparison endpoint
- Add SbomComparePage component with header toolbar (two SBOM selectors, Compare button, Export dropdown) and six collapsible diff sections per Figma design
- Add route `/sbom/compare` with URL query params `left` and `right` for shareability
- Add checkbox selection to SbomListPage for multi-select with "Compare selected" action
- Add unit tests for the comparison page component and hook (MSW mocks)

---

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** Atomicity indicator #4 (Tightly coupled feature components) is present. The frontend comparison page requires the new backend `GET /api/v2/sbom/compare` endpoint that does not yet exist. Merging the frontend changes to main without the backend endpoint would result in a broken comparison page (API calls to a non-existent endpoint). The backend endpoint alone is harmless on main, but the frontend depends on it. Additionally, the SbomListPage checkbox selection UI ("Compare selected" button) navigates to the comparison page, which would lead to a broken user experience without the backend. These cross-repository dependencies require all-or-nothing delivery.

**Interdependent tasks:** The frontend comparison page task depends on the backend endpoint task. The SbomListPage checkbox selection task depends on the frontend comparison page task (navigates to it).
