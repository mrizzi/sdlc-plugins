# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

The `without_qualifiers()` method called in the service layer strips all qualifier parameters from PURLs before they are serialized into the response. Since qualifiers are appended after a `?` character in PURL syntax, removing qualifiers eliminates the `?` and everything after it.

**Evidence from tests:**

Multiple test assertions explicitly verify the absence of `?` in response PURLs:

- `tests/api/purl_recommend.rs`, `test_recommend_purls_basic`:
  - `assert!(!body.items[0].purl.contains('?'));`
  - `assert!(!body.items[1].purl.contains('?'));`

- `tests/api/purl_simplify.rs`, `test_simplified_purl_no_version`:
  - `assert!(!body.items[0].purl.contains('?'));`

- `tests/api/purl_simplify.rs`, `test_simplified_purl_mixed_types`:
  - `assert!(!body.items[0].purl.contains("vcs_url"));`

- `tests/api/purl_simplify.rs`, `test_simplified_purl_ordering_preserved`:
  - `assert!(!body.items[0].purl.contains('?'));`
  - `assert!(!body.items[1].purl.contains('?'));`

**Evidence from implementation:**

In `modules/fundamental/src/purl/service/mod.rs`, the map closure calls `p.without_qualifiers()` before serialization, ensuring no PURL in the response can contain qualifier parameters. All CI checks pass, confirming these assertions succeed.
