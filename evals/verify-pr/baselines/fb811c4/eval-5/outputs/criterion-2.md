# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Analysis

The `without_qualifiers()` method strips all qualifier parameters from PURLs before serialization. Multiple test assertions confirm that the `?` character (which precedes query parameters in PURLs) is absent from response PURLs.

## Evidence

In `tests/api/purl_recommend.rs` (`test_recommend_purls_basic`):
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

In `tests/api/purl_simplify.rs` (`test_simplified_purl_no_version`):
```rust
assert!(!body.items[0].purl.contains('?'));
```

In `tests/api/purl_simplify.rs` (`test_simplified_purl_mixed_types`):
```rust
assert!(!body.items[0].purl.contains("vcs_url"));
```

In `tests/api/purl_simplify.rs` (`test_simplified_purl_ordering_preserved`):
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

All test assertions confirm qualifiers are stripped from the response.
