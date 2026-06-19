# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

Changes:
- Add SBOM comparison diff model types (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)
- Add SBOM comparison service logic to compute a structured diff between two SBOMs using existing package, advisory, and license data
- Add GET /api/v2/sbom/compare?left={id1}&right={id2} endpoint with query parameter validation
- Add integration tests for the comparison endpoint covering added/removed packages, version changes, vulnerability diffs, and license changes

## trustify-ui

Changes:
- Add TypeScript interfaces for the comparison API response shape
- Add API client function to call the comparison endpoint
- Add React Query hook (useSbomComparison) for the comparison API call
- Add SBOM comparison page at /sbom/compare with header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes)
- Add route definition for /sbom/compare
- Add checkbox selection and "Compare selected" action to the existing SBOM list page

---

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present that would require feature-branch mode:

1. **No coordinated schema migrations** — the feature requires no new database tables; diffs are computed on-the-fly from existing data.
2. **No breaking API changes** — the backend adds a new GET endpoint (`/api/v2/sbom/compare`). This is purely additive and does not modify any existing endpoint contracts.
3. **No cross-cutting refactors** — no existing types, modules, or shared code are renamed or restructured.
4. **No tightly coupled deployment requirement** — the backend endpoint can merge to `main` independently. It is a new, additive endpoint that causes no harm if the frontend has not yet shipped. The frontend tasks depend on the backend tasks via the Dependencies section, ensuring correct ordering.

All tasks target `main` as their Target Branch. Cross-repo ordering is enforced through explicit Dependencies: frontend tasks that require the comparison endpoint list the backend endpoint task as a dependency.
