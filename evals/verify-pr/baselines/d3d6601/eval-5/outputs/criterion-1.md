# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Criterion Text
`GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers.

## Verdict: PASS

## Reasoning

The PR modifies `modules/fundamental/src/purl/service/mod.rs` to strip qualifiers from PURLs before returning them. The key change is in the `recommend` method:

1. The qualifier join is removed: the line `.join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def())` is deleted, so qualifiers are no longer fetched from the database.

2. The PURL serialization is changed to use `without_qualifiers()`:
   ```rust
   .map(|p| {
       let simplified = p.without_qualifiers();
       PurlSummary {
           purl: simplified.to_string(),
       }
   })
   ```

   Previously, it was:
   ```rust
   .map(|p| PurlSummary {
       purl: p.to_string(),
   })
   ```

3. The test `test_recommend_purls_basic` in `tests/api/purl_recommend.rs` confirms the behavior change. It seeds PURLs with qualifiers (`?repository_url=...&type=jar`) but asserts that the response contains versioned PURLs without qualifiers:
   ```rust
   assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
   ```

The endpoint path `GET /api/v2/purl/recommend` is unchanged (the `recommend.rs` endpoint file still serves this route). The code changes ensure that any PURL returned by this endpoint has qualifiers stripped via `without_qualifiers()`.

This criterion is satisfied by the implementation.
