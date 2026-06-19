## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response and a client function to call the new backend endpoint. This establishes the typed API layer that the React Query hook and UI components will consume. The interfaces must match the JSON contract defined by the backend comparison model.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: `SbomComparison`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `src/api/rest.ts` — Add `compareSboms(leftId: string, rightId: string): Promise<SbomComparison>` client function

## Implementation Notes
Follow the existing patterns in `src/api/models.ts` and `src/api/rest.ts`.

TypeScript interfaces in `models.ts`:
```typescript
export interface SbomComparison {
  added_packages: AddedPackage[];
  removed_packages: RemovedPackage[];
  version_changes: VersionChange[];
  new_vulnerabilities: NewVulnerability[];
  resolved_vulnerabilities: ResolvedVulnerability[];
  license_changes: LicenseChange[];
}

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
```

Client function in `rest.ts`:
```typescript
export const compareSboms = (leftId: string, rightId: string): Promise<SbomComparison> =>
  client.get(`/api/v2/sbom/compare`, { params: { left: leftId, right: rightId } })
    .then((res) => res.data);
```

Use the existing Axios `client` instance from `src/api/client.ts`.

## Reuse Candidates
- `src/api/models.ts` — Existing interface patterns (naming, snake_case field alignment with backend)
- `src/api/rest.ts` — Existing client function patterns (`fetchSboms`, `fetchAdvisories`)
- `src/api/client.ts::client` — Axios instance with base URL and auth interceptors

## Acceptance Criteria
- [ ] All TypeScript interfaces are defined and exported from `models.ts`
- [ ] `compareSboms` function is defined and exported from `rest.ts`
- [ ] Interface field names match the backend JSON contract exactly (snake_case)
- [ ] TypeScript compilation passes (`tsc --noEmit`)

## Test Requirements
- [ ] Type compilation verification (no type errors)

## Dependencies
- Depends on: Task 4 — Backend comparison endpoint (API contract must be finalized)
- Depends on: Task 1 — Create feature branch
