## Repository
trustify-backend

## Description
Add comprehensive integration tests for the improved search endpoint, covering relevance ranking, filtering, caching, and backward compatibility. The existing test file at `tests/api/search.rs` contains search endpoint integration tests that must be updated to cover the new functionality while ensuring existing test cases still pass.

## Files to Modify
- `tests/api/search.rs` — Extend the existing search integration tests with new test cases for full-text relevance ranking, filter parameters, combined filters, cache headers, edge cases (empty queries, special characters, invalid filters), and backward compatibility. Follow the existing `assert_eq!(resp.status(), StatusCode::OK)` pattern used in this file and in `tests/api/sbom.rs` and `tests/api/advisory.rs`.

## Implementation Notes
- Follow the integration test conventions from `tests/api/sbom.rs` and `tests/api/advisory.rs`: tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Test data setup: insert test SBOMs, advisories, and packages with known text content and severity levels so that search results are deterministic and rankable.
- For relevance ranking tests: insert documents with varying degrees of match quality (exact title match, partial match, no match) and verify the returned order matches expected ranking.
- For filter tests: insert a mix of entity types and severities, then verify each filter narrows results correctly.
- For backward compatibility: verify that existing search query patterns (no filters, basic text search) still return the same response structure (same JSON fields, same pagination format).
- For caching tests: verify `Cache-Control` headers are present in responses.
- Reference `common/src/model/paginated.rs` (`PaginatedResults`) for the expected response structure when asserting on response body shape.

## Reuse Candidates
- `tests/api/sbom.rs` — Test patterns for API endpoint integration tests (request building, response assertion)
- `tests/api/advisory.rs` — Test patterns including severity-related assertions
- `common/src/model/paginated.rs::PaginatedResults` — Expected response shape for list/search endpoints

## Acceptance Criteria
- [ ] All new tests pass against a PostgreSQL test database
- [ ] Existing search tests continue to pass (no regressions)
- [ ] Tests cover relevance ranking, all filter types, filter combinations, caching headers, and error cases
- [ ] Test coverage includes edge cases: empty query, special characters, invalid filter values, no results

## Test Requirements
- [ ] Integration test: basic text search returns results ranked by relevance score descending
- [ ] Integration test: search with `type=sbom` filter returns only SBOM results
- [ ] Integration test: search with `type=advisory` filter returns only advisory results
- [ ] Integration test: search with `severity=critical` filter returns only critical advisories
- [ ] Integration test: search with `created_after` date filter excludes older results
- [ ] Integration test: combining `type` and `severity` filters returns correctly narrowed results
- [ ] Integration test: search with no filters returns all entity types (backward compatibility)
- [ ] Integration test: search response includes `relevance_score` field in each result
- [ ] Integration test: search response includes `Cache-Control` header
- [ ] Integration test: empty search query returns a 200 response (not an error)
- [ ] Integration test: invalid filter value (e.g., `severity=banana`) returns 400 status
- [ ] Integration test: search results are wrapped in `PaginatedResults` structure with total count

## Verification Commands
- `cargo test --test api search` — All search integration tests pass

## Dependencies
- Depends on: Task 4 — Add response caching for search queries
