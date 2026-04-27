# Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Analysis

The PR modifies `modules/fundamental/src/purl/service/mod.rs` to strip qualifiers from returned PURLs. The key change is in the `.map()` closure:

```rust
// Before (base branch):
.map(|p| PurlSummary {
    purl: p.to_string(),
})

// After (PR branch):
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

The `without_qualifiers()` method is called on each PURL before converting to string, which strips qualifier parameters from the output.

Additionally, the endpoint file `modules/fundamental/src/purl/endpoints/recommend.rs` removes the `use sea_orm::JoinType;` import since the qualifier join is no longer needed.

The test `test_recommend_purls_basic` confirms this behavior by asserting:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This shows a versioned PURL without qualifiers is returned.

## Result: PASS

The code changes clearly implement qualifier stripping via `without_qualifiers()` and the test validates that the endpoint returns versioned PURLs without qualifier parameters.
