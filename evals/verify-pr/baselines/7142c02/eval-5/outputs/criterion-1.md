# Criterion 1: Versioned PURLs without qualifiers

**Acceptance Criterion:** `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

**Verdict: PASS**

## Evidence

### Production code changes

In `modules/fundamental/src/purl/service/mod.rs`, the recommend method now calls `p.without_qualifiers()` on each returned PURL before serialization:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

This strips all qualifiers from the PURL string, producing versioned PURLs like `pkg:maven/org.apache/commons-lang3@3.12` instead of `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`.

Additionally, the qualifier join was removed from the query in the service layer:

```rust
// Removed:
.join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def());
```

And the `sea_orm::JoinType` import was removed from `modules/fundamental/src/purl/endpoints/recommend.rs`.

### Test coverage

In `tests/api/purl_recommend.rs`, the `test_recommend_purls_basic` test now asserts:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This confirms the endpoint returns versioned PURLs without qualifiers. The test seeds PURLs with qualifiers (`?repository_url=...&type=jar`) but the response assertion checks for the version-only form.

### Conclusion

The production code transforms all returned PURLs through `without_qualifiers()`, and the test explicitly asserts the expected format. This criterion is satisfied.
