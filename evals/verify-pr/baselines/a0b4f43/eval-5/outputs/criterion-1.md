# Criterion 1: GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3 returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The PR diff modifies two source files to implement this criterion:

1. **`modules/fundamental/src/purl/endpoints/recommend.rs`**: Removes the `use sea_orm::JoinType;` import, indicating the qualifier join is no longer used in the endpoint layer.

2. **`modules/fundamental/src/purl/service/mod.rs`**: The `recommend` method is updated to:
   - Remove the `.join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def())` call, eliminating the qualifier join from the query.
   - Call `p.without_qualifiers()` on each result item before serialization, producing a `simplified` PURL object.
   - Serialize the simplified PURL with `simplified.to_string()`, which produces versioned PURLs without qualifiers.

3. **Test evidence in `tests/api/purl_recommend.rs`**: The `test_recommend_purls_basic` test now asserts:
   ```rust
   assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
   assert!(!body.items[0].purl.contains('?'));
   assert!(!body.items[1].purl.contains('?'));
   ```
   This confirms the response contains versioned PURLs without qualifier parameters.

The implementation correctly strips qualifiers at both the query layer (no join) and the serialization layer (`without_qualifiers()`), and the test assertions confirm the expected output format.
