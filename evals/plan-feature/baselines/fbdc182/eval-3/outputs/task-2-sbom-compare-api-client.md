## Repository
trustify-ui

## Description
Add the TypeScript API client function, response type interfaces, and a React Query hook for the new `GET /api/v2/sbom/compare` backend endpoint. This data-layer task is a prerequisite for the comparison UI page (Task 3) and must be complete before the page component is built.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for the `SbomDiff` response and its sub-types (`AddedPackage`, `RemovedPackage`, `VersionChange`, `VulnerabilityChange`, `LicenseChange`)
- `src/api/rest.ts` — add `fetchSbomCompare(leftId: string, rightId: string): Promise<SbomDiff>` function using the existing Axios client

## Files to Create
- `src/hooks/useSbomCompare.ts` — React Query hook `useSbomCompare(leftId, rightId)` that calls `fetchSbomCompare`; enabled only when both IDs are provided

## Implementation Notes

**Model interfaces** — follow the naming and style of existing interfaces in `src/api/models.ts`. Add:
```typescript
export interface AddedPackage {
  name: string;
  version: string;
  license: string;
  advisory_count: number;
}

export interface RemovedPackage {
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

export interface VulnerabilityChange {
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

export interface SbomDiff {
  added_packages: AddedPackage[];
  removed_packages: RemovedPackage[];
  version_changes: VersionChange[];
  new_vulnerabilities: VulnerabilityChange[];
  resolved_vulnerabilities: VulnerabilityChange[];
  license_changes: LicenseChange[];
}
```

**API function** — follow the pattern of existing functions in `src/api/rest.ts` which use the Axios instance from `src/api/client.ts`. Add:
```typescript
export const fetchSbomCompare = (leftId: string, rightId: string): Promise<SbomDiff> =>
  client.get("/sbom/compare", { params: { left: leftId, right: rightId } }).then((r) => r.data);
```

**React Query hook** — follow the pattern of `src/hooks/useSbomById.ts` (single-entity hook with an ID dependency). The hook should only fire when both `leftId` and `rightId` are non-empty strings:
```typescript
export const useSbomCompare = (leftId: string | undefined, rightId: string | undefined) =>
  useQuery({
    queryKey: ["sbom-compare", leftId, rightId],
    queryFn: () => fetchSbomCompare(leftId!, rightId!),
    enabled: !!leftId && !!rightId,
  });
```

**MSW mock handler** — add a handler in `tests/mocks/handlers.ts` for `GET /api/v2/sbom/compare` that returns a fixture; add `tests/mocks/fixtures/sbom-compare.json` with representative diff data covering all six diff categories.

## Reuse Candidates
- `src/api/client.ts` — existing Axios instance; import and use directly, do not create a new instance
- `src/hooks/useSbomById.ts` — pattern for a `useQuery` hook with an `enabled` guard on a nullable ID parameter
- `src/api/models.ts` — existing interface patterns; add new interfaces to the same file rather than creating a new models file
- `src/api/rest.ts` — existing fetch function patterns; add `fetchSbomCompare` alongside existing functions
- `tests/mocks/handlers.ts` — add MSW handler here to follow project-wide test mock pattern
- `tests/mocks/fixtures/sboms.json` — reference for fixture file format and naming convention

## Acceptance Criteria
- [ ] `SbomDiff` and all sub-type interfaces are exported from `src/api/models.ts`
- [ ] `fetchSbomCompare(leftId, rightId)` is exported from `src/api/rest.ts` and calls `GET /api/v2/sbom/compare?left={leftId}&right={rightId}`
- [ ] `useSbomCompare(leftId, rightId)` hook is exported from `src/hooks/useSbomCompare.ts`
- [ ] Hook returns `{ data, isLoading, isError }` consistent with other hooks in `src/hooks/`
- [ ] Hook does not fire (`enabled: false`) when either ID is `undefined` or empty string
- [ ] MSW handler added to `tests/mocks/handlers.ts` for the compare endpoint
- [ ] Fixture file `tests/mocks/fixtures/sbom-compare.json` added with data for all six diff categories
- [ ] TypeScript compiles with no new errors (`tsc --noEmit`)

## Test Requirements
- [ ] Unit test for `useSbomCompare` in `src/hooks/useSbomCompare.test.ts` (or co-located): verify hook does not fire when IDs are undefined
- [ ] Unit test: when both IDs provided and MSW returns fixture data, hook resolves with typed `SbomDiff` data
- [ ] Unit test: when API returns an error, hook exposes `isError: true`

## Verification Commands
- `npm run typecheck` — no TypeScript errors
- `npm test -- useSbomCompare` — hook unit tests pass

## Dependencies
- Depends on: Task 1 — SBOM diff service and compare endpoint (backend must exist before integration testing against a real server)
