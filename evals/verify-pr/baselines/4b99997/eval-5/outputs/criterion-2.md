# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Analysis

The PR ensures qualifiers are stripped by calling `p.without_qualifiers()` in the service layer before serializing the PURL to a string. This removes all query parameters (which follow the `?` character in PURL syntax).

The test file `tests/api/purl_recommend.rs` explicitly validates this with assertions:

```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

These assertions directly verify that no `?` character (and therefore no query parameters/qualifiers) is present in the response PURLs.

The new test file `tests/api/purl_simplify.rs` also validates this across multiple scenarios:
- `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'));`
- `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"));`
- `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`

## Result: PASS

The code removes qualifiers via `without_qualifiers()` and multiple tests explicitly assert that `?` is absent from response PURLs.
