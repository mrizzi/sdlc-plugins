# Root Cause Analysis: ACME-500

## Root Cause

The convention heading extraction in the plan-feature skill uses `line[3:]` to extract the heading text after `## `, but does not call `.strip()` on the result. When a `CONVENTIONS.md` heading has trailing whitespace (e.g., `## Migration Patterns  `), the extracted section name becomes `"Migration Patterns  "` (with trailing spaces). The downstream convention-aware task enrichment performs an exact-match lookup using `"Migration Patterns"` (without trailing spaces), which fails silently. No warning or error is emitted, so the convention is dropped without any indication.

## Affected Files

- **`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`** -- Convention conformance analysis: `section_name = line[3:]` does not strip trailing whitespace
- **`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`** -- Convention-aware task enrichment: exact-match lookup `convention_name in discovered_conventions` fails when key has trailing whitespace

## Suggested Approach

Add a `.strip()` call to the heading extraction line so that trailing (and leading) whitespace is removed from the section name:

```python
section_name = line[3:].strip()
```

This ensures that headings with trailing whitespace are normalized before being stored as dictionary keys, so downstream exact-match lookups succeed regardless of whitespace in the source file.

## Reproducer Strategy

Create a test `CONVENTIONS.md` with trailing whitespace on a heading (e.g., `## Migration Patterns  ` with two trailing spaces). Run the convention extraction logic and assert that the convention **is** included in the generated task output. This test should:

1. **Fail before the fix** -- confirming the bug is reproduced
2. **Pass after the fix** -- confirming the fix resolves the issue

Additionally, verify that existing tests continue to pass (no regression from the `.strip()` addition).
