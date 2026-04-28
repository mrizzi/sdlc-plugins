# Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The PR modifies the PURL recommendation endpoint to strip qualifiers from the response.

### Evidence from the diff

**Service layer change (`modules/fundamental/src/purl/service/mod.rs`):**

The `recommend` method was updated to:
1. Remove the `JoinType::LeftJoin` on `purl::Relation::PurlQualifier` -- qualifiers are no longer joined in the query.
2. Apply `.without_qualifiers()` on each PURL result before constructing the `PurlSummary`:
   ```rust
   .map(|p| {
       let simplified = p.without_qualifiers();
       PurlSummary {
           purl: simplified.to_string(),
       }
   })
   ```

**Endpoint layer change (`modules/fundamental/src/purl/endpoints/recommend.rs`):**

The `JoinType` import was removed (no longer needed), confirming qualifier joins are fully eliminated from the endpoint path.

**Test confirmation (`tests/api/purl_recommend.rs`):**

The `test_recommend_purls_basic` test now asserts:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This confirms the endpoint returns versioned PURLs (with `@3.12`) without qualifiers (no `?repository_url=...&type=jar`).

The new test file `tests/api/purl_simplify.rs` further confirms this behavior across multiple PURL types (Maven, npm, pypi).

### Conclusion

The code changes demonstrate that `GET /api/v2/purl/recommend` now returns versioned PURLs without qualifiers. The qualifier join is removed, `without_qualifiers()` is called on each result, and tests assert the simplified format. This criterion is satisfied.
