# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

The implementation strips qualifiers at the service layer using the `without_qualifiers()` method on the `PackageUrl` builder (referenced in the task's Implementation Notes as existing in `common/src/purl.rs`). Since `without_qualifiers()` produces a PURL without any qualifier component, the resulting string will not contain the `?` separator that introduces qualifiers in the PURL specification.

Multiple tests explicitly verify the absence of the `?` character in response PURLs:

In `tests/api/purl_recommend.rs`, `test_recommend_purls_basic`:
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

In `tests/api/purl_simplify.rs`:
- `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'));`
- `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"));`
- `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`

These negative assertions directly verify that no qualifier parameters appear in the response PURLs.

## Evidence

- `tests/api/purl_recommend.rs`: Two `contains('?')` negative assertions in `test_recommend_purls_basic`
- `tests/api/purl_simplify.rs`: Additional negative assertions across three test functions
- `modules/fundamental/src/purl/service/mod.rs`: `p.without_qualifiers()` call ensures qualifier stripping at the data layer
- CI: All checks pass
