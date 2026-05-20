
## Project Overview

This repository is a lightweight static documentation fork of "AI Agents for Beginners". The goal is to publish the course as a bilingual GitHub Pages reading site for theory, design patterns, architecture, and implementation methods.

## Current Scope

- Default language: English.
- Secondary language: Vietnamese in `translations/vi`.
- Source content: Markdown.
- Published output: static HTML, CSS, JavaScript in `_site/`.
- Runtime frontend: no framework.
- Practice/runtime files are intentionally excluded from the course source.

## Site Build

Build the static site with:

```bash
python tools/build_site.py
```

The build script:

- Reads English Markdown from the repository root and lesson folders.
- Reads Vietnamese Markdown from `translations/vi`.
- Generates `/en/` and `/vi/`.
- Copies readable image assets.
- Fails if generated pages link to `.md`, `.ipynb`, `.py`, or `.cs` files.

## Content Guidelines

- Keep the site focused on reading and research.
- Prefer conceptual explanation, diagrams, design tradeoffs, architecture notes, and deployment methods.
- Do not add runnable notebooks, Python samples, C# samples, local app demos, or environment setup flows.
- Short code snippets inside Markdown are acceptable when they explain a concept and are not presented as a runnable exercise.
- Keep English and Vietnamese lesson navigation aligned.
- Avoid links to removed practice files.

## File Organization

```text
README.md
STUDY_GUIDE.md
site/
  template.html
  assets/
tools/
  build_site.py
translations/
  vi/
<lesson-number>-<lesson-name>/
  README.md
  images/
```

## GitHub Pages

Deployment is handled by `.github/workflows/deploy-pages.yml`.

The workflow runs on pushes to `main` and through manual `workflow_dispatch`. It builds `_site/`, uploads the Pages artifact, and deploys with the official GitHub Pages actions.


## Verification

Before committing site changes:

1. Run `python tools/build_site.py`.
2. Confirm `_site/index.html`, `_site/en/index.html`, and `_site/vi/index.html` exist.
3. Confirm generated links do not point to `.md`, `.ipynb`, `.py`, or `.cs`.
4. Check a few English and Vietnamese lesson pages for navigation, images, tables, and code blocks.
