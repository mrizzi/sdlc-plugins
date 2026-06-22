# Steps 2-3 -- Codebase Investigation: ACME-500

## Step 2 -- Reproduce/Trace

### Reproduction approach

This bug involves a skill invocation (`/plan-feature`) and its internal convention parsing logic.
Direct reproduction requires running the plan-feature skill with a specially crafted CONVENTIONS.md.
Instead, code-path tracing is used to confirm the defect.

### Code-path trace

**Entry point**: `/plan-feature ACME-100` invocation, which triggers the convention conformance
analysis in the plan-feature skill.

**Trace path**:

1. The plan-feature skill reads `CONVENTIONS.md` and splits by newline.
2. For each line starting with `## `, it extracts the heading text using `line[3:]`.
3. The extracted section name is stored as a dictionary key in `conventions[section_name]`.
4. Later, the task enrichment step looks up convention names via exact match: `if convention_name in discovered_conventions`.

**Divergence point**: At step 2, `line[3:]` extracts the heading text **without stripping trailing whitespace**. When the heading line is `## Migration Patterns  \n`, the extracted key becomes `"Migration Patterns  "` (with two trailing spaces). The subsequent exact-match lookup in step 4 compares `"Migration Patterns"` (no trailing spaces) against `"Migration Patterns  "` (with trailing spaces), which fails silently.

**Reproduction outcome**: Confirmed via code-path tracing. The defect is deterministic -- any CONVENTIONS.md heading with trailing whitespace will cause the corresponding convention to be silently dropped.

## Step 3 -- Codebase Investigation

### Target repository

- **Component**: sdlc-workflow
- **Repository**: acme-backend (from Repository Registry)
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

### Code Intelligence note

Per CLAUDE.md: "No Serena MCP servers are configured. Code intelligence is not available."
Falling back to Read/Grep/Glob for investigation.

### Affected files and symbols

#### 1. Convention heading extraction

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
**Section**: Convention conformance analysis

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: does not strip trailing whitespace
        conventions[section_name] = current_section_content
```

The defect is at `line[3:]` -- this slicing extracts everything after `## ` but does not call `.strip()` or `.rstrip()` on the result. Trailing whitespace from the heading line (spaces, tabs) is preserved in the dictionary key.

#### 2. Convention-aware task enrichment

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
**Section**: Convention-aware task enrichment

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md  {convention_name}: {action}")
```

This exact-match lookup fails when `convention_name` (normalized, no trailing whitespace) does not match the key stored with trailing whitespace from the extraction step.

### Existing tests

**File**: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does **not** include trailing whitespace on headings. This edge case is not covered by current evals.

### CONVENTIONS.md lookup

The repository does not have a `CONVENTIONS.md` at its root. No conventions apply to the fix task itself.

### Investigation summary

| Finding | Detail |
|---------|--------|
| Root location | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, convention heading extraction |
| Defect | `line[3:]` does not strip trailing whitespace |
| Impact | Any CONVENTIONS.md heading with trailing whitespace is silently dropped |
| Silent failure | No warning or error is logged when a heading fails to match |
| Test gap | Existing eval fixtures lack trailing-whitespace test cases |
| Fix scope | Single root cause, single file -- no decomposition needed |
