# Codebase Investigation — ACME-500

## Step 2 — Reproduce/Trace

### Code-path tracing

This bug involves a skill invocation (`/plan-feature`) and its convention conformance
analysis logic. Direct reproduction is not possible without running the skill against
a live Jira instance. Instead, the code paths are traced.

**Entry point**: The `/plan-feature` skill reads `CONVENTIONS.md` from the target
repository and parses section headings to build a convention lookup dictionary.

**Trace findings**:

1. The convention lookup iterates over lines of `CONVENTIONS.md`, looking for lines
   starting with `## `.
2. When a heading line is found, the section name is extracted using `line[3:]`.
3. This extraction does NOT strip trailing whitespace from the heading text.
4. If the heading line in `CONVENTIONS.md` is `## Migration Patterns  \n` (with
   trailing spaces), the extracted section name becomes `"Migration Patterns  "`
   (with trailing spaces).
5. Later, when the task enrichment step checks `if convention_name in discovered_conventions`,
   it uses the clean name `"Migration Patterns"` (without trailing spaces).
6. The exact-match comparison fails because `"Migration Patterns" != "Migration Patterns  "`.
7. The convention is silently skipped — no warning or error is logged.

**Reproduction outcome**: Confirmed via code-path trace. The bug is deterministic and
will occur for any `CONVENTIONS.md` heading with trailing whitespace.

## Step 3 — Codebase Investigation

### Target repository

- **Component**: sdlc-workflow
- **Repository**: acme-backend (from Repository Registry)
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

### Code Intelligence

No Serena MCP servers are configured. Falling back to Read/Grep/Glob for investigation.

### Affected files and symbols

#### File: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

**Convention conformance analysis — heading extraction**:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

The defect is at `line[3:]`: this slices the string starting at index 3 (after `## `)
but does NOT call `.strip()` on the result. Trailing whitespace on the heading line
is preserved in `section_name`, causing the dictionary key to include trailing spaces.

**Convention-aware task enrichment — matching**:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
```

This performs an exact-match lookup using a clean convention name (without trailing
whitespace). The lookup fails when the dictionary key has trailing whitespace from
the extraction step.

### Existing test coverage

**File**: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does NOT include trailing
whitespace on headings. This edge case is not covered by current evals.

### CONVENTIONS.md lookup

The repository does not have a `CONVENTIONS.md` at its root. No conventions apply
to the fix task.

### Root cause identification

The root cause is the trailing-whitespace heading extraction: `line[3:]` does not
strip whitespace. The extracted section name retains trailing spaces, which causes
the exact-match comparison in the task enrichment step to fail silently.

### Summary of findings

| Finding | Detail |
|---------|--------|
| **Defective code** | `line[3:]` in convention heading extraction |
| **Location** | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` |
| **Mechanism** | Trailing whitespace preserved in dictionary key |
| **Impact** | Convention silently dropped from generated task |
| **Test gap** | Existing eval fixture lacks trailing-whitespace headings |
| **Fix direction** | Add `.strip()` to heading extraction: `line[3:].strip()` |
