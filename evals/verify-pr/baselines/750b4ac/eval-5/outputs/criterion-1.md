# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Criterion Text

`GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers.

## Verdict: PASS

## Reasoning

The PR modifies `modules/fundamental/src/purl/service/mod.rs` to strip qualifiers from the PURL before serialization. Specifically, the `.map()` closure now calls `p.without_qualifiers()` on each result before constructing the `PurlSummary`:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

Previously, the code directly serialized the full PURL including qualifiers:

```rust
.map(|p| PurlSummary {
    purl: p.to_string(),
})
```

The endpoint handler in `recommend.rs` continues to call the same `PurlService::recommend()` method, so the qualifier stripping applies to all responses from this endpoint.

The updated test `test_recommend_purls_basic` confirms the expected behavior by asserting:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This shows a versioned PURL without qualifiers is returned. The new test file `purl_simplify.rs` further validates this across multiple PURL types (maven, npm, pypi).

This criterion is satisfied by the code changes.
