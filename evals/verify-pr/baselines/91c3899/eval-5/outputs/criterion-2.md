# Criterion 2: Response PURLs do not contain `?` query parameters

## Verdict: PASS

## Analysis

The `without_qualifiers()` method strips all qualifier parameters from PURLs, removing any `?key=value` pairs. Tests explicitly verify the absence of the `?` character in returned PURL strings.

### Evidence

Multiple tests assert qualifier absence:

In `tests/api/purl_recommend.rs`:
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

In `tests/api/purl_simplify.rs`:
- `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'));`
- `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"));`
- `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`

The implementation in `modules/fundamental/src/purl/service/mod.rs` uses `p.without_qualifiers()` before `to_string()`, ensuring qualifiers are never included in the response.
