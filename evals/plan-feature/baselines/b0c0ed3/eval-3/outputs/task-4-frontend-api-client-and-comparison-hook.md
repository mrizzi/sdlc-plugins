## Repository
trustify-ui

## Description
Add the TypeScript interfaces, API client function, and React Query hook for the SBOM comparison endpoint. This task creates the data-fetching layer that the comparison page UI (Task 5) will consume. The API client function calls the new `GET /api/v2/sbom/compare` endpoint built in the backend tasks.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces for the comparison response: `SbomComparisonResult`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string): Promise<SbomComparisonResult>` function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call with `left` and `right` SBOM IDs as parameters

## Implementation Notes
**TypeScript interfaces** — Add to `src/api/models.ts` following the existing interface patterns in that file. The interfaces must match the backend response shape exactly:

```typescript
export interface PackageDiff {
  name: string;
  version: string;
  license: string;
  advisory_count: number;
}

export interface VersionChange {
  name: string;
  left_version: string;
  right_version: string;
  direction: "upgrade" | "downgrade";
}

export interface VulnerabilityDiff {
  advisory_id: string;
  severity: string;
  title: string;
  affected_package: string;
}

export interface LicenseChange {
  name: string;
  left_license: string;
  right_license: string;
}

export interface SbomComparisonResult {
  added_packages: PackageDiff[];
  removed_packages: PackageDiff[];
  version_changes: VersionChange[];
  new_vulnerabilities: VulnerabilityDiff[];
  resolved_vulnerabilities: VulnerabilityDiff[];
  license_changes: LicenseChange[];
}
```

**API client function** — Add to `src/api/rest.ts` following the pattern of existing functions like `fetchSboms()`. Use the Axios instance from `src/api/client.ts`:
```typescript
export const fetchSbomComparison = (leftId: string, rightId: string): Promise<SbomComparisonResult> =>
  client.get(`/api/v2/sbom/compare`, { params: { left: leftId, right: rightId } }).then(res => res.data);
```

**React Query hook** — Follow the pattern in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts`. The hook should:
- Accept `leftId` and `rightId` as parameters
- Use a query key like `["sbom-comparison", leftId, rightId]`
- Only enable the query when both IDs are provided (use the `enabled` option)
- Return the standard `useQuery` result object

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` as defined above (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)
- Returns 400 if either `left` or `right` param is missing
- Returns 404 if either SBOM ID does not exist

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — Existing API client function pattern to follow for the comparison function
- `src/api/client.ts` — Axios instance with base URL and auth interceptors; import and use for the comparison request
- `src/hooks/useSbomById.ts` — React Query hook pattern with single-entity query key; adapt for two-ID query key
- `src/hooks/useSboms.ts` — React Query hook pattern for list queries; reference for query key conventions

## Acceptance Criteria
- [ ] `SbomComparisonResult` and all nested interfaces are defined in `src/api/models.ts`
- [ ] `fetchSbomComparison` function exists in `src/api/rest.ts` and calls the correct endpoint with query parameters
- [ ] `useSbomComparison` hook exists in `src/hooks/useSbomComparison.ts` and returns React Query result
- [ ] The hook is disabled (does not fire a request) when either SBOM ID is missing or empty
- [ ] The hook uses a query key that includes both SBOM IDs for proper caching

## Test Requirements
- [ ] Unit test: `fetchSbomComparison` calls the correct URL with left and right query params
- [ ] Unit test: `useSbomComparison` returns data matching `SbomComparisonResult` when both IDs are provided (use MSW mock)
- [ ] Unit test: `useSbomComparison` does not fire a request when `leftId` is empty
- [ ] Unit test: `useSbomComparison` does not fire a request when `rightId` is empty

## Dependencies
- Depends on: Task 2 — Backend comparison endpoint (the API must exist for the client to call)
