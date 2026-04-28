## Repository
trustify-ui

## Description
Add TypeScript interfaces for the SBOM comparison API response, an API client function to call the comparison endpoint, and a React Query hook to manage the comparison data lifecycle. This provides the data layer that the comparison UI components will consume.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces for the comparison response: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `src/api/rest.ts` — Add `compareSboms(leftId: string, rightId: string)` API client function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call, enabled only when both IDs are provided

## Implementation Notes
**TypeScript interfaces** — add to `src/api/models.ts` following the existing interface patterns in that file. The interfaces must match the backend response shape exactly:

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
  Backend source: `modules/fundamental/src/sbom/model/comparison.rs` in trustify-backend (Task 1). Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

**API client function** — add to `src/api/rest.ts` following the pattern of existing functions like `fetchSboms()`. Use the Axios instance from `src/api/client.ts`:
```typescript
export const compareSboms = (leftId: string, rightId: string): Promise<SbomComparisonResult> =>
  client.get("/api/v2/sbom/compare", { params: { left: leftId, right: rightId } }).then(r => r.data);
```

**React Query hook** — create `src/hooks/useSbomComparison.ts` following the pattern in `src/hooks/useSbomById.ts` and `src/hooks/useSboms.ts`. The hook should:
1. Accept `leftId: string | undefined` and `rightId: string | undefined` as parameters
2. Use `useQuery` with a query key like `["sbom-comparison", leftId, rightId]`
3. Set `enabled: !!leftId && !!rightId` so the query only fires when both IDs are provided
4. Return the standard React Query result object (`data`, `isLoading`, `isError`, etc.)

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — existing API client function; follow the same Axios pattern
- `src/api/client.ts` — Axios instance with base URL and auth interceptors
- `src/hooks/useSbomById.ts` — existing React Query hook; follow the same `useQuery` pattern with conditional `enabled` flag
- `src/hooks/useSboms.ts` — existing React Query hook for SBOM list; reference for query key naming

## Acceptance Criteria
- [ ] TypeScript interfaces match the backend comparison response shape exactly
- [ ] `compareSboms` function calls the correct endpoint with left/right query parameters
- [ ] `useSbomComparison` hook returns comparison data when both SBOM IDs are provided
- [ ] Hook does not fire the query when either SBOM ID is undefined
- [ ] No TypeScript compilation errors

## Test Requirements
- [ ] Unit test: `useSbomComparison` hook returns data when both IDs are provided (using MSW to mock the endpoint)
- [ ] Unit test: `useSbomComparison` hook does not fire when one ID is undefined
- [ ] Unit test: `useSbomComparison` hook handles error responses correctly

## Dependencies
- Depends on: Task 2 — Backend comparison endpoint (the API must exist for the client to call)
