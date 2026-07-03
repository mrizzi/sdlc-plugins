# Codebase Investigation: ACME-500

## Code Path Tracing

### Convention Heading Extraction

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
**Function**: Convention conformance analysis

The plan-feature skill reads `CONVENTIONS.md` and extracts section headings using the following logic:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

The critical issue is at `section_name = line[3:]`. This slices the string starting at index 3 (after `## `), but does **not** call `.strip()` on the result. When a heading line contains trailing whitespace -- for example `## Migration Patterns  \n` -- the extracted section name becomes `"Migration Patterns  "` (with two trailing spaces).

### Convention-Aware Task Enrichment

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
**Function**: Convention-aware task enrichment

The task enrichment step matches conventions by exact section name:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md  {convention_name}: {action}")
```

This performs an exact string match. When the enrichment step looks up `"Migration Patterns"` (without trailing whitespace), it fails to find `"Migration Patterns  "` (with trailing whitespace) in the `discovered_conventions` dictionary. The convention is silently skipped with no warning or error.

## Exact Failure Mechanism

1. `CONVENTIONS.md` contains the line: `## Migration Patterns  ` (with trailing spaces)
2. The heading extraction logic runs `line[3:]`, producing the key `"Migration Patterns  "`
3. This key is stored in the `conventions` dictionary
4. During task enrichment, the code looks up `"Migration Patterns"` (without trailing spaces)
5. The exact-match lookup fails: `"Migration Patterns"` != `"Migration Patterns  "`
6. The convention is silently dropped -- no warning is emitted

## Root Cause Assessment

This is a **single root cause**: the heading extraction at `line[3:]` does not strip trailing whitespace. The silent failure in the enrichment step is a direct consequence of the corrupted key, not a separate bug.

## Affected Files and Symbols

| File | Symbol / Location | Issue |
|---|---|---|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention heading extraction (`section_name = line[3:]`) | Missing `.strip()` on extracted heading text |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment (`convention_name in discovered_conventions`) | Exact match fails due to upstream whitespace corruption |

## Test Coverage Gap

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does **not** include trailing whitespace on headings, so this edge case is not covered by current evals.
