# Task 8: Create MSW mocks and test fixtures for SBOM comparison

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Create mock data fixtures and MSW (Mock Service Worker) request handlers for the SBOM comparison endpoint. These mocks enable frontend unit tests and local development without a running backend. The mock data covers all six diff categories with representative sample data, and the MSW handler intercepts `GET /api/v2/sbom/compare` requests to return the fixture.

## Files to Create
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison response data containing representative entries for all six diff categories (added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, license changes)

## Files to Modify
- `tests/mocks/handlers.ts` — Add MSW handler for `GET /api/v2/sbom/compare` that returns the mock fixture data; include error case handlers for missing parameters and non-existent IDs

## Implementation Notes
- Follow the existing mock pattern in `tests/mocks/handlers.ts` which uses MSW's `http.get()` handler pattern with `HttpResponse.json()`.
- Follow the existing fixture pattern in `tests/mocks/fixtures/sboms.json` for file structure and naming.
- The mock fixture `sbom-comparison.json` should include:
  - 2-3 added packages with varying advisory counts
  - 1-2 removed packages
  - 2-3 version changes (mix of upgrades and downgrades)
  - 2-3 new vulnerabilities with varying severities (include at least one "critical" for testing severity highlighting)
  - 1-2 resolved vulnerabilities
  - 1-2 license changes
- The MSW handler should:
  1. Match `GET /api/v2/sbom/compare` requests.
  2. Extract `left` and `right` query parameters.
  3. Return `400` if either parameter is missing.
  4. Return the fixture data for valid requests.
- Register the new handler alongside existing handlers in the handlers array.

## Reuse Candidates
- `tests/mocks/handlers.ts` — existing MSW handlers as pattern reference
- `tests/mocks/fixtures/sboms.json` — existing fixture file as structure reference
- `tests/setup.ts` — test setup that initializes MSW with the handlers array
- `src/api/models.ts` — TypeScript interfaces (from Task 4) that define the expected mock data shape

## Acceptance Criteria
- [ ] Mock fixture file contains representative data for all six diff categories
- [ ] At least one mock vulnerability has "critical" severity for testing highlight behavior
- [ ] MSW handler intercepts `GET /api/v2/sbom/compare` requests
- [ ] Handler returns `400` when query parameters are missing
- [ ] Handler returns the fixture data for valid requests
- [ ] Handler is registered in the existing handlers array
- [ ] Mock data shape matches the TypeScript interfaces from `src/api/models.ts`

## Test Requirements
- [ ] MSW handler is verified by the component tests in Tasks 6 and 7 that exercise the comparison API flow
- [ ] Mock data covers edge cases: critical severity, downgrade direction, multiple advisory counts

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add SBOM comparison TypeScript types and API client function (interfaces define the mock data shape)

`[sdlc-workflow] Description digest: sha256-md:b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0`
