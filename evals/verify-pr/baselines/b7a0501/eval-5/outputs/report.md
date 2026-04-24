# Verification Report: PR #746 -- TC-9105

## Summary

| Field | Value |
|-------|-------|
| **Jira Task** | TC-9105: Simplify PURL recommendation response to exclude qualifiers |
| **PR** | https://github.com/trustify/trustify-backend/pull/746 |
| **Repository** | trustify-backend |
| **Status** | In Review |
| **Parent Feature** | TC-9001 |

---

## Verification Matrix

| # | Check | Result | Details |
|---|-------|--------|---------|
| 1 | PR linked to Jira task | PASS | PR URL is recorded in TC-9105; task status is "In Review" |
| 2 | All files-to-modify are touched | PASS | `recommend.rs` (endpoint), `service/mod.rs` (service), `purl_recommend.rs` (tests) are all modified |
| 3 | All files-to-create are present | PASS | `tests/api/purl_simplify.rs` is created as a new file with 62 lines |
| 4 | No out-of-scope files modified | PASS | Only the 4 files listed in the task (2 production, 2 test) are changed |
| 5 | Test Change Classification | **MIXED** | See detailed analysis below |
| 6 | CI status | N/A | Cannot verify CI from fixture data; PR is in review |

---

## Acceptance Criteria Verification

| # | Criterion | Verdict | Evidence |
|---|-----------|---------|----------|
| 1 | `GET /api/v2/purl/recommend` returns versioned PURLs without qualifiers | PASS | Service layer calls `without_qualifiers()` on every PURL; `test_recommend_purls_basic` asserts versioned PURL without qualifiers |
| 2 | Response PURLs do not contain `?` query parameters | PASS | Multiple tests assert `!purl.contains('?')`; structural prevention via `without_qualifiers()` |
| 3 | Duplicate entries are deduplicated after qualifier removal | PASS | `.dedup_by(|a, b| a.purl == b.purl)` added in service; `test_recommend_purls_dedup` verifies 2 qualifier-variants collapse to 1 |
| 4 | Existing pagination and sorting behavior is preserved | PASS | `test_recommend_purls_pagination` unchanged from base; new `test_simplified_purl_ordering_preserved` confirms pagination with qualifier removal |
| 5 | Response shape is unchanged (`PaginatedResults<PurlSummary>`) | PASS | Endpoint return type unchanged; all 7 tests deserialize as `PaginatedResults<PurlSummary>` |

---

## Test Requirements Verification

| # | Requirement | Verdict | Evidence |
|---|-------------|---------|----------|
| 1 | Update `test_recommend_purls_basic` to assert versioned PURL without qualifiers | PASS | Assertion changed from fully qualified PURL to `"pkg:maven/org.apache/commons-lang3@3.12"` |
| 2 | Remove `test_recommend_purls_with_qualifiers` | PASS | Function entirely deleted in diff |
| 3 | Add `test_recommend_purls_dedup` for deduplication verification | PASS | New function added, asserts 2 qualifier-variants yield 1 result |
| 4 | Add `tests/api/purl_simplify.rs` with edge case tests | PASS | New file with 3 tests: no-version, mixed-types, ordering-preserved |

---

## Test Change Classification: MIXED

### Classification Rationale

This PR contains BOTH additive and reductive test changes, resulting in a **MIXED** classification.

### Reductive Signals

1. **`test_recommend_purls_with_qualifiers` REMOVED**: This function existed in the base branch (verifying that qualifier variants were returned as separate entries) and is entirely deleted in the PR. This is intentional -- the behavior it tested no longer exists after the qualifier removal change.

2. **Assertion in `test_recommend_purls_basic` RELAXED**: The base branch assertion checked for a fully qualified PURL string including `?repository_url=https://repo1.maven.org&type=jar`. The PR changes this to check only the versioned PURL `"pkg:maven/org.apache/commons-lang3@3.12"`. While the PR adds compensating `contains('?')` negative assertions, the primary equality check validates a less-specific string. This is intentional -- it matches the new simplified response format.

### Additive Signals

1. **`test_recommend_purls_dedup` is NEW**: Added to the existing `tests/api/purl_recommend.rs` file. It verifies that two PURLs differing only by qualifiers are deduplicated into one entry after qualifier removal.

2. **`tests/api/purl_simplify.rs` is an ENTIRELY NEW file** with 3 new test functions:
   - `test_simplified_purl_no_version` -- edge case: PURLs without version
   - `test_simplified_purl_mixed_types` -- edge case: PURLs across different ecosystems (npm, pypi)
   - `test_simplified_purl_ordering_preserved` -- confirms ordering and pagination after qualifier removal

### Net Impact

| Metric | Base | PR | Delta |
|--------|------|----|-------|
| Test functions in `purl_recommend.rs` | 4 | 4 | 0 (1 removed, 1 added) |
| Test functions in `purl_simplify.rs` | 0 | 3 | +3 |
| **Total test functions** | **4** | **7** | **+3** |

The reductive changes are justified by the intentional behavioral change (removing qualifier support from the recommendation endpoint). The additive changes provide comprehensive coverage of the new simplified behavior. The net test count increases from 4 to 7.

---

## Production Code Changes Summary

1. **`modules/fundamental/src/purl/endpoints/recommend.rs`**: Removed `sea_orm::JoinType` import (no longer needed since qualifier join is removed).

2. **`modules/fundamental/src/purl/service/mod.rs`**:
   - Removed `.join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def())` from the recommendation query
   - Added `.group_by(purl::Column::Id)` to the count query for accurate totals
   - Added `.map(|p| { let simplified = p.without_qualifiers(); ... })` to strip qualifiers from response PURLs
   - Added `.dedup_by(|a, b| a.purl == b.purl)` to eliminate duplicates after qualifier removal

---

## Overall Verdict: PASS

All 5 acceptance criteria are satisfied. All 4 test requirements are met. The test change classification is MIXED (both additive and reductive signals present), with reductive changes justified by the intentional behavioral change. The net test coverage increases by 3 functions. No out-of-scope files are modified.
