# Criterion 1: Versioned PURLs Without Qualifiers

**Criterion:** `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

**Verdict:** PASS

## Reasoning

The PR modifies `modules/fundamental/src/purl/service/mod.rs` to strip qualifiers from the response. The key change is in the `.map()` closure where each PURL result is now processed through `p.without_qualifiers()` before being serialized:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

Previously, the code mapped directly to `p.to_string()` which included all qualifiers. The `without_qualifiers()` method (documented in the task as available on the `PackageUrl` builder in `common/src/purl.rs`) strips qualifier parameters while preserving the version component.

The endpoint handler in `modules/fundamental/src/purl/endpoints/recommend.rs` still calls the same `recommend()` method on `PurlService`, and the return type remains `Json<PaginatedResults<PurlSummary>>`, so the endpoint path and response shape are unchanged.

The test `test_recommend_purls_basic` in the PR version confirms this behavior by asserting:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This is a versioned PURL without qualifiers (no `?` or query parameters), confirming the criterion is met.
