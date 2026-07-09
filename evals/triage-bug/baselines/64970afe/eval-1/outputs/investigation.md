# Steps 2-3: Codebase Investigation

## Step 2: Search Strategy

The bug reports that plan-feature silently drops conventions when `CONVENTIONS.md` headings have trailing whitespace. The investigation targets:

1. The convention heading extraction logic in the plan-feature skill
2. The convention-aware task enrichment that performs the lookup
3. Existing test coverage for this edge case

## Step 3: Investigation Findings

### Finding 1: Heading extraction does not strip trailing whitespace

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
**Section**: Convention conformance analysis

The heading extraction code:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

The slice `line[3:]` extracts everything after `## ` but does NOT call `.strip()` on the result. When the source line is `## Migration Patterns  \n`, the extracted key becomes `"Migration Patterns  "` (with two trailing spaces).

### Finding 2: Convention lookup uses exact string matching

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
**Section**: Convention-aware task enrichment

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

The `in` check performs an exact-match comparison. When the key stored in `discovered_conventions` is `"Migration Patterns  "` but the expected lookup key is `"Migration Patterns"`, the match fails and the convention is silently skipped. No warning or fallback is emitted.

### Finding 3: Existing tests do not cover trailing whitespace

**File**: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does NOT include trailing whitespace on headings. This edge case is therefore not covered by current evals, which explains why the regression was not caught.

## Root Cause Summary

The `line[3:]` slice in the convention heading extraction does not strip trailing whitespace. This causes convention names to be stored with trailing spaces, which then fail the exact-match lookup during task enrichment. The fix is to call `.strip()` on the extracted heading text (i.e., `line[3:].strip()`). A reproducer test with trailing whitespace on a heading line should be added to confirm the fix.
