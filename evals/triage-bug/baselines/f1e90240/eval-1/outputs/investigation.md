# Codebase Investigation: ACME-500

## Code Path Trace

### Step 1: Convention Extraction (Root of the Bug)

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- Convention conformance analysis

The plan-feature skill reads `CONVENTIONS.md` headings using this logic:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

The heading extraction at `line[3:]` does NOT strip trailing whitespace. When the heading line is `## Migration Patterns  \n`, the extracted section name becomes `"Migration Patterns  "` (with two trailing spaces). This is the origin of the defect.

### Step 2: Convention Matching (Where the Failure Manifests)

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- Convention-aware task enrichment

The task enrichment step matches conventions by exact section name:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md  {convention_name}: {action}")
```

This match fails because `convention_name` is the clean string `"Migration Patterns"` while the dictionary key stored during extraction is `"Migration Patterns  "` (with trailing spaces). The `in` operator performs an exact-match lookup, so the convention is not found.

### Step 3: Silent Failure

There is no `else` branch or fallback logging when a convention name is not found in `discovered_conventions`. The convention is simply skipped without any warning, making the issue invisible to the user.

### Step 4: Test Coverage Gap

**File**: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does NOT include trailing whitespace on headings. This edge case is therefore not covered by any current eval or test, which explains why it was not caught before release.

## Divergence Point

The actual behavior diverges from expected behavior at **Step 1 (Convention Extraction)**. The `line[3:]` slice captures everything after `## ` including trailing whitespace characters. All downstream lookups that use the extracted section name as a dictionary key will fail when the original heading has trailing whitespace, because the lookup keys are clean (trimmed) strings.

## Affected Files

| File | Role in Bug |
|------|-------------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` (convention lookup) | Extracts heading without stripping trailing whitespace |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` (task enrichment) | Exact-match fails due to whitespace mismatch |
| `evals/plan-feature/files/conventions-mock.md` | Missing test coverage for trailing whitespace edge case |
