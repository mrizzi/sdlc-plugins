# Task 4 — Add SBOM comparison API types and client function

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response and a typed API client function to call the new backend comparison endpoint. This establishes the frontend data contract matching the backend's `SbomComparisonResult` structure and provides the data-fetching function that React Query hooks will consume.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for the comparison result types
- `src/api/rest.ts` — add `fetchSbomComparison()` API client function

## Implementation Notes
**TypeScript interfaces** to add in `src/api/models.ts`:

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

export interface NewVulnerability {
  advisory_id: string;
  severity: string;
  title: string;
  affected_package: string;
}

export interface ResolvedVulnerability {
  advisory_id: string;
  severity: string;
  title: string;
  previously_affected_package: string;
}

export interface LicenseChange {
  name: string;
  left_license: string;
  right_license: string;
}

export interface SbomComparisonResult {
  added_packages: AddedPackage[];
  removed_packages: RemovedPackage[];
  version_changes: VersionChange[];
  new_vulnerabilities: NewVulnerability[];
  resolved_vulnerabilities: ResolvedVulnerability[];
  license_changes: LicenseChange[];
}
```

**API client function** to add in `src/api/rest.ts`:

```typescript
export const fetchSbomComparison = (leftId: string, rightId: string): Promise<SbomComparisonResult> =>
  client.get(`/api/v2/sbom/compare`, { params: { left: leftId, right: rightId } })
    .then((res) => res.data);
```

Use the existing Axios `client` instance from `src/api/client.ts`, following the same pattern as `fetchSboms()` and other functions in `rest.ts`.

Per CONVENTIONS.md §API Layer: typed API functions in `src/api/rest.ts` use the Axios client from `src/api/client.ts`.
Applies: task modifies `src/api/rest.ts` matching the convention's API layer scope.

## Acceptance Criteria
- [ ] All six sub-types and the `SbomComparisonResult` interface are defined in `models.ts`
- [ ] `fetchSbomComparison()` calls `GET /api/v2/sbom/compare` with left and right query parameters
- [ ] Function returns a typed `Promise<SbomComparisonResult>`
- [ ] Interfaces match the backend response shape exactly (snake_case field names)

## Test Requirements
- [ ] Add MSW handler in `tests/mocks/handlers.ts` for `GET /api/v2/sbom/compare` returning a mock `SbomComparisonResult`
- [ ] Add mock fixture data in `tests/mocks/fixtures/` for comparison response

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003

[sdlc-workflow] Description digest: sha256-md:5fff84174e038a74ccfa36a9a9069a29ea82063e1cbeea03a78ad7f32c7171b8
