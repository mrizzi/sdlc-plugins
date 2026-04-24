# Task 4 — Frontend API types, client function, and React Query hook

## Repository
trustify-ui

## Description
Add the TypeScript type definitions, API client function, and React Query hook for the SBOM comparison endpoint. This establishes the frontend data layer for the comparison feature, following existing patterns for API integration.

## Files to Modify
- `src/api/models.ts` — Add `SbomComparisonResult`, `PackageDiffEntry`, `VersionChangeEntry`, `VulnerabilityDiffEntry`, and `LicenseChangeEntry` TypeScript interfaces
- `src/api/rest.ts` — Add `compareSboms(leftId: string, rightId: string)` API client function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook `useSbomComparison(leftId, rightId)` that wraps the API call with enabled/disabled logic based on whether both IDs are provided

## Implementation Notes
- Follow the type definition pattern in `src/api/models.ts` — existing interfaces like SBOM response types use TypeScript interfaces with camelCase field names mapped from the backend's snake_case JSON.
- Follow the API client function pattern in `src/api/rest.ts` — existing functions like `fetchSboms()` use the Axios instance from `src/api/client.ts` with typed return values.
- Follow the React Query hook pattern in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts` — these use `useQuery` with typed query keys and return types.
- The hook should accept `leftId` and `rightId` as parameters and set `enabled: !!leftId && !!rightId` to prevent calling the API until both IDs are selected.
- Use query key `["sbom-comparison", leftId, rightId]` for cache management.

### Backend API contracts
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape:
  ```typescript
  interface SbomComparisonResult {
    added_packages: PackageDiffEntry[];
    removed_packages: PackageDiffEntry[];
    version_changes: VersionChangeEntry[];
    new_vulnerabilities: VulnerabilityDiffEntry[];
    resolved_vulnerabilities: VulnerabilityDiffEntry[];
    license_changes: LicenseChangeEntry[];
  }

  interface PackageDiffEntry {
    name: string;
    version: string;
    license: string;
    advisory_count: number;
  }

  interface VersionChangeEntry {
    name: string;
    left_version: string;
    right_version: string;
    direction: "upgrade" | "downgrade";
  }

  interface VulnerabilityDiffEntry {
    advisory_id: string;
    severity: string;
    title: string;
    affected_package: string;
  }

  interface LicenseChangeEntry {
    name: string;
    left_license: string;
    right_license: string;
  }
  ```
  Defined by backend endpoint in `modules/fundamental/src/sbom/endpoints/compare.rs`.

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/models.ts` — existing TypeScript interfaces for API response types to follow the same pattern
- `src/api/rest.ts` — existing API client functions (e.g., `fetchSboms()`) to follow the same Axios pattern
- `src/api/client.ts` — Axios instance with base URL and auth interceptors
- `src/hooks/useSboms.ts` — existing React Query hook pattern for list queries
- `src/hooks/useSbomById.ts` — existing React Query hook pattern for single-resource queries

## Acceptance Criteria
- [ ] `SbomComparisonResult` and related interfaces are defined in `models.ts`
- [ ] `compareSboms()` function calls `GET /api/v2/sbom/compare` with `left` and `right` query params
- [ ] `useSbomComparison` hook is disabled when either ID is missing
- [ ] `useSbomComparison` hook returns typed `SbomComparisonResult` data
- [ ] Query cache key includes both SBOM IDs for proper cache invalidation

## Test Requirements
- [ ] Unit test: `useSbomComparison` does not fire API call when `leftId` is undefined
- [ ] Unit test: `useSbomComparison` does not fire API call when `rightId` is undefined
- [ ] Unit test: `useSbomComparison` calls API with correct query params when both IDs are provided
- [ ] Unit test: `compareSboms()` sends GET request to correct URL with query parameters

## Dependencies
- Depends on: Task 2 — Backend comparison endpoint and route registration (API contract must be finalized)
