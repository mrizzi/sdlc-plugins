## Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

**Verdict: PASS**

### Analysis

The PR modifies the service layer in `modules/fundamental/src/purl/service/mod.rs` to strip qualifiers from PURLs before returning them. The relevant change is:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

Previously, the code serialized the full PURL including qualifiers:

```rust
.map(|p| PurlSummary {
    purl: p.to_string(),
})
```

The `without_qualifiers()` method is called on each PURL entity before serialization, ensuring that the response contains only versioned PURLs (e.g., `pkg:maven/org.apache/commons-lang3@3.12`) without qualifier parameters.

### Test Evidence

The test `test_recommend_purls_basic` seeds PURLs with qualifiers (`?repository_url=...&type=jar`) and asserts that the response contains the versioned form without qualifiers:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

Additionally, the new test file `tests/api/purl_simplify.rs` includes `test_simplified_purl_mixed_types` which verifies qualifier stripping for npm PURLs:

```rust
assert_eq!(body.items[0].purl, "pkg:npm/%40angular/core@16.0.0");
assert!(!body.items[0].purl.contains("vcs_url"));
```

The criterion is satisfied by both the implementation change and corresponding test assertions.
