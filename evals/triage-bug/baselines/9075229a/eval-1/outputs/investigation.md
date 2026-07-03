# Steps 2-3 -- Codebase Investigation: ACME-500

## Step 2 -- Reproduce/Trace

### Code-path tracing

This bug involves the plan-feature skill's convention parsing logic, which is a skill/documentation
bug that cannot be directly reproduced via CLI commands. Code-path tracing was used instead.

**Entry point**: `/plan-feature ACME-100` invocation triggers convention conformance analysis.

**Trace findings**:

1. **Convention heading extraction** (`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`):
   The plan-feature skill reads `CONVENTIONS.md` and extracts headings using this logic:
   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]  # Extracts heading text after "## "
           conventions[section_name] = current_section_content
   ```
   The extraction at `line[3:]` does NOT strip trailing whitespace. When the heading line is
   `## Migration Patterns  \n`, the extracted section name becomes `"Migration Patterns  "`
   (with two trailing spaces).

2. **Convention-aware task enrichment** (`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`):
   The task enrichment step matches conventions by exact section name:
   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
   ```
   This match fails because `"Migration Patterns"` (the expected name) does not equal
   `"Migration Patterns  "` (the extracted name with trailing spaces).

3. **No error handling or warning**: The code does not log a warning when a convention section
   is looked up but not found. The failure is completely silent.

**Divergence point**: The behavior diverges at the heading extraction step (`line[3:]`), where
trailing whitespace is preserved. The downstream exact-match comparison then fails silently.

## Step 3 -- Codebase Investigation

### Target Repository

- **Repository**: acme-backend (from Repository Registry)
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend
- **Code Intelligence**: No Serena MCP servers configured; used Read/Grep/Glob fallback.

### Affected Files and Symbols

| File | Symbol/Section | Role |
|------|---------------|------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention heading extraction loop | Extracts section names from CONVENTIONS.md without stripping whitespace |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment | Performs exact-match lookup that fails on whitespace-padded keys |

### Existing Test Coverage

- **File**: `evals/plan-feature/files/conventions-mock.md`
- **Status**: The existing eval fixture for plan-feature conventions does NOT include trailing
  whitespace on headings. This edge case is not covered by current evals.

### CONVENTIONS.md Lookup

The repository does not have a `CONVENTIONS.md` file at its root. No conventions apply to the
generated fix task.

### Investigation Goals Summary

1. **Specific files and symbols affected**: The convention heading extraction logic in
   `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- specifically the `line[3:]` extraction
   that fails to strip trailing whitespace.

2. **Code paths involved**: Convention file reading -> heading extraction -> section name storage ->
   convention-to-task matching. The defect is in the extraction step, manifesting at the matching step.

3. **Correct patterns for Implementation Notes**: The fix should add `.strip()` (or equivalent
   whitespace trimming) to the heading extraction step. Existing convention matching logic is
   otherwise correct.

4. **Existing test files and patterns**: `evals/plan-feature/files/conventions-mock.md` is the
   relevant fixture file. A reproducer test should add a variant with trailing whitespace on headings.

5. **Reusable utilities**: No additional shared utilities identified -- the fix is localized to the
   heading extraction logic.
