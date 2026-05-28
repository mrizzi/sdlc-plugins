# Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The PR modifies the service layer in `modules/fundamental/src/purl/service/mod.rs` to strip qualifiers from PURLs before returning them. Specifically:

1. The qualifier join is removed: the line `.join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def())` is deleted from the recommendation query.

2. The response mapping now calls `p.without_qualifiers()` before serializing:
   ```rust
   .map(|p| {
       let simplified = p.without_qualifiers();
       PurlSummary {
           purl: simplified.to_string(),
       }
   })
   ```

3. The `JoinType` import is also removed from `modules/fundamental/src/purl/endpoints/recommend.rs`, confirming qualifiers are no longer joined.

4. The test `test_recommend_purls_basic` confirms this behavior: it seeds PURLs with qualifiers (`?repository_url=...&type=jar`) but asserts the response contains only the versioned PURL without qualifiers:
   ```rust
   assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
   ```

The code changes directly implement this criterion. The endpoint still returns versioned PURLs (with `@version` suffix) but without the `?qualifier=value` suffix.
