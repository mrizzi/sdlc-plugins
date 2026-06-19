## Criterion 7: Root-cause investigation runs on eval failure sub-tasks

**Result: PASS**

Step 7 (Root-Cause Investigation) is activated because Step 6d created sub-tasks (specifically the eval-3 failure sub-task). Per Step 7a, eval failure sub-tasks from Step 6d are included alongside review feedback sub-tasks and CI failure sub-tasks as inputs to root-cause investigation.

The eval-3 failures concern convention upgrade eligibility and sub-task creation -- these are universal knowledge (eval design patterns apply across repos) and classify as method-based skill gaps in the implement-task phase:

- **Universality test:** The knowledge required to prevent these defects (evaluating convention upgrade eligibility for suggestions, creating sub-tasks for code change requests including upgraded suggestions) applies to ANY repository, not just this specific one. Result: universal.
- **Method-vs-Fact test:** The guidance ("check whether suggestions match documented conventions before skipping them", "ensure sub-tasks are created for all code change requests including upgraded suggestions") is expressible as methods without referencing language-specific APIs. Result: method.
- **Classification:** Skill gap in the implement-task phase -- the verify-pr skill's convention upgrade logic failed to evaluate whether the suggestion matched a project convention.

A root-cause task is created targeting the implement-task skill to improve convention upgrade evaluation.
