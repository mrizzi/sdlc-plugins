# Codebase Investigation — ACME-500

## Step 2 — Reproduce/Trace

### Code-path tracing

This bug involves a skill invocation (`/plan-feature`) and cannot be directly reproduced via CLI commands in this context. Code-path tracing was performed instead.

**Entry point**: The `/plan-feature` skill reads `CONVENTIONS.md` and extracts section headings to build a conventions lookup table.

**Trace findings**:

1. The convention extraction logic in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` splits the file content by newlines and identifies headings starting with `## `.
2. The heading text is extracted using `line[3:]`, which takes the substring after `## ` but does **not** strip trailing whitespace.
3. When a heading line has trailing whitespace (e.g., `## Migration Patterns  \n`), the extracted section name becomes `"Migration Patterns  "` (with trailing spaces).
4. Later, the convention-aware task enrichment step performs an exact match: `if convention_name in discovered_conventions`. The lookup uses the clean name `"Migration Patterns"`, which does not match the whitespace-padded key `"Migration Patterns  "`.
5. The match silently fails — no warning or error is logged — and the convention is omitted from the generated task's Implementation Notes.

**Reproduction outcome**: Confirmed via code-path tracing. The behavior described in the bug report is consistent with the code logic.

## Step 3 — Codebase Investigation

### Target repository

- **Repository**: acme-backend
- **Serena Instance**: serena_backend (from Repository Registry)
- **Path**: /home/dev/repos/acme-backend
- **Component**: sdlc-workflow

### Affected files and symbols

| File | Symbol/Section | Issue |
|------|---------------|-------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention heading extraction (`line[3:]`) | Does not strip trailing whitespace from heading text |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment (`convention_name in discovered_conventions`) | Exact match fails when key has trailing whitespace |

### Code analysis

**Convention extraction (root of the defect)**:
```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: no .strip() call
        conventions[section_name] = current_section_content
```

The fix point is `line[3:]` which should be `line[3:].strip()` to normalize trailing whitespace.

**Convention matching (downstream failure)**:
```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
```

This match is correct in isolation — the problem is upstream in the key extraction.

### Existing test coverage

- **File**: `evals/plan-feature/files/conventions-mock.md`
- **Finding**: The existing eval fixture for plan-feature conventions does NOT include trailing whitespace on headings. This edge case is not covered by current evals.

### CONVENTIONS.md lookup

The repository does not have a `CONVENTIONS.md` at its root. No conventions to apply to this fix task.

### Reuse candidates

No existing whitespace-trimming utilities or shared string normalization helpers were discovered in the codebase. The fix is a straightforward `.strip()` call at the extraction point.
