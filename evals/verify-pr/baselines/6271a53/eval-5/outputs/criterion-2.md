## Criterion 2: Response PURLs do not contain ? query parameters (no qualifiers present)

**Verdict: PASS**

### Analysis

The PR ensures that no PURL in the recommendation response contains the `?` character, which is the delimiter for query parameters (qualifiers) in the PURL specification.

The implementation uses `p.without_qualifiers()` in the service layer to strip all qualifier data before constructing the `PurlSummary` response object. Since qualifiers are encoded as query parameters after the `?` in a PURL string, removing qualifiers guarantees the absence of `?` in the output.

### Test Evidence

Multiple tests explicitly assert the absence of `?` in response PURLs:

In `test_recommend_purls_basic`:
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

In `test_simplified_purl_no_version`:
```rust
assert!(!body.items[0].purl.contains('?'));
```

In `test_simplified_purl_ordering_preserved`:
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

The `contains('?')` assertions provide direct verification that qualifier delimiters are absent from every returned PURL. The criterion is satisfied.
