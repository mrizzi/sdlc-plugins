# Steps 2-3 -- Codebase Investigation: ACME-500

## Step 2 -- Reproduce/Trace

### Reproduction Approach

The bug involves the plan-feature skill's internal convention parsing logic. This is
a code-path tracing scenario rather than a runnable reproduction, since the bug is in
skill behavior that requires tracing through the convention lookup code.

### Code-Path Trace

**Entry point**: `/plan-feature ACME-100` -- the plan-feature skill invocation.

**Trace path**:

1. The plan-feature skill reads `CONVENTIONS.md` and parses section headings using
   a line-by-line loop.

2. The heading extraction logic in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`:
   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]  # Extracts heading text after "## "
           conventions[section_name] = current_section_content
   ```

3. **Divergence point identified**: The extraction `line[3:]` takes everything after
   the `## ` prefix but does NOT strip trailing whitespace. When the heading line is
   `## Migration Patterns  \n` (with trailing spaces), the extracted section name
   becomes `"Migration Patterns  "` (with two trailing spaces).

4. The convention-aware task enrichment step then attempts to match by section name:
   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
   ```

5. This exact-match lookup fails because `"Migration Patterns"` (the expected key)
   does not equal `"Migration Patterns  "` (the actual key with trailing spaces).

6. The match fails silently -- no warning, no error, no log. The convention is simply
   omitted from the generated task's Implementation Notes.

### Trace Finding

The bug is confirmed through code-path tracing. The heading extraction at `line[3:]`
does not strip trailing whitespace, causing exact-match comparisons to fail when
`CONVENTIONS.md` headings contain trailing spaces. The failure is silent.

## Step 3 -- Codebase Investigation

### Target Repository

Based on the Component field (`sdlc-workflow`) and the code paths referenced in
Steps to Reproduce, the target repository is the sdlc-plugins repository itself.

From the Repository Registry:
- **Repository**: acme-backend
- **Role**: Rust backend service
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

Note: Code Intelligence section states "No Serena MCP servers are configured."
Using Read/Grep/Glob fallback.

### Affected Files and Symbols

1. **`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`** -- Convention conformance
   analysis section
   - The heading extraction logic: `section_name = line[3:]`
   - Missing `.strip()` call on the extracted section name
   - The convention-aware task enrichment: exact-match `convention_name in discovered_conventions`

### Existing Test Coverage

- **`evals/plan-feature/files/conventions-mock.md`** -- Existing eval fixture for
  plan-feature conventions does NOT include trailing whitespace on headings. This
  edge case is not covered by current evals.

### CONVENTIONS.md Lookup

The repository does not have a `CONVENTIONS.md` at its root. No conventions to
incorporate into the fix task's Implementation Notes.

### Investigation Summary

| Finding | Detail |
|---------|--------|
| **Defective file** | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` |
| **Defective code** | `section_name = line[3:]` -- no whitespace stripping |
| **Match failure** | Exact-match comparison in task enrichment step fails due to trailing spaces |
| **Silent failure** | No warning or error logged when convention is not matched |
| **Test gap** | Existing conventions-mock.md has no trailing whitespace test case |
| **Related pattern** | Convention lookup and task enrichment are in the same skill file |
