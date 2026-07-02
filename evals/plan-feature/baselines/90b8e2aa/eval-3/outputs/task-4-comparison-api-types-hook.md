## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response, an Axios-based API client function to call the backend comparison endpoint, and a React Query hook to manage comparison data fetching with loading/error states. This establishes the data layer that the comparison page (Task 5) will consume.

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook that wraps fetchSbomComparison(); accepts left and right SBOM IDs; disabled when either ID is null/undefined

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange
- `src/api/rest.ts` — Add fetchSbomComparison(leftId: string, rightId: string) function using the Axios client

## Implementation Notes
- Follow the existing TypeScript interface pattern in `src/api/models.ts` for defining API response types.
- Follow the existing API client function pattern in `src/api/rest.ts` (e.g., `fetchSboms()`) for the new `fetchSbomComparison()` function.
- Follow the existing React Query hook pattern in `src/hooks/useSboms.ts` for the new `useSbomComparison` hook.
- Use the Axios instance from `src/api/client.ts` which includes base URL and auth interceptors.
- The hook should use `useQuery` with `enabled: !!leftId && !!rightId` to prevent API calls when either ID is missing.
- Per the frontend key conventions (API layer): Axios client in `src/api/client.ts`; typed API functions in `src/api/rest.ts`; React Query hooks in `src/hooks/`.
  Applies: task modifies `src/api/rest.ts` and creates `src/hooks/useSbomComparison.ts` matching the convention's TypeScript API layer scope.
- Per the frontend key conventions (Naming): camelCase for hooks and utilities.
  Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's TypeScript file scope.
- Per the frontend key conventions (State management): React Query (TanStack Query) for server state; no Redux.
  Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's TypeScript hook scope.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id}&right={id}` — response shape:
  ```typescript
  interface SbomComparisonResult {
    added_packages: AddedPackage[];
    removed_packages: RemovedPackage[];
    version_changes: VersionChange[];
    new_vulnerabilities: NewVulnerability[];
    resolved_vulnerabilities: ResolvedVulnerability[];
    license_changes: LicenseChange[];
  }

  interface AddedPackage {
    name: string;
    version: string;
    license: string;
    advisory_count: number;
  }

  interface RemovedPackage {
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

  interface NewVulnerability {
    advisory_id: string;
    severity: string;
    title: string;
    affected_package: string;
  }

  interface ResolvedVulnerability {
    advisory_id: string;
    severity: string;
    title: string;
    previously_affected_package: string;
  }

  interface LicenseChange {
    name: string;
    left_license: string;
    right_license: string;
  }
  ```
  (see `modules/fundamental/src/sbom/endpoints/compare.rs` and `modules/fundamental/src/sbom/model/comparison.rs` in trustify-backend)
- Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/models.ts` — existing TypeScript interfaces to follow as pattern for new comparison types
- `src/api/rest.ts::fetchSboms()` — existing API client function demonstrating Axios usage with typed responses
- `src/hooks/useSboms.ts` — existing React Query hook demonstrating useQuery pattern with query key and fetch function
- `src/api/client.ts` — Axios instance with base URL and auth interceptors

## Acceptance Criteria
- [ ] TypeScript interfaces match the backend comparison endpoint response shape exactly
- [ ] fetchSbomComparison() calls GET /api/v2/sbom/compare with left and right query parameters
- [ ] useSbomComparison hook returns loading, error, and data states via React Query
- [ ] Hook is disabled (does not fire API call) when either SBOM ID is null or undefined
- [ ] Hook re-fetches when either SBOM ID changes

## Test Requirements
- [ ] Unit test for fetchSbomComparison() with MSW mock handler verifying correct endpoint and query parameters
- [ ] Unit test for useSbomComparison hook: returns data on successful API response
- [ ] Unit test for useSbomComparison hook: returns error state on API failure
- [ ] Unit test for useSbomComparison hook: does not fetch when either ID is undefined

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add SBOM comparison REST endpoint and integration tests
