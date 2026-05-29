# Criterion 2: Response PURLs do not contain `?` query parameters

## Criterion Text
Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

The PR addresses this criterion through both the implementation and test assertions.

### Implementation

In `modules/fundamental/src/purl/service/mod.rs`, the `without_qualifiers()` method is called on each PURL before serialization:

```rust
let simplified = p.without_qualifiers();
PurlSummary {
    purl: simplified.to_string(),
}
```

The `without_qualifiers()` method (documented in the task's Implementation Notes as part of the `PackageUrl` builder in `common/src/purl.rs`) constructs a PURL without any query parameters. Since qualifiers in PURL syntax are represented as `?key=value&key2=value2` after the version, stripping qualifiers means the resulting string will never contain a `?` character.

### Test Evidence

Multiple tests explicitly assert the absence of `?` in response PURLs:

In `tests/api/purl_recommend.rs`, `test_recommend_purls_basic`:
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

In `tests/api/purl_simplify.rs`, `test_simplified_purl_no_version`:
```rust
assert!(!body.items[0].purl.contains('?'));
```

In `tests/api/purl_simplify.rs`, `test_simplified_purl_mixed_types`:
```rust
assert!(!body.items[0].purl.contains("vcs_url"));
```

In `tests/api/purl_simplify.rs`, `test_simplified_purl_ordering_preserved`:
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

The combination of the `without_qualifiers()` implementation and the explicit `contains('?')` assertions in tests confirms this criterion is satisfied.
