# Contributing

Thank you for contributing! This document explains how to add languages, problems, and projects in a consistent way.

Principles
- Keep content clear, concise, and educational.
- Prefer runnable examples where feasible.
- Use templates to keep a consistent contributor experience.

License expectations
- Code (scripts, runnable code, helper libraries) in the repository: MIT License (see LICENSE).
- Content (problem statements, solutions, project drafts, walkthroughs): CC BY‑NC‑SA 4.0 (see CONTENT_LICENSE.md).
- By submitting a PR, you agree to license your contribution under the repository licenses above.
- Add a one-line header in new files if you want to indicate license explicitly (example below).

Recommended license header examples
- For code files:
  // Copyright (c) 2026 ShamShamsw
  // Licensed under the MIT License. See LICENSE.
- For content files (Markdown):
  <!--
  Copyright (c) 2026 <Your Name>
  This content is licensed under CC BY‑NC‑SA 4.0. See CONTENT_LICENSE.md.
  -->

How to add a new language section
1. Create a folder at /languages/<language-name> (lowercase).
2. Add a README.md with:
   - Short intro and recommended runtime/version.
   - How to run examples/tests.
   - Style/format guidance (e.g., PEP8 for Python).
3. Add /problems and /projects subfolders.

Problem format (markdown)
- Filename: kebab-case, e.g., two-sum.md
- Template (required fields):
  - Title
  - Difficulty: Easy | Medium | Hard
  - Topics: array, dp, graph, sql, etc.
  - Statement
  - Examples
  - Constraints
  - Hints (optional)
  - Canonical solution: link to solution file(s)
  - Tests (optional): add small runnable tests if applicable

Project format
- Each project should use a dedicated directory:
  /languages/<lang>/projects/<project-name>/
    - README.md (step-by-step guide + objectives)
    - starter/ (starter code)
    - final/ (complete solution)
    - tests/ (optional)
    - walkthrough.ipynb (optional; recommended for Python)
- The README should include expected learning outcomes, time estimate, and suggested extensions.

Jupyter notebooks (Python)
- Short examples and walkthroughs may be provided as notebooks.
- Keep notebooks focused and small (few cells).
- Remove large datasets; use small sample data or link to external datasets.

Pull request process
- Fork the repo (or branch from main if you have access).
- Create a feature branch with a descriptive name.
- One feature per PR (e.g., add-python-cheatsheet).
- Write a clear PR description and link to related issues.
- Include tests for runnable problems if applicable.
- Maintain formatting (prettier/black as appropriate).

Labels & issues
- Use labels: good first issue, help wanted, documentation, feature, bug.
- If you want to join as an active maintainer, open an issue describing your interest.

Thank you — contributors make this project possible!
