## Repository
trustify-backend

## Description
Add a dedicated integration test file for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering the main success path, 404 behavior, deduplication correctness, cache header presence, and post-ingestion cache invalidation. Tests run against a real PostgreSQL test database following the same harness used by `tests/api/sbom.rs` and `tests/api/advisory.rs`.

## Files to Create
- `tests/api/sbom_advisory_summary.rs` — integration tests for the advisory summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add `sbom_advisory_summary` to the `[[test]]` targets or the module list, matching the pattern used for `sbom.rs` and `advisory.rs`

## Implementation Notes
Follow the structure of `tests/api/sbom.rs` and `tests/api/advisory.rs` exactly:

1. **Test harness setup**: Use whatever shared test-DB setup function is already defined in the `tests/` crate (likely a `common` module or a `setup()` helper called at the top of each test). Do not duplicate DB bootstrapping logic.

2. **Seed helpers**: Reuse or extend existing seed helpers (likely in `tests/api/sbom.rs` or a shared fixtures module) to insert SBOM rows and advisory rows. Link them via the `sbom_advisory` join table. Use raw SeaORM inserts (same pattern as the existing test files) rather than calling the ingest HTTP endpoint for unit-level speed.

3. **Assertion pattern**: The existing tests use `assert_eq!(resp.status(), StatusCode::OK)`. Deserialize the JSON body into `AdvisorySeveritySummary` using `resp.json::<AdvisorySeveritySummary>().await.unwrap()` and assert individual fields.

4. **Cache header test**: After a successful 200 response, assert `resp.headers().get("cache-control").unwrap() == "max-age=300"`.

5. **Deduplication test**: Insert the same advisory ID into `sbom_advisory` twice for the same SBOM (simulating a duplicate correlation). Assert the summary counts that advisory only once.

6. **Cache invalidation test**: Call the summary endpoint to prime the cache, then trigger advisory ingestion via `POST /api/v2/ingest/advisory` (or the ingest service directly), then call the summary endpoint again and assert counts have updated.

Test cases to implement:

| Test name | Scenario | Expected result |
|---|---|---|
| `test_advisory_summary_returns_counts` | SBOM with 3 critical, 1 high advisories | `{ critical: 3, high: 1, medium: 0, low: 0, total: 4 }` |
| `test_advisory_summary_empty_sbom` | SBOM with no linked advisories | `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }` |
| `test_advisory_summary_deduplication` | Same advisory linked twice to SBOM | Advisory counted once |
| `test_advisory_summary_not_found` | Non-existent SBOM UUID | HTTP 404 |
| `test_advisory_summary_cache_header` | Successful response | `Cache-Control: max-age=300` present |
| `test_advisory_summary_cache_invalidation` | Ingest new advisory after priming cache | Second call reflects new count |

## Reuse Candidates
- `tests/api/sbom.rs` — test harness pattern, DB setup, HTTP client construction, `assert_eq!(resp.status(), StatusCode::OK)` idiom
- `tests/api/advisory.rs` — advisory seeding helpers and advisory entity insert patterns
- `entity/src/sbom_advisory.rs` — column names needed for direct insert in seed setup

## Acceptance Criteria
- [ ] All six test cases listed above are implemented and pass
- [ ] Tests do not share mutable state — each test seeds its own SBOM and advisory rows
- [ ] `cargo test -p tests` passes with no failures or ignored tests related to this feature

## Verification Commands
- `cargo test -p tests advisory_summary` — all six `test_advisory_summary_*` tests pass

## Dependencies
- Depends on: Task 3 — Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint with caching
- Depends on: Task 4 — Invalidate advisory summary cache in advisory ingestor
