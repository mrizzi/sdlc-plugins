# Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The PR modifies the service layer in `modules/fundamental/src/purl/service/mod.rs` to strip qualifiers from PURLs before returning them. Specifically:

1. **Qualifier join removed:** The `JoinType::LeftJoin` on `purl::Relation::PurlQualifier` has been removed from the query, so qualifier data is no longer fetched from the database.

2. **`without_qualifiers()` applied:** The code now calls `p.without_qualifiers()` on each PURL entity before serializing it to a string. This strips any qualifier information, producing versioned PURLs like `pkg:maven/org.apache/commons-lang3@3.12` instead of `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`.

3. **Test verification:** The updated `test_recommend_purls_basic` test in `tests/api/purl_recommend.rs` asserts:
   - `assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12")` -- confirms versioned PURL without qualifiers
   - `assert!(!body.items[0].purl.contains('?'))` -- confirms no query parameters
   - `assert!(!body.items[1].purl.contains('?'))` -- confirms for second item as well

4. **New test file:** `tests/api/purl_simplify.rs` contains additional edge-case tests (`test_simplified_purl_no_version`, `test_simplified_purl_mixed_types`, `test_simplified_purl_ordering_preserved`) that all verify PURLs are returned without qualifiers.

The endpoint handler in `recommend.rs` still returns `Json<PaginatedResults<PurlSummary>>`, and the service method now produces simplified PURLs. The code change directly implements this criterion.
