# Repository Impact Map — TC-9003: SBOM Comparison View

trustify-backend:
  changes:
    - Add SBOM comparison model types (SbomComparisonResult and related structs for added/removed packages, version changes, vulnerabilities, license changes)
    - Add SBOM comparison diff service logic to compute structured diffs between two SBOMs
    - Add GET /api/v2/sbom/compare endpoint with left and right query parameters
    - Add integration tests for the comparison endpoint

trustify-ui:
  changes:
    - Add TypeScript interfaces for the comparison API response types
    - Add API client function to call the comparison endpoint
    - Add React Query hook for managing comparison data fetching state
    - Add SBOM comparison page at /sbom/compare with header toolbar and six collapsible diff sections
    - Add route definition for the comparison page
    - Update SBOM list page with checkbox selection and "Compare selected" navigation button
    - Add unit tests and MSW mocks for comparison features

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** Atomicity indicator #4 (Tightly coupled feature components) is present. The frontend comparison page at `/sbom/compare` requires the backend comparison endpoint `GET /api/v2/sbom/compare` which does not yet exist. Neither side functions independently:
- The backend endpoint without the frontend has no consumer
- The frontend page without the backend endpoint would call a non-existent API and fail

**Interdependent tasks:**
- Task 4 (frontend API types/hook) depends on Task 3 (backend endpoint) for the API contract
- Task 5 (frontend comparison page) depends on Task 4 (frontend hook) which depends on Task 3 (backend endpoint)
- Task 6 (frontend list page selection) depends on Task 5 (frontend comparison page) for the navigation target

The `workflow:feature-branch` label will be applied to the feature issue TC-9003 in Step 6a.
