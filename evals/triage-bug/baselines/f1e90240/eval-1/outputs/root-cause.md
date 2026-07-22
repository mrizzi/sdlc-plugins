# Root Cause Analysis: ACME-500

## Root Cause

The plan-feature skill's convention extraction code uses `line[3:]` to extract section headings from `CONVENTIONS.md`, which preserves any trailing whitespace present on the heading line. When the heading line is `## Migration Patterns  ` (with trailing spaces), the extracted key becomes `"Migration Patterns  "`. Downstream, the convention-aware task enrichment step looks up conventions by their clean name (`"Migration Patterns"`), which does not match the whitespace-padded key. The convention is silently dropped with no warning logged.

## Affected Files

- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- Convention conformance analysis section: the `line[3:]` extraction does not call `.strip()` on the heading text, causing whitespace-polluted dictionary keys.
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- Convention-aware task enrichment section: the exact-match lookup (`if convention_name in discovered_conventions`) fails silently when keys contain trailing whitespace.
- `evals/plan-feature/files/conventions-mock.md` -- Existing eval fixture does not include trailing whitespace on headings, so this edge case has no test coverage.

## Suggested Approach

1. **Fix the extraction**: Apply `.strip()` to the heading text after slicing:
   ```python
   section_name = line[3:].strip()
   ```
   This normalizes all heading keys regardless of trailing whitespace in the source file.

2. **Add a warning for unmatched conventions**: In the task enrichment step, log a warning when a convention name is expected but not found in `discovered_conventions`. This prevents silent failures for any future edge cases.

3. **Add eval coverage**: Create a new eval fixture (or extend `conventions-mock.md`) that includes headings with trailing whitespace, and verify that conventions are still matched and included in the generated task output.

## Reproducer Strategy

1. Create a `CONVENTIONS.md` file where at least one `##` heading has trailing whitespace (e.g., `## Migration Patterns  ` with two trailing spaces).
2. Run `/plan-feature` against a feature that should trigger that convention.
3. **Before fix**: Verify the generated task's Implementation Notes do NOT include the convention reference -- confirming the bug.
4. **After fix**: Verify the generated task's Implementation Notes DO include the convention reference (e.g., `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`).
