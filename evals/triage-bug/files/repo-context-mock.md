<!-- SYNTHETIC TEST DATA — mock repository context for triage-bug codebase investigation eval testing -->

# Mock Repository Context: acme-backend

This file simulates the relevant code paths that the triage-bug skill would
discover during Step 3 (Codebase Investigation) for bug ACME-500.

## File: plugins/sdlc-workflow/skills/plan-feature/SKILL.md

### Convention conformance analysis (excerpt)

The plan-feature skill reads `CONVENTIONS.md` headings using this logic:

```python
# Relevant section from the skill's convention lookup
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

**Note**: The heading extraction at `line[3:]` does NOT strip trailing whitespace.
If the heading line is `## Migration Patterns  \n`, the extracted section name
becomes `"Migration Patterns  "` (with trailing spaces), which fails exact-match
comparison against the expected `"Migration Patterns"`.

## File: plugins/sdlc-workflow/skills/plan-feature/SKILL.md

### Convention-aware task enrichment (excerpt)

The task enrichment step matches conventions by section name:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
```

This match fails when `convention_name` has trailing whitespace from the extraction step.

## Test files

### Existing test: evals/plan-feature/files/conventions-mock.md

The existing eval fixture for plan-feature conventions does NOT include trailing
whitespace on headings — so this edge case is not covered by current evals.

## CONVENTIONS.md

The repository does not have a CONVENTIONS.md at its root.
