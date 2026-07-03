# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

The code change in `modules/fundamental/src/purl/service/mod.rs` applies `without_qualifiers()` to every PURL before including it in the response. Since qualifiers in PURL syntax are appended after a `?` character (e.g., `?repository_url=...&type=jar`), stripping qualifiers guarantees no `?` appears in the returned PURL strings.

Multiple tests in the PR explicitly verify this invariant:

In `tests/api/purl_recommend.rs`, the updated `test_recommend_purls_basic` function includes:
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

In `tests/api/purl_simplify.rs`, three separate test functions verify the absence of `?`:
- `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'));`
- `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"));` (checks a specific qualifier key is absent)
- `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`

The combination of the `without_qualifiers()` call in the service layer and the explicit `contains('?')` assertions in tests confirms that response PURLs will not contain query parameters.
