# Evaluating skills: ideas for cross-iteration comparison and token optimization

> Draft issue for [agentskills/agentskills](https://github.com/agentskills/agentskills).
> References: [evaluating-skills.mdx](https://github.com/agentskills/agentskills/blob/main/docs/skill-creation/evaluating-skills.mdx)

## Context

We followed the [Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills) guide to build an eval framework for a skill that generates Jira implementation plans. The guide was excellent for getting the first iteration running end-to-end. As we moved into subsequent iterations, we ran into a few scenarios where we extended the approach — sharing in case these are useful upstream.

## 1: Persisting results for cross-iteration comparison

The guide covers comparing `with_skill` vs `without_skill` within a single iteration via `benchmark.json`. When we started iterating on the skill (the loop in "Iterating on the skill"), we wanted to also compare iteration-1 results against iteration-2 to measure improvement over time. Since the workspace is ephemeral, we needed a way to preserve baseline results across iterations.

**Our approach:** We commit baseline results to `evals/<skill>/baselines/<git-commit-hash>/` folders, keyed by the main branch commit hash. Each folder contains the full outputs, grading.json, timing.json, benchmark.json, and feedback.json. This makes cross-iteration comparison straightforward — look up the previous baseline by commit hash and compute the delta.

## 2: Reusing base-branch results across PR iterations

When iterating on a skill across multiple PR cycles, the base-branch (main) SKILL.md stays the same while the PR-branch version evolves. We found that re-running base-branch evals on every iteration produced identical results, so we looked for a way to run them once and reuse.

**Our approach:** CI runs evals once on push to main and commits results to `baselines/<hash>/`. Subsequent PRs look up the stored baseline instead of re-running base-branch evals. This reduces per-iteration cost by roughly half.

## 3: Naming for version-to-version comparison

The guide uses `with_skill/` and `without_skill/` subdirectories, which works well for measuring the value a skill adds over no skill at all. In our case, after the first iteration, we were mostly comparing two versions of the same skill — both runs use the skill, just different versions. We found that adapting the naming helped clarify what each configuration represents.

**Our approach:** We use `pr-branch/` and `base-branch/` to reflect that both configurations run with the skill, differing only in version. The guide already acknowledges this scenario ("use the previous version as your baseline... save to `old_skill/outputs/`") — our naming is just a variation on that.

## Suggestion

A brief note in the guide about preserving `benchmark.json` between iterations for trend tracking could help practitioners who want to measure improvement over time. The token optimization and naming adaptation may be too context-specific, but we're happy to share more details if useful.

Our full implementation is at [mrizzi/sdlc-plugins PR #83](https://github.com/mrizzi/sdlc-plugins/pull/83).
