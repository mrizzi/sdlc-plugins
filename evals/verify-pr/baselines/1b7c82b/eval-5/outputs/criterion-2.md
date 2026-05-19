# Criterion 2: Response PURLs do not contain `?` query parameters

## Criterion Text
Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

This criterion is closely related to Criterion 1 but focuses specifically on the absence of the `?` character in response PURLs, confirming no qualifiers are appended.

### Code evidence

The service layer change in `modules/fundamental/src/purl/service/mod.rs` calls `p.without_qualifiers()` before serialization. This method produces a PURL string that omits the qualifier portion (everything after `?` in the standard PURL format). Since qualifiers are the only component that introduces a `?` character in a PURL string, calling `without_qualifiers()` guarantees the resulting string contains no `?`.

### Test evidence

Multiple tests explicitly verify the absence of `?`:

**In `tests/api/purl_recommend.rs` (modified):**
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

These assertions were added to `test_recommend_purls_basic` to explicitly verify that no qualifier separator appears in any response PURL.

**In `tests/api/purl_simplify.rs` (new):**
```rust
// test_simplified_purl_no_version:
assert!(!body.items[0].purl.contains('?'));

// test_simplified_purl_mixed_types:
assert!(!body.items[0].purl.contains("vcs_url"));

// test_simplified_purl_ordering_preserved:
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

The tests cover multiple PURL types (maven, npm, pypi) and multiple scenarios (with version, without version, with pagination), all asserting the absence of qualifier characters.

The combination of the `without_qualifiers()` call in the service layer and the explicit `contains('?')` assertions in multiple tests confirms this criterion is fully satisfied.
