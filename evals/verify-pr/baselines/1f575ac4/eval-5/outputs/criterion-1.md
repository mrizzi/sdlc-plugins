# Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The implementation satisfies this criterion through two changes:

1. **Service layer (`modules/fundamental/src/purl/service/mod.rs`):** The `recommend` method now calls `p.without_qualifiers()` on each PURL result before constructing the `PurlSummary`. This strips qualifier parameters, producing versioned PURLs like `pkg:maven/org.apache/commons-lang3@3.12` instead of `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`.

2. **Endpoint layer (`modules/fundamental/src/purl/endpoints/recommend.rs`):** The `JoinType` import for `sea_orm::JoinType` was removed since the qualifier join is no longer needed. The endpoint handler itself is structurally unchanged -- it still delegates to `PurlService::recommend()` and wraps the result in `Json`.

3. **Test validation:** `test_recommend_purls_basic` in `tests/api/purl_recommend.rs` explicitly asserts that the response contains `"pkg:maven/org.apache/commons-lang3@3.12"` (version only, no qualifiers). The new test file `tests/api/purl_simplify.rs` further validates this for multiple PURL types (Maven, npm, pypi).

The code change directly implements the criterion: the endpoint returns versioned PURLs without qualifiers.
