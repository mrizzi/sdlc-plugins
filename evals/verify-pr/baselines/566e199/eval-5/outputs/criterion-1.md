# Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Analysis

The PR modifies `modules/fundamental/src/purl/service/mod.rs` to strip qualifiers from the recommendation response. Specifically:

1. The qualifier join is removed: the line `.join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def())` is deleted.
2. The mapping logic is updated: instead of `p.to_string()` (which included qualifiers), the code now calls `p.without_qualifiers()` and then `.to_string()` on the simplified PURL.

The `without_qualifiers()` method is referenced in the task's Implementation Notes as an existing method on the `PackageUrl` builder in `common/src/purl.rs` that constructs PURLs without qualifiers.

The test `test_recommend_purls_basic` in `tests/api/purl_recommend.rs` confirms this behavior:
- Seeds PURLs with qualifiers (`?repository_url=...&type=jar`)
- Requests recommendations via `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3`
- Asserts the response contains `pkg:maven/org.apache/commons-lang3@3.12` (versioned, no qualifiers)

The endpoint path in the diff matches the acceptance criterion's endpoint exactly. The code change directly implements the qualifier removal behavior described.
