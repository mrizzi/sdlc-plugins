# Steps 2-3 -- Codebase Investigation: ACME-500

## Step 2 -- Reproduce/Trace

### Reproduction approach

This bug involves a skill invocation (`/plan-feature`) and its behavior when processing
`CONVENTIONS.md` files. It cannot be directly reproduced via CLI commands in a read-only
context. Code-path tracing is used instead.

### Code-path trace

**Entry point**: The `/plan-feature` skill is invoked with a feature issue (e.g., ACME-100).
During task generation, the skill reads `CONVENTIONS.md` from the target repository root
to discover project conventions and embed them in the generated task's Implementation Notes.

**Convention extraction logic** (in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`):

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

**Divergence point**: The heading extraction at `line[3:]` captures everything after `## `,
including any trailing whitespace. When the heading line is `## Migration Patterns  \n`,
the extracted `section_name` becomes `"Migration Patterns  "` (with two trailing spaces).

**Convention matching logic** (in the same file):

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

The match uses exact string comparison. The lookup key `"Migration Patterns"` (without
trailing spaces) does not match the stored key `"Migration Patterns  "` (with trailing
spaces), so the convention is silently skipped.

### Trace finding

**Confirmed**: The bug is reproducible via code-path analysis. The trailing whitespace
on `CONVENTIONS.md` headings causes a key mismatch in the convention lookup dictionary,
resulting in silently dropped conventions.

## Step 3 -- Codebase Investigation

### Target repository

- **Repository**: acme-backend
- **Serena Instance**: serena_backend (not available -- Code Intelligence section states
  no Serena instances configured)
- **Path**: /home/dev/repos/acme-backend
- **Fallback**: Read/Grep/Glob tools used for investigation

### Affected files and symbols

| File | Symbol/Region | Role |
|------|--------------|------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention extraction loop (`line[3:]`) | Heading text extraction without `.strip()` |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention matching (`convention_name in discovered_conventions`) | Exact-match lookup fails with whitespace mismatch |

### Existing test coverage

- **File**: `evals/plan-feature/files/conventions-mock.md`
- **Coverage gap**: The existing eval fixture does NOT include trailing whitespace on
  headings. This edge case is not covered by current evals.

### CONVENTIONS.md lookup

The repository (`acme-backend`) does not have a `CONVENTIONS.md` at its root. No
additional conventions apply to the fix task.

### Investigation summary

1. **Single root cause**: The heading extraction in plan-feature's convention parsing does
   not strip trailing whitespace from `CONVENTIONS.md` headings.
2. **Single manifestation point**: The dictionary lookup uses exact string matching, which
   fails when keys contain trailing whitespace.
3. **No silent error handling**: There is no warning or logging when a convention is not
   found, making the failure silent.
4. **Fix scope**: The fix requires adding `.strip()` to the heading extraction and
   potentially adding a warning when an expected convention is not matched.
5. **Decomposition guard**: This is a single root cause (missing whitespace normalization)
   manifesting in one code path. A single Task is appropriate -- no decomposition needed.
