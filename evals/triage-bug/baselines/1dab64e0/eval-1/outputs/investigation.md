# Steps 2-3 -- Codebase Investigation Findings

## Step 2 -- Reproduce/Trace

### Reproduction approach

The Steps to Reproduce describe a skill invocation (`/plan-feature ACME-100`) rather than a
directly runnable command. This is a code-path tracing scenario rather than a runnable reproduction.

### Code-path trace

**Entry point**: The plan-feature skill is invoked with a Jira issue key. During task generation,
it reads `CONVENTIONS.md` and extracts convention sections by heading.

**Trace through convention lookup**:

1. The skill reads `CONVENTIONS.md` content and splits it by newline.
2. For each line, it checks if the line starts with `## ` to identify section headings.
3. The heading text is extracted using `line[3:]` -- this takes everything after `## ` but
   does NOT strip trailing whitespace.
4. If the heading line is `## Migration Patterns  \n`, the extracted section name becomes
   `"Migration Patterns  "` (with two trailing spaces).

**Trace through convention-aware task enrichment**:

5. The task enrichment step matches conventions by section name using an exact comparison:
   `if convention_name in discovered_conventions`.
6. The canonical convention name `"Migration Patterns"` does NOT match the extracted key
   `"Migration Patterns  "` because of the trailing spaces.
7. The convention is silently skipped -- no warning or error is logged.

**Divergence point**: Step 3 above -- `line[3:]` does not call `.strip()` or `.rstrip()`,
so trailing whitespace in the heading line is preserved in the dictionary key.

### Reproduction outcome

**Confirmed via code-path trace.** The heading extraction logic at `line[3:]` does not
strip trailing whitespace, causing downstream exact-match comparisons to fail silently.

## Step 3 -- Codebase Investigation

### Target repository

- **Repository**: acme-backend
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend
- **Component**: sdlc-workflow

### Affected files and symbols

| File | Symbol/Location | Issue |
|------|-----------------|-------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention conformance analysis -- heading extraction | `line[3:]` does not strip trailing whitespace |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment -- `convention_name in discovered_conventions` | Exact match fails when key has trailing spaces |

### Existing test coverage

| Test File | Coverage |
|-----------|----------|
| `evals/plan-feature/files/conventions-mock.md` | Existing eval fixture does NOT include trailing whitespace on headings -- this edge case is not covered |

### CONVENTIONS.md lookup

The repository does not have a `CONVENTIONS.md` at its root. No additional conventions
apply to the fix task.

### Reuse candidates

- Existing plan-feature eval infrastructure (`evals/plan-feature/`) can be used as a
  pattern for the reproducer test structure
- The existing `conventions-mock.md` fixture can be duplicated/modified to include
  trailing whitespace on headings for the reproducer test

### Key findings

1. **Single root cause**: The bug has a single root cause (missing `.strip()` on heading
   extraction) that manifests in one code path. No decomposition is needed.
2. **No existing test coverage**: The trailing-whitespace edge case is not covered by
   any existing eval or test fixture.
3. **Fix is localized**: The fix requires modifying the heading extraction logic in one
   location -- adding `.strip()` to the `line[3:]` expression.
4. **Silent failure mode**: There is no logging or warning when a convention heading
   fails to match, making this bug difficult to diagnose in practice.
