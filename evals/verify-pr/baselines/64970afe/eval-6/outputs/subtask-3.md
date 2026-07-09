# Sub-Task: Root-cause: implement-task should check target repository file types before skipping language-specific rules

## Type: root-cause

## Repository
sdlc-plugins

## Target Branch
main

## Description
When implementing Check 6 (Documentation Coverage), the implement-task skill marked Markdown as "not applicable -- skip Markdown files" without checking whether the target repository is primarily Markdown-based. In a documentation-heavy repository like sdlc-plugins where skills are defined in Markdown, skipping the dominant file type defeats the purpose of the documentation coverage check. The implement-task skill should verify whether a file type being excluded is actually dominant in the target repository before adding exclusion rules.

This is a convention gap. The project's CONVENTIONS.md documents that "This is a documentation-heavy repository -- skills are defined in Markdown (SKILL.md files) rather than traditional programming languages" but the implement-task skill did not cross-reference this context when implementing a language-specific exclusion rule.

## Files to Modify
- `CONVENTIONS.md` -- add a convention documenting that new checks or rules must not exclude the repository's primary file type without providing an alternative coverage mechanism for that type

## Implementation Notes
- Add a convention under an appropriate section (e.g., "Code Style" or a new "Skill Design" section) that states: when implementing checks that have language-specific rules with exclusions, verify that excluded file types are not the repository's primary/dominant file type; if they are, provide an alternative rule for that file type rather than skipping it entirely
- This convention ensures that future implement-task runs will consider the repository context when implementing language-specific behavior

## Acceptance Criteria
- [ ] CONVENTIONS.md includes a convention about not excluding the repository's dominant file type from checks without providing an alternative rule
- [ ] The convention is specific enough to prevent similar oversights in future documentation-related checks
