# Criterion 2: Response PURLs do not contain ? query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

The PR ensures qualifiers are stripped by calling `p.without_qualifiers()` in the service layer before constructing the `PurlSummary`. This removes all query parameters from the PURL string representation.

Multiple tests explicitly assert the absence of `?` in the response PURLs:

In `tests/api/purl_recommend.rs`, `test_recommend_purls_basic`:
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

In `tests/api/purl_simplify.rs`, `test_simplified_purl_no_version`:
```rust
assert!(!body.items[0].purl.contains('?'));
```

In `tests/api/purl_simplify.rs`, `test_simplified_purl_mixed_types`:
```rust
assert!(!body.items[0].purl.contains("vcs_url"));
```

In `tests/api/purl_simplify.rs`, `test_simplified_purl_ordering_preserved`:
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

These assertions directly verify that no query parameters (qualifiers) appear in the response PURLs. All CI checks pass.
