# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The PR modifies the `recommend` method in `modules/fundamental/src/purl/service/mod.rs` to strip qualifiers from PURLs before returning them. Specifically:

1. The qualifier join is removed: the line `.join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def())` is deleted, and the `use sea_orm::JoinType;` import is removed from `recommend.rs`.

2. The mapping logic is changed from:
   ```rust
   .map(|p| PurlSummary {
       purl: p.to_string(),
   })
   ```
   to:
   ```rust
   .map(|p| {
       let simplified = p.without_qualifiers();
       PurlSummary {
           purl: simplified.to_string(),
       }
   })
   ```

3. The `without_qualifiers()` method is called on each PURL before converting to string, which strips qualifier parameters.

4. The test `test_recommend_purls_basic` in the PR asserts:
   ```rust
   assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
   ```
   This confirms the response contains a versioned PURL without qualifiers (no `?` query string).

The code change directly implements this criterion by using the `without_qualifiers()` method on the `PackageUrl` builder as described in the Implementation Notes.
