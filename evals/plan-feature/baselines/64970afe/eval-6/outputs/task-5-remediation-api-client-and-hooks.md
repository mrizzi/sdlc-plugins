## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Add TypeScript interfaces for the remediation API response types, Axios client functions for calling the two remediation endpoints, and React Query hooks for data fetching. This establishes the frontend data layer for the remediation dashboard.

## Files to Create
- `src/hooks/useRemediationSummary.ts` -- React Query hook for GET /api/v2/remediation/summary
- `src/hooks/useRemediationByProduct.ts` -- React Query hook for GET /api/v2/remediation/by-product

## Files to Modify
- `src/api/models.ts` -- add RemediationSummary, SeverityStatusCount, and ProductRemediation interfaces
- `src/api/rest.ts` -- add fetchRemediationSummary() and fetchRemediationByProduct() client functions

## Implementation Notes
- Per CONVENTIONS.md $API Layer: follow the Axios client pattern in `src/api/rest.ts` for client functions (e.g., `fetchSboms()`) and create React Query hooks in `src/hooks/` matching the pattern in `src/hooks/useSboms.ts`.
  Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's .ts hook scope.
- Per CONVENTIONS.md $Naming: use camelCase for hooks and utility functions (e.g., `useRemediationSummary`, `fetchRemediationSummary`).
  Applies: task creates `src/hooks/useRemediationByProduct.ts` matching the convention's TypeScript naming scope.
- **Backend API contracts:**
  - `GET /api/v2/remediation/summary` -- response shape: `{ severities: { critical: StatusCounts, high: StatusCounts, medium: StatusCounts, low: StatusCounts } }` where `StatusCounts = { open: number, inProgress: number, resolved: number }` (see `modules/fundamental/src/remediation/model/summary.rs` in trustify-backend)
  - `GET /api/v2/remediation/by-product` -- response shape: `PaginatedResults<{ productName: string, total: number, open: number, resolved: number }>` (see `modules/fundamental/src/remediation/model/by_product.rs` in trustify-backend)
  - Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` -- reference implementation for typed API client function
- `src/api/rest.ts::fetchAdvisories` -- reference for API function pattern with pagination
- `src/hooks/useSboms.ts` -- reference implementation for React Query hook pattern
- `src/hooks/useAdvisories.ts` -- reference for query hook pattern with list data
- `src/api/client.ts` -- Axios instance with base URL and auth interceptors (reuse directly)

## Acceptance Criteria
- [ ] TypeScript interfaces for RemediationSummary and ProductRemediation are defined in models.ts
- [ ] fetchRemediationSummary() and fetchRemediationByProduct() functions are added to rest.ts
- [ ] useRemediationSummary and useRemediationByProduct hooks are created and correctly typed
- [ ] Hooks use React Query's useQuery with appropriate query keys

## Test Requirements
- [ ] Verify TypeScript interfaces compile without errors
- [ ] Verify hooks can be imported and used in component tests
- [ ] Add MSW handlers for the remediation endpoints in tests/mocks/handlers.ts

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9006 from main
- Depends on: Task 2 -- Add remediation module with summary aggregation service and endpoint
- Depends on: Task 3 -- Add per-product remediation breakdown endpoint
