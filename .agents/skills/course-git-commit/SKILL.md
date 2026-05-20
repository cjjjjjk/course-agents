---
name: course-git-commit
description: Apply this project's commit message format, test-before-commit gate, and Codex co-author footer.
user-invocable: true
when_to_use: "Use before creating commits or when reviewing commit readiness."
category: workflow
keywords: [commit, git, verification]
---

# Backend Commit Skill

## Message Format

Use an uppercase commit type.

```txt
type(scope - optional): message

- description 1 of the change 
- description 2 of the change
...

```

Rules:

- `scope` is optional.
- When a scope is used, put it inside parentheses.
- Keep the message concise and descriptive.

Examples:

## Auto-Commit Gate

Agents may proactively create a commit after completing requested work only when all relevant tests pass.

Rules:

- Run the relevant test suite before committing.
- Do not commit if tests fail.
- If tests cannot be run, report the reason and do not auto-commit unless the user explicitly asks.
- Include the agent co-author footer when the agent contributed to the change.

```txt
Co-authored-by: ...agent_name.. <agent_email>
```
