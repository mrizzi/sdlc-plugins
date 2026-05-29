# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

Changes:
- Add SBOM comparison diff model structs (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)
- Add SBOM comparison service logic in the sbom service module (diff computation using existing package, advisory, and license data)
- Add `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint
- Add integration tests for the comparison endpoint

## trustify-ui

Changes:
- Add TypeScript interfaces for the SBOM comparison API response types
- Add API client function for fetching SBOM comparison results
- Add React Query hook for SBOM comparison data
- Add SBOM comparison page with header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes)
- Add route definition for `/sbom/compare`
- Add checkbox selection and "Compare selected" button to the SBOM list page
- Add unit tests for the comparison page and MSW mock handlers
- Add virtualized list rendering for large diffs (>100 changed packages)

## Workflow Mode Decision

**Selected mode: `feature-branch`**

**Rationale:** Atomicity indicator #4 (Tightly coupled feature components) is present. The frontend comparison page requires the new backend `GET /api/v2/sbom/compare` endpoint that does not yet exist. Merging the frontend task without the backend endpoint would result in a broken comparison page that calls a non-existent API. Merging the backend endpoint alone is safe but the feature is only usable with both sides deployed. The frontend and backend changes are interdependent — feature-branch mode ensures they land together.

**Interdependent tasks:**
- Backend: comparison endpoint task (provides the API)
- Frontend: comparison page task (consumes the API)
