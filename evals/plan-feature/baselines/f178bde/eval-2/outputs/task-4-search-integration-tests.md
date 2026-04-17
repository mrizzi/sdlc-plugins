# Task 4 — Add integration tests for search improvements

## Repository
trustify-backend

## Description
Add comprehensive integration tests covering the search improvements introduced
by Tasks 1-3: performance-related index usage, full-text ranking behavior, and
filter parameters. This task also verifies backward compatibility of the existing
search endpoint contract.

**Ambiguity note:** Because the feature provides no quantitative performance
targets ("should be fast enough"), this task cannot include performance assertion
tests (e.g., "search completes in under 200ms"). Tests will verify functional
correctness only. If performance SLAs are defined later, additional benchmark
tests should be added.

## Files to Modify
- `tests/api/search.rs` — Add new integration test cases for ranking, filtering, and backward compatibility

## Implementation Notes
- Follow the existing test pattern in `tests/api/search.rs` which uses `assert_eq!(resp.status(), StatusCode::OK)` and hits a real PostgreSQL test database
- Also reference test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs` for consistency with the project's integration test style
- Test data setup should create entities across multiple types (SBOMs, advisories, packages) with known text content to verify ranking and filtering behavior
- Per constraints doc section 5.9-5.13: prefer parameterized tests when multiple test cases exercise the same behavior with different inputs; add doc comments to every test function; add given-when-then inline comments to non-trivial tests
- **Ambiguity:** Without defined performance targets, tests can only verify functional behavior (correct results, correct ordering, correct filtering). If the stakeholder later defines latency SLAs, benchmark tests should be added as a follow-up

## Reuse Candidates
- `tests/api/search.rs` — Existing search integration tests; extend with new test cases following the same patterns
- `tests/api/sbom.rs` — Integration test patterns for reference (test setup, assertion style)
- `tests/api/advisory.rs` — Integration test patterns for reference

## Acceptance Criteria
- [ ] Integration tests verify that search results are ranked by relevance (best match first)
- [ ] Integration tests verify that entity-type filter returns only the requested entity type
- [ ] Integration tests verify backward compatibility (unfiltered search returns all types)
- [ ] All new tests pass against a PostgreSQL test database
- [ ] All existing tests continue to pass

## Test Requirements
- [ ] Test: search with a specific term returns the most relevant result first
- [ ] Test: search with `type=sbom` returns only SBOM entities
- [ ] Test: search with `type=advisory` returns only advisory entities
- [ ] Test: search without type filter returns mixed entity types
- [ ] Test: search with invalid type filter returns error
- [ ] Test: existing search queries return the same result set (order may differ due to ranking)

## Verification Commands
- `cargo test --test search` — all search integration tests pass
- `cargo test` — full test suite passes (no regressions)

## Dependencies
- Depends on: Task 2 — Improve search result ranking with full-text scoring
- Depends on: Task 3 — Add filtering parameters to search endpoint
