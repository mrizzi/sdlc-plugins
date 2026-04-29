# Criterion 2: Response PURLs do not contain ? query parameters

## Criterion Text
> Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Detailed Reasoning

### Code Implementation

This criterion is satisfied by the same `without_qualifiers()` call analyzed in Criterion 1. The `PackageUrl::without_qualifiers()` method (referenced in the task's Implementation Notes as existing in `common/src/purl.rs`) constructs a new PURL containing only the scheme, type, namespace, name, and version -- omitting the qualifier portion entirely.

Since PURL qualifiers are encoded as query parameters after a `?` character (per the PURL specification), calling `without_qualifiers()` guarantees that no `?` appears in the resulting string.

### Test Evidence

The updated `test_recommend_purls_basic` test explicitly asserts the absence of `?`:

```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

These are direct character-level checks ensuring no qualifier separator exists in the response PURLs. Both items in the response are verified.

Additional tests in `purl_simplify.rs` reinforce this:

- `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'));`
- `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"));` (checks that a specific qualifier key is absent)
- `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`

### Coverage Across PURL Types

The test suite covers multiple PURL types:
- Maven PURLs with `repository_url` and `type` qualifiers
- npm PURLs with `vcs_url` qualifier
- PURLs without any version (namespace/name only)

All tests confirm that qualifiers are stripped from the response regardless of PURL type or original qualifier content.

### Conclusion

The `without_qualifiers()` call in the service layer structurally prevents `?` from appearing in response PURLs, and multiple tests across both test files verify this with explicit `contains('?')` assertions. This criterion is fully satisfied.
