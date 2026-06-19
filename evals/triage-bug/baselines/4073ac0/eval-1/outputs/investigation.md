# Codebase Investigation — ACME-500

## Step 2 — Reproduce/Trace

### Code-path tracing

The bug cannot be directly reproduced via runnable commands (it involves a skill invocation). Tracing through the relevant code paths instead.

**Entry point**: `/plan-feature ACME-100` — the plan-feature skill invocation.

**Trace path**:

1. The plan-feature skill reads `CONVENTIONS.md` using a line-by-line parser.
2. The heading extraction logic in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` uses:
   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]  # Extracts heading text after "## "
           conventions[section_name] = current_section_content
   ```
3. The extraction `line[3:]` does **not** strip trailing whitespace. When the heading line is `## Migration Patterns  \n`, the extracted section name becomes `"Migration Patterns  "` (with two trailing spaces).
4. Later, the convention-aware task enrichment step performs an exact match:
   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md  {convention_name}: {action}")
   ```
5. The match fails because `"Migration Patterns"` (expected, no trailing spaces) does not equal `"Migration Patterns  "` (extracted, with trailing spaces).
6. No warning or error is logged when the match fails — the convention is silently dropped.

**Trace finding**: The divergence between expected and actual behavior occurs at the heading extraction step (`line[3:]`), which does not call `.strip()` or `.rstrip()` on the extracted heading text.

## Step 3 — Codebase Investigation

### Target repository

Based on the Component field (`sdlc-workflow`) and the code paths referenced in Steps to Reproduce, the bug affects the **acme-backend** repository.

- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

### Affected files and symbols

| File | Symbol/Location | Issue |
|------|----------------|-------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention conformance analysis — heading extraction loop | `line[3:]` does not strip trailing whitespace |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment — exact match lookup | `convention_name in discovered_conventions` fails for whitespace-padded keys |

### Existing test coverage

- `evals/plan-feature/files/conventions-mock.md` — the existing eval fixture for plan-feature conventions does **not** include trailing whitespace on headings. This edge case is not covered by current evals.

### CONVENTIONS.md lookup

The repository does not have a `CONVENTIONS.md` at its root. No project-specific conventions to incorporate into the fix task.

### Investigation summary

- **Root cause location**: The heading extraction logic in plan-feature's convention conformance analysis uses `line[3:]` without stripping whitespace.
- **Impact**: Any `CONVENTIONS.md` heading with trailing whitespace will be silently dropped during convention-aware task enrichment.
- **Existing patterns**: The existing eval fixture does not cover trailing whitespace, confirming this is an untested edge case.
- **Relevant test directory**: `evals/plan-feature/` — the reproducer test should follow the existing eval patterns in this directory.
