## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the TypeScript API layer for the SBOM comparison feature: type definitions for the comparison response, an API client function, and a React Query hook. This provides the data-fetching infrastructure that the comparison page UI (Task 6) consumes.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for the comparison response types
- `src/api/rest.ts` — add `fetchSbomComparison` API client function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call

## Implementation Notes
**TypeScript interfaces** (add to `src/api/models.ts`):
Follow the existing interface patterns in `models.ts` for naming and field conventions.

```typescript
interface PackageDiff {
  name: string;
  version: string;
  license: string;
  advisory_count: number;
}

interface VersionChange {
  name: string;
  left_version: string;
  right_version: string;
  direction: "upgrade" | "downgrade";
}

interface VulnerabilityDiff {
  advisory_id: string;
  severity: string;
  title: string;
  affected_package: string;
}

interface LicenseChange {
  name: string;
  left_license: string;
  right_license: string;
}

interface SbomComparison {
  added_packages: PackageDiff[];
  removed_packages: PackageDiff[];
  version_changes: VersionChange[];
  new_vulnerabilities: VulnerabilityDiff[];
  resolved_vulnerabilities: VulnerabilityDiff[];
  license_changes: LicenseChange[];
}
```

**API client function** (add to `src/api/rest.ts`):
Follow the existing pattern of functions like `fetchSboms()` and `fetchAdvisories()` which use the Axios instance from `src/api/client.ts`. The function should call `GET /api/v2/sbom/compare?left={leftId}&right={rightId}` and return `SbomComparison`.

**React Query hook** (create `src/hooks/useSbomComparison.ts`):
Follow the existing hook patterns in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts`. Use `useQuery` with a query key like `["sbom-comparison", leftId, rightId]`. The hook should be enabled only when both IDs are provided (use `enabled: !!leftId && !!rightId`).

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparison` (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)
- Returns 400 when `left` or `right` parameters are missing
- Returns 404 when either SBOM ID does not exist

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — existing API client function showing the Axios call pattern and response typing
- `src/hooks/useSboms.ts` — existing React Query hook demonstrating the query key pattern and hook structure
- `src/hooks/useSbomById.ts` — React Query hook for single entity fetch, showing the `enabled` option pattern
- `src/api/client.ts` — Axios instance with base URL and auth interceptors

## Acceptance Criteria
- [ ] TypeScript interfaces for `SbomComparison` and related types are defined in `models.ts`
- [ ] `fetchSbomComparison(leftId, rightId)` function is added to `rest.ts` using the existing Axios client
- [ ] `useSbomComparison(leftId, rightId)` React Query hook is created with proper query key and enabled flag
- [ ] All types match the backend API response shape

## Test Requirements
- [ ] Unit test for `useSbomComparison` hook: verify it calls the correct endpoint with correct parameters
- [ ] Unit test: verify hook is disabled when IDs are not provided
- [ ] Add MSW handler for `GET /api/v2/sbom/compare` in `tests/mocks/handlers.ts`
- [ ] Add mock comparison fixture data in `tests/mocks/fixtures/`

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003
- Depends on: Task 4 — Add GET /api/v2/sbom/compare endpoint
