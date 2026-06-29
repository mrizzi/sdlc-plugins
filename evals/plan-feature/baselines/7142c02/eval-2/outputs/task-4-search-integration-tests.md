## Repository
trustify-backend

## Target Branch
main

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": "Normal", "fixVersions": ["RHTPA 1.6.0"]}

## Description
Add comprehensive integration tests for the improved search functionality covering performance regression detection, relevance scoring validation, filter combinations, and edge cases. While Tasks 1-3 include basic test requirements for their specific changes, this task adds end-to-end integration tests that verify the complete search improvement works cohesively and establishes a test baseline for ongoing search quality.

**Assumption (pending clarification):** Without quantitative performance targets from the feature description, performance-related tests can only verify that search completes within a reasonable timeout, not that a specific latency SLA is met. If performance targets are established, the timeout thresholds in these tests should be updated accordingly.

## Files to Modify
- `tests/api/search.rs` — Add new integration test cases covering the full search improvement suite: relevance ordering, filter combinations, edge cases, and backward compatibility with existing search behavior.

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/search.rs` — tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` for status assertions.
- Also reference patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs` for test structure, test data setup, and assertion patterns.
- Tests should set up known test data (SBOMs, advisories, packages with predictable names and properties) so assertions about ranking and filtering are deterministic.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/search.rs` matching the convention's test file scope.
- Per CONVENTIONS.md §Error handling: verify that error responses use the `AppError` enum from `common/src/error.rs`. Applies: task modifies `tests/api/search.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests. Follow the same test setup, request building, and assertion patterns.
- `tests/api/advisory.rs` — existing advisory endpoint integration tests. Follow the same patterns for test data creation.
- `common/src/model/paginated.rs::PaginatedResults<T>` — response structure to deserialize in test assertions.

## Acceptance Criteria
- [ ] All new integration tests pass against a PostgreSQL test database
- [ ] Tests cover relevance scoring: a name match ranks above a description-only match
- [ ] Tests cover each filter dimension individually (entity_type, severity, date range)
- [ ] Tests cover filter combinations (multiple filters applied simultaneously)
- [ ] Tests cover edge cases: empty query, special characters, no results, very long query strings
- [ ] Tests verify backward compatibility: existing search behavior is preserved when no new parameters are provided
- [ ] Tests verify error handling: invalid filter values return appropriate error responses

## Test Requirements
- [ ] End-to-end test: search with a query matching multiple entity types, verify relevance ordering
- [ ] End-to-end test: search with entity_type filter, verify only matching types returned
- [ ] End-to-end test: search with severity filter on advisories, verify correct filtering
- [ ] End-to-end test: search with date range, verify only results within range
- [ ] End-to-end test: search with all filters combined (query + entity_type + severity + date range)
- [ ] Edge case test: empty search query returns results without error
- [ ] Edge case test: search query with special characters (quotes, backslash, SQL keywords) handled safely
- [ ] Edge case test: no matching results returns empty paginated response (not an error)
- [ ] Edge case test: date_from after date_to returns empty results or 400 error
- [ ] Backward compatibility test: `GET /api/v2/search?q=term` without new parameters works as before

## Verification Commands
- `cargo test -p tests --test search` — all search integration tests pass

## Dependencies
- Depends on: Task 3 — Add search filter parameters (all search features must be implemented before comprehensive integration tests)

[sdlc-workflow] Description digest: sha256-md:425e76a53fdabe1e6c3a7ede6b79980a3d1fbd97fe4add04320b08f5c35e1ffd
