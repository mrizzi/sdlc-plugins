# Step 4: Root Cause Analysis

This is the comment that would be posted on Bug ACME-500.

---

## Root Cause

### What is broken

The plan-feature skill's convention conformance analysis extracts `CONVENTIONS.md` section headings using `line[3:]`, which captures everything after the `## ` prefix but does **not** strip trailing whitespace. When a heading line contains trailing spaces (e.g., `## Migration Patterns  `), the extracted section name becomes `"Migration Patterns  "` instead of `"Migration Patterns"`.

The downstream convention-aware task enrichment step performs an exact string match (`if convention_name in discovered_conventions`) against the stored keys. Because the stored key has trailing spaces and the lookup key does not, the match fails silently -- no warning is logged, and the convention is omitted from the generated task description.

### Where it is broken

- **Extraction site**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- convention conformance analysis, specifically the `section_name = line[3:]` assignment.
- **Lookup site**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- convention-aware task enrichment, the `if convention_name in discovered_conventions` check.

### Why it was not caught

The existing eval fixture (`evals/plan-feature/files/conventions-mock.md`) does not include trailing whitespace on any heading lines, so this edge case has no test coverage.

### How to verify the fix

1. Create a reproducer test that uses a `CONVENTIONS.md` fixture with trailing whitespace on a heading line (e.g., `## Migration Patterns  ` with two trailing spaces).
2. Run the plan-feature convention conformance analysis against this fixture.
3. Assert that the generated task's Implementation Notes include the expected convention reference: `Per CONVENTIONS.md "Migration Patterns: add Index::create() for all FK columns.`

### Suggested fix

Apply `.strip()` to the extracted heading text:

```python
section_name = line[3:].strip()
```

This normalizes heading names regardless of trailing whitespace in the source file.
