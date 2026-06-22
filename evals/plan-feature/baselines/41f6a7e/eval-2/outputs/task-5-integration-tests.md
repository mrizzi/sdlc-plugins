# Task 5: Update and expand search integration tests

## Repository

trustify-backend

## Target Branch

`main`

## Description

Expand the search integration test suite to cover the new full-text search, relevance ranking, filtering, and caching features introduced in Tasks 1-4. Tests should run against a real PostgreSQL instance following the existing integration test pattern and provide a performance baseline for search queries.

## Files to Modify

- `tests/api/search.rs` -- Add the following test cases:

  **Relevance ranking tests:**
  - `test_search_relevance_ordering` -- Insert entities with varying degrees of term overlap. Search for a multi-word query and assert that results with more term matches rank higher.
  - `test_search_relevance_score_present` -- Verify the `relevance_score` field is present and is a float between 0.0 and 1.0.
  - `test_search_sort_by_relevance` -- Search with `sort_by=relevance` and verify ordering differs from `sort_by=date`.
  - `test_search_sort_by_date` -- Search with `sort_by=date` and verify chronological ordering.
  - `test_search_sort_by_name` -- Search with `sort_by=name` and verify alphabetical ordering.

  **Filter tests:**
  - `test_search_filter_entity_type_single` -- Filter by `entity_type=advisory` and verify only advisories are returned.
  - `test_search_filter_entity_type_multiple` -- Filter by `entity_type=advisory&entity_type=sbom` and verify both types are returned but not packages.
  - `test_search_filter_date_range` -- Insert entities with known dates, filter by `date_from` and `date_to`, verify only entities within the range are returned.
  - `test_search_filter_severity` -- Insert advisories with different severities, filter by `severity=critical`, verify only critical advisories are returned.
  - `test_search_filter_license` -- Insert packages with known licenses, filter by `license=MIT`, verify matching packages are returned.
  - `test_search_filter_combined` -- Apply multiple filters simultaneously and verify AND logic.
  - `test_search_filter_invalid_entity_type` -- Pass an invalid entity type and verify 400 response.
  - `test_search_filter_invalid_date` -- Pass a malformed date and verify 400 response.
  - `test_search_filter_date_range_inverted` -- Pass `date_from > date_to` and verify 400 response.

  **Edge case tests:**
  - `test_search_empty_query` -- Search with an empty `q` parameter and verify empty result set with 200 status.
  - `test_search_special_characters` -- Search with special characters (`@`, `#`, `&`, quotes) and verify no 500 error.
  - `test_search_single_character` -- Search with a single character and verify ILIKE fallback returns results.
  - `test_search_very_long_query` -- Search with a very long query string (1000+ chars) and verify graceful handling.
  - `test_search_no_results` -- Search for a term with no matches and verify empty result set with 200 status.

  **Caching tests:**
  - `test_search_cache_control_header` -- Verify `Cache-Control` header is present with expected directives.
  - `test_search_vary_header` -- Verify `Vary` header includes `Accept` and `Authorization`.

  **Backward compatibility tests:**
  - `test_search_existing_behavior_preserved` -- Replicate the existing test cases to confirm they still pass without modification.
  - `test_search_no_filters_returns_all` -- Search without any filter parameters and verify all entity types are returned.

## Implementation Notes

- Follow the existing test pattern in `tests/api/search.rs`. The existing tests likely use a test helper that sets up a PostgreSQL database, runs migrations, seeds test data, and provides an HTTP client.
- Reuse existing test fixtures and helpers. Check for a `TestContext`, `TestApp`, or similar struct that provides a configured Axum app and database connection.
- For relevance ranking tests, create test entities with carefully chosen content so that expected ranking is deterministic. For example:
  - Entity A: name = "Critical OpenSSL vulnerability in TLS 1.3"
  - Entity B: name = "Package update notification"
  - Entity C: name = "OpenSSL security patch"
  - Search for "openssl vulnerability": A should rank highest (both terms), C second (one term), B should not appear.
- For performance baseline tests, use `std::time::Instant` to measure search latency and assert it is below a reasonable threshold (e.g., < 500ms for 1000 entities). Log the actual timing for PR review.
- Ensure test data is isolated per test to prevent cross-test interference. Use transactions or unique identifiers.

## Acceptance Criteria

- [ ] All new tests pass against a PostgreSQL test database
- [ ] All existing search tests continue to pass without modification
- [ ] Relevance ranking tests demonstrate correct ordering
- [ ] Filter tests cover single, multiple, and combined filter scenarios
- [ ] Edge case tests confirm graceful handling of unusual inputs
- [ ] Cache header tests verify correct HTTP caching configuration
- [ ] No test relies on hardcoded database state outside its own setup

## Verification Commands

```bash
# Run all search tests
cargo test --test search -- --nocapture

# Run only the new relevance tests
cargo test --test search test_search_relevance -- --nocapture

# Run only the filter tests
cargo test --test search test_search_filter -- --nocapture
```

## Dependencies

- Task 1 (search indexes) -- tests require tsvector columns and GIN indexes
- Task 2 (relevance ranking) -- relevance ranking tests exercise the ts_rank functionality
- Task 3 (filter parameters) -- filter tests exercise the new query parameters
- Task 4 (caching) -- cache header tests verify the caching middleware
