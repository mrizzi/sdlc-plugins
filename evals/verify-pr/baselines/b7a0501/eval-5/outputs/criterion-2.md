# Criterion 2: Response PURLs do not contain `?` query parameters

## Acceptance Criterion
Response PURLs do not contain `?` query parameters (no qualifiers present).

## Verdict: PASS

## Reasoning

The PR explicitly adds assertions in multiple test functions to verify that no `?` character appears in response PURLs, confirming no qualifiers leak through.

### Test Evidence

1. **`test_recommend_purls_basic`** (modified in `tests/api/purl_recommend.rs`):
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

2. **`test_simplified_purl_no_version`** (new in `tests/api/purl_simplify.rs`):
```rust
assert!(!body.items[0].purl.contains('?'));
```

3. **`test_simplified_purl_mixed_types`** (new in `tests/api/purl_simplify.rs`):
```rust
assert!(!body.items[0].purl.contains("vcs_url"));
```

4. **`test_simplified_purl_ordering_preserved`** (new in `tests/api/purl_simplify.rs`):
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

### Production Code

The `without_qualifiers()` method is called on every PURL before serialization in the service layer, structurally preventing qualifier parameters from appearing in the response.
