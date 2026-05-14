# Criterion 2: Response PURLs do not contain `?` query parameters

## Acceptance Criterion
Response PURLs do not contain `?` query parameters (no qualifiers present).

## Evidence

### Production Code Changes

In `modules/fundamental/src/purl/service/mod.rs`, the mapping step now calls `p.without_qualifiers()` before serializing to string, which strips all query parameters from the PURL.

### Test Evidence

In `tests/api/purl_recommend.rs`, the updated `test_recommend_purls_basic` includes explicit assertions:
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

These directly verify that the `?` character (which introduces query parameters/qualifiers) is absent from response PURLs.

In `tests/api/purl_simplify.rs`:
- `test_simplified_purl_no_version` asserts: `assert!(!body.items[0].purl.contains('?'));`
- `test_simplified_purl_mixed_types` asserts: `assert!(!body.items[0].purl.contains("vcs_url"));` (checking qualifier key absence)
- `test_simplified_purl_ordering_preserved` asserts: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`

All CI checks pass.

## Verdict: PASS

Multiple tests explicitly assert the absence of `?` in response PURLs, and the production code uses `without_qualifiers()` to guarantee this.
