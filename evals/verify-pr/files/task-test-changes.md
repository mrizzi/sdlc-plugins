<!-- SYNTHETIC TEST DATA — mock Jira task description for eval testing; names, URLs, and identifiers are fictional -->

# Jira Task: TC-9105

**Key**: TC-9105
**Summary**: Simplify PURL recommendation response to exclude qualifiers
**Status**: In Review
**Labels**: ai-generated-jira
**PR URL**: https://github.com/trustify/trustify-backend/pull/746
**Web URL**: https://redhat.atlassian.net/browse/TC-9105
**Parent Feature**: TC-9001

---

## Repository
trustify-backend

## Description
Simplify the PURL recommendation response by removing qualifier details from the returned package identifiers. Currently, the `GET /api/v2/purl/recommend` endpoint returns fully qualified PURLs including `repository_url`, `type`, and other qualifiers. After this change, the endpoint returns versioned PURLs without qualifiers (e.g., `pkg:maven/org.apache/commons-lang3@3.12` instead of `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`). This reduces response payload size and simplifies client consumption. Existing tests for qualifier-specific behavior are removed since qualifiers are no longer part of the response.

## Files to Modify
- `modules/fundamental/src/purl/endpoints/recommend.rs` — remove qualifier inclusion from PURL serialization
- `modules/fundamental/src/purl/service/mod.rs` — update recommendation query to skip qualifier joins
- `tests/api/purl_recommend.rs` — update existing tests to match simplified response format

## Files to Create
- `tests/api/purl_simplify.rs` — new integration tests for the simplified response format

## Implementation Notes
- Follow the existing PURL endpoint patterns in `modules/fundamental/src/purl/endpoints/`
- The `PackageUrl` builder in `common/src/purl.rs` supports constructing PURLs with or without qualifiers — use the `without_qualifiers()` method
- Remove the qualifier join from the recommendation query in the service layer; the join was only needed for qualifier inclusion in the response
- Update the existing `test_recommend_purls_basic` assertion to check for versioned PURL without qualifiers
- Remove the `test_recommend_purls_with_qualifiers` test function entirely — qualifier-specific behavior no longer exists
- Add a deduplication test to the existing test file since removing qualifiers may surface duplicate entries that were previously distinct due to different qualifiers

## Acceptance Criteria
- [ ] `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers
- [ ] Response PURLs do not contain `?` query parameters (no qualifiers present)
- [ ] Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response
- [ ] Existing pagination and sorting behavior is preserved
- [ ] Response shape is unchanged (still `PaginatedResults<PurlSummary>`)

## Test Requirements
- [ ] Update `test_recommend_purls_basic` to assert versioned PURL without qualifiers
- [ ] Remove `test_recommend_purls_with_qualifiers` (no longer applicable)
- [ ] Add `test_recommend_purls_dedup` to verify deduplication after qualifier removal
- [ ] Add new test file `tests/api/purl_simplify.rs` with tests for simplified format edge cases
