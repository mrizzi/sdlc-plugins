# Task 3 — Frontend: API types, client function, and React Query hook for SBOM comparison

## Repository
trustify-ui

## Description
Add TypeScript interfaces for the SBOM comparison API response, an Axios client function to call the comparison endpoint, and a React Query hook (`useSbomComparison`) to manage the comparison data fetching state. This establishes the data layer that the comparison page UI (Task 4) will consume.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for comparison response types
- `src/api/rest.ts` — add `compareSboms()` API client function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook for fetching comparison data

## Implementation Notes

### TypeScript interfaces (`models.ts`)

Add the following interfaces matching the backend API response shape:

```typescript
export interface PackageDiffEntry {
  name: string;
  version: string;
  license: string | null;
  advisory_count: number;
}

export interface VersionChangeEntry {
  name: string;
  left_version: string;
  right_version: string;
  direction: "upgrade" | "downgrade";
}

export interface VulnerabilityDiffEntry {
  advisory_id: string;
  severity: string;
  title: string;
  affected_package: string;
}

export interface LicenseChangeEntry {
  name: string;
  left_license: string;
  right_license: string;
}

export interface SbomComparisonDiff {
  added_packages: PackageDiffEntry[];
  removed_packages: PackageDiffEntry[];
  version_changes: VersionChangeEntry[];
  new_vulnerabilities: VulnerabilityDiffEntry[];
  resolved_vulnerabilities: VulnerabilityDiffEntry[];
  license_changes: LicenseChangeEntry[];
}
```

### API client function (`rest.ts`)

Add a function following the existing pattern used by `fetchSboms()` and other API functions in this file:

```typescript
export const compareSboms = (leftId: string, rightId: string): Promise<SbomComparisonDiff> =>
  client.get(`/api/v2/sbom/compare`, { params: { left: leftId, right: rightId } })
    .then((res) => res.data);
```

Use the existing Axios instance from `src/api/client.ts` which already has base URL and auth interceptors configured.

### React Query hook (`useSbomComparison.ts`)

Follow the pattern used in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts`:

```typescript
export const useSbomComparison = (leftId: string | undefined, rightId: string | undefined) => {
  return useQuery({
    queryKey: ["sbom-comparison", leftId, rightId],
    queryFn: () => compareSboms(leftId!, rightId!),
    enabled: !!leftId && !!rightId,
  });
};
```

The hook should only execute the query when both `leftId` and `rightId` are provided (use `enabled` option). Return the standard React Query result object (`data`, `isLoading`, `isError`, `error`).

### Backend API contracts

- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonDiff` (see `modules/fundamental/src/sbom/model/comparison.rs` in trustify-backend)
- Uses existing `GET /api/v2/sbom` endpoint via `useSboms` hook for populating SBOM selectors (already implemented)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/client.ts` — Axios instance with base URL and auth interceptors (use directly)
- `src/api/rest.ts::fetchSboms` — reference pattern for API client functions
- `src/hooks/useSboms.ts` — reference pattern for React Query hooks with `useQuery`
- `src/hooks/useSbomById.ts` — reference pattern for React Query hooks with conditional enabled flag
- `src/api/models.ts` — existing TypeScript interfaces to follow naming and style conventions

## Acceptance Criteria
- [ ] TypeScript interfaces for all comparison diff types are defined and exported
- [ ] `compareSboms()` function calls the correct endpoint with query parameters
- [ ] `useSbomComparison` hook returns loading, error, and data states
- [ ] Hook is disabled (does not fetch) when either SBOM ID is undefined
- [ ] All types align with the backend API response contract

## Test Requirements
- [ ] Unit test: `useSbomComparison` hook returns data on successful API response (using MSW mock)
- [ ] Unit test: `useSbomComparison` hook is disabled when leftId or rightId is undefined
- [ ] Unit test: `useSbomComparison` hook handles API error responses correctly

## Dependencies
- Depends on: Task 2 — Backend: SBOM comparison endpoint and route registration (API contract must be finalized)
