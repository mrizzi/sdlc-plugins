# Criterion 2: Response PURLs do not contain `?` query parameters

## Criterion
Response PURLs do not contain `?` query parameters (no qualifiers present).

## Verification

### Service layer implementation
In `modules/fundamental/src/purl/service/mod.rs`, every PURL in the response is processed through `without_qualifiers()` before being serialized via `to_string()`. This method strips all qualifier key-value pairs, which are the portion of a PURL that appears after the `?` character.

### Test assertions
The PR adds explicit assertions for the absence of `?` in multiple test files:

**In `tests/api/purl_recommend.rs` (`test_recommend_purls_basic`):**
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

**In `tests/api/purl_simplify.rs` (`test_simplified_purl_no_version`):**
```rust
assert!(!body.items[0].purl.contains('?'));
```

**In `tests/api/purl_simplify.rs` (`test_simplified_purl_mixed_types`):**
```rust
assert!(!body.items[0].purl.contains("vcs_url"));
```

**In `tests/api/purl_simplify.rs` (`test_simplified_purl_ordering_preserved`):**
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

### Analysis
The code universally applies `without_qualifiers()` in the service layer's mapping step, meaning every PURL returned by the recommend endpoint will have qualifiers stripped. The tests verify this by asserting on the absence of `?` characters. The seeded PURLs in the tests do include qualifiers (e.g., `?repository_url=https://repo1.maven.org&type=jar`), confirming that the stripping happens at the service layer and the response is qualifier-free.

## Result: PASS

The implementation strips qualifiers from all response PURLs, and multiple tests explicitly assert that `?` is not present in the returned PURLs.
