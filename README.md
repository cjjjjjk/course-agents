# AI Agents for Beginners

AI Agents for Beginners is a static reading edition of the Microsoft course, focused on theory, design patterns, architecture, and deployment methods for AI agents.

This fork keeps the course lightweight for reading and research:

- English content is the default source.
- Vietnamese content is available in `translations/vi`.
- The published site is generated as plain HTML, CSS, and JavaScript.
- Runnable notebooks, Python scripts, C# samples, and local runtime setup are intentionally excluded.

## Read the Course

The course is organized as standalone lessons. Start with the introduction if you are new to agents, or jump directly to a topic.

| Lesson | Topic |
| --- | --- |
| 00 | [Course orientation](./00-course-setup/README.md) |
| 01 | [Intro to AI Agents and Agent Use Cases](./01-intro-to-ai-agents/README.md) |
| 02 | [Exploring AI Agentic Frameworks](./02-explore-agentic-frameworks/README.md) |
| 03 | [Understanding AI Agentic Design Patterns](./03-agentic-design-patterns/README.md) |
| 04 | [Tool Use Design Pattern](./04-tool-use/README.md) |
| 05 | [Agentic RAG](./05-agentic-rag/README.md) |
| 06 | [Building Trustworthy AI Agents](./06-building-trustworthy-agents/README.md) |
| 07 | [Planning Design Pattern](./07-planning-design/README.md) |
| 08 | [Multi-Agent Design Pattern](./08-multi-agent/README.md) |
| 09 | [Metacognition Design Pattern](./09-metacognition/README.md) |
| 10 | [AI Agents in Production](./10-ai-agents-production/README.md) |
| 11 | [Agentic Protocols: MCP, A2A, and NLWeb](./11-agentic-protocols/README.md) |
| 12 | [Context Engineering for AI Agents](./12-context-engineering/README.md) |
| 13 | [Managing Agentic Memory](./13-agent-memory/README.md) |
| 14 | [Exploring Microsoft Agent Framework](./14-microsoft-agent-framework/README.md) |
| 15 | [Building Computer Use Agents](./15-browser-use/README.md) |
| 18 | [Securing AI Agents](./18-securing-ai-agents/README.md) |

## Static Site

The GitHub Pages site is built from Markdown source files by `tools/build_site.py`.

```bash
python tools/build_site.py
```

The generated output is written to `_site/`:

- `/` redirects to `/en/`.
- `/en/` contains the English course.
- `/vi/` contains the Vietnamese course.

The runtime site does not use React, Vue, MkDocs, Docusaurus, Jekyll, or any other frontend framework.

## Content Policy

This fork is for reading and studying theory. Keep contributions aligned with that purpose:

- Prefer explanations, diagrams, conceptual examples, and implementation guidance.
- Do not add runnable notebooks or application samples.
- Keep links inside lessons pointed at readable documentation pages.
- Keep English and Vietnamese navigation in sync when adding or removing lessons.

## Attribution

This repository is forked from the Microsoft AI Agents for Beginners course. Original course materials, trademarks, and third-party assets remain subject to their respective licenses and policies.
