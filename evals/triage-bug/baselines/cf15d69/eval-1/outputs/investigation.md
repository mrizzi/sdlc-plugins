# Codebase Investigation - ACME-500

## Step 2: Reproduce/Trace

### Code Path Traced from Steps to Reproduce

The bug report states that running `/plan-feature` on a feature requiring database migrations fails to pick up the "Migration Patterns" convention from `CONVENTIONS.md` when the heading line has trailing whitespace.

Tracing the code path:

1. **Entry point**: `/plan-feature ACME-100` invokes the plan-feature skill
2. **Convention loading**: The skill reads `CONVENTIONS.md` and parses headings to build a dictionary of convention sections
3. **Heading extraction**: Located in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- the convention lookup logic:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

4. **The defect**: `line[3:]` slices the string from index 3 onward but does NOT strip trailing whitespace. When the heading line is `## Migration Patterns  \n`, the extracted key becomes `"Migration Patterns  "` (with two trailing spaces).

5. **Convention matching**: The task enrichment step performs an exact-match lookup:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

The lookup key `"Migration Patterns"` (no trailing spaces) does not match the stored key `"Migration Patterns  "` (with trailing spaces), so the match fails silently.

6. **Silent failure**: No warning or fallback is triggered when a convention is not found, causing the convention to be silently dropped from the generated task description.

## Step 3: Codebase Investigation

### Affected Files and Symbols

| File | Symbol/Location | Role |
|------|----------------|------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention conformance analysis -- heading extraction (`line[3:]`) | **Root cause**: does not strip trailing whitespace from heading text |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment -- `convention_name in discovered_conventions` | **Failure point**: exact-match comparison fails due to whitespace mismatch |
| `evals/plan-feature/files/conventions-mock.md` | Existing eval fixture | **Gap**: does not include trailing whitespace on headings, so the edge case is untested |

### Existing Test Coverage

The existing eval fixture `evals/plan-feature/files/conventions-mock.md` does NOT include trailing whitespace on headings. This means the current eval suite does not exercise the code path that leads to this bug.

### Root Cause Classification

- **Type**: Input sanitization defect
- **Severity**: Medium -- conventions are silently dropped with no warning, producing incorrect task descriptions
- **Scope**: Affects any `CONVENTIONS.md` heading that has trailing whitespace (spaces or tabs before the newline)
