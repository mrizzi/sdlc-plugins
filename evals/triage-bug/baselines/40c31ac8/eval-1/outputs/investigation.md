# Codebase Investigation — ACME-500

## Step 2 — Reproduce/Trace

### Reproduction approach

The Steps to Reproduce involve running the `/plan-feature` skill, which is a skill invocation
rather than a directly runnable command. Direct reproduction is not feasible without invoking
the skill. Code-path tracing was used instead.

### Code-path trace

**Entry point**: `/plan-feature ACME-100` invocation triggers the plan-feature skill's
convention conformance analysis.

**Trace through convention lookup**:

1. The plan-feature skill reads `CONVENTIONS.md` and splits the content by newlines.
2. For each line, it checks if the line starts with `## ` to identify section headings.
3. The heading text is extracted using `line[3:]` — this slices the string from index 3
   onward, capturing everything after `## `.
4. **Defect identified**: `line[3:]` does NOT strip trailing whitespace. When the heading
   line is `## Migration Patterns  \n`, the extracted section name becomes
   `"Migration Patterns  "` (with two trailing spaces).

**Trace through convention matching**:

5. The task enrichment step looks up conventions by exact string comparison:
   `if convention_name in discovered_conventions`.
6. The expected key `"Migration Patterns"` does not match the stored key
   `"Migration Patterns  "` due to the trailing spaces.
7. The convention is silently skipped — no warning or error is emitted.

**Reproduction outcome**: Confirmed via code-path tracing. The bug is deterministic
whenever a CONVENTIONS.md heading contains trailing whitespace.

## Step 3 — Codebase Investigation

### Target repository

- **Repository**: acme-backend
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend
- **Component**: sdlc-workflow

Note: Code Intelligence section states no Serena MCP servers are configured, so
Read/Grep/Glob fallback was used.

### Affected files and symbols

| File | Symbol/Location | Issue |
|------|----------------|-------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention lookup loop — `section_name = line[3:]` | Heading extraction does not strip trailing whitespace |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment — `if convention_name in discovered_conventions` | Exact-match comparison fails when key has trailing spaces |

### Existing test coverage

- **File**: `evals/plan-feature/files/conventions-mock.md`
- **Gap**: The existing eval fixture for plan-feature conventions does NOT include
  trailing whitespace on headings. This edge case is not covered by current evals.

### CONVENTIONS.md lookup

The acme-backend repository does not have a `CONVENTIONS.md` at its root. No conventions
apply to the generated fix task.

### Key patterns for the fix

1. The heading extraction code is in the convention lookup section of plan-feature's SKILL.md.
2. The fix should add `.strip()` to the heading extraction: `section_name = line[3:].strip()`.
3. The reproducer test should create a CONVENTIONS.md fixture with trailing whitespace on
   headings and verify the convention is still matched and included in the output.
4. Existing eval patterns in `evals/plan-feature/` provide the test structure to follow.
