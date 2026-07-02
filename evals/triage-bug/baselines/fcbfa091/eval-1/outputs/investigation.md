# Codebase Investigation: ACME-500

## Target Repository

- **Repository**: acme-backend (from Repository Registry)
- **Role**: Rust backend service
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

## Component Match

The Bug's Component field is `sdlc-workflow`, which matches the plugin at `plugins/sdlc-workflow/`.

## Step 2: Code-Path Tracing

The Steps to Reproduce describe a skill invocation (`/plan-feature ACME-100`) rather than
a runnable command, so direct reproduction is not possible. Instead, the code paths were
traced through the plan-feature skill's convention handling logic.

### Entry point

The entry point is the plan-feature skill invocation. When plan-feature processes a feature,
it reads the repository's `CONVENTIONS.md` file and extracts convention sections by heading
to enrich generated task descriptions with convention references.

### Trace through convention lookup

In `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, the convention conformance analysis
section contains the following heading extraction logic:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

**Finding**: `line[3:]` slices the string starting at index 3 (after `## `), but it does
NOT strip trailing whitespace or newline characters. When the heading line in CONVENTIONS.md
is `## Migration Patterns  \n`, the extracted `section_name` becomes `"Migration Patterns  "`
(with two trailing spaces), not `"Migration Patterns"`.

### Trace through convention-aware task enrichment

The task enrichment step matches conventions by section name using exact string comparison:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
```

When the skill looks up `"Migration Patterns"` (without trailing spaces) in the
`discovered_conventions` dictionary, it fails to find a match because the dictionary key
is `"Migration Patterns  "` (with trailing spaces). The convention is silently dropped --
no warning or error is produced.

## Step 3: Codebase Investigation Findings

### Affected Files and Symbols

| File | Symbol/Section | Issue |
|------|----------------|-------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention conformance analysis -- heading extraction | `line[3:]` does not strip trailing whitespace |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment | Exact-match lookup fails when key has trailing whitespace |

### Existing Test Coverage

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does NOT include
trailing whitespace on headings. This edge case is not covered by current evals, which is
why the bug was not caught during development.

### CONVENTIONS.md Lookup

The repository does not have a `CONVENTIONS.md` at its root. No additional conventions
apply to the fix task.

### Root Cause Summary

The root cause is a missing `.strip()` call on the heading extraction in the plan-feature
convention lookup. The line `section_name = line[3:]` should be
`section_name = line[3:].strip()` to normalize heading names by removing trailing whitespace
(including spaces, tabs, and newline characters).

This causes any convention section whose heading has trailing whitespace to be silently
excluded from generated task descriptions, with no warning to the user.
