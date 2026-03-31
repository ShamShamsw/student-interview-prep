# Contributing

Thank you for contributing! This document explains how to add languages, problems, and projects in a consistent way.

Principles
- Keep content clear, concise, and educational.
- Prefer runnable examples where feasible.
- Use templates to keep a consistent contributor experience.

License expectations
- Code (scripts, runnable code, helper libraries) in the repository: Student Interview Prep Source-Available Non-Commercial Attribution License 1.0 (see LICENSE).
- Content (problem statements, solutions, project drafts, walkthroughs): CC BY‑NC‑SA 4.0 (see CONTENT_LICENSE.md).
- By submitting a PR, you agree to license your contribution under the repository licenses above and grant the copyright holder(s) the right to relicense your contribution for future versions of the repository.
- Add a one-line header in new files if you want to indicate license explicitly (example below).

Recommended license header examples
- For code files:
  // Copyright (c) 2026 ShamShamsw
  // Licensed under the Student Interview Prep Source-Available Non-Commercial Attribution License 1.0. See LICENSE.
- For content files (Markdown):
  <!--
  Copyright (c) 2026 <Your Name>
  This content is licensed under CC BY‑NC‑SA 4.0. See CONTENT_LICENSE.md.
  -->

License note
- The repository source code is source-available, not OSI open source, because commercial sale and other commercial use require prior written permission.
- Future versions of the repository may be released under different license terms at the sole discretion of the copyright holder(s). Already released versions remain governed by the license that applied when they were released.

## Why Open Source Matters

Open source projects are projects whose source code, documentation, or learning materials are shared publicly so other people can read them, use them, improve them, and contribute back under the project license. In practice, open source helps turn individual work into something the wider community can learn from and build on.

Why people create open source projects
- To solve a real problem in public so others can reuse the solution.
- To teach, document ideas, and help other learners avoid starting from zero.
- To build a portfolio that shows practical skills, code quality, and communication.
- To attract collaborators who can add features, fix bugs, and improve documentation.
- To create tools or resources that keep improving beyond what one person can maintain alone.

Why open source is becoming more popular
- Remote collaboration is normal, so public repositories are an easy way to work across locations and time zones.
- Employers increasingly value visible proof of problem-solving, testing, documentation, and teamwork.
- Modern developer platforms make it easier to share code, review changes, track issues, and welcome contributors.
- Communities learn faster when examples, templates, and reference implementations are public.
- AI tools, automation, and package ecosystems make it easier to start small and grow a project over time.

Why it matters for learners and maintainers
- You get feedback from real users instead of guessing what is useful.
- You practice writing for other people, not just for yourself.
- You learn project hygiene: version control, tests, issue tracking, release notes, and documentation.
- You build credibility by showing how you make decisions and respond to review.

## Planning an Open Source Project

Before publishing, define the project clearly.

1. Start with one specific problem. A narrow first version is easier to explain, test, and maintain.
2. Decide who the project is for. Beginner learners, job seekers, maintainers, and experienced developers all need different levels of detail.
3. Write down the scope. Be explicit about what the project will do now and what is out of scope for the first release.
4. Choose the license early. Contributors need to know how code and content can be used.
5. Set contribution rules. A README, contribution guide, and issue labels reduce confusion and lower the barrier to entry.
6. Make the first tasks small. Good starter issues, documentation fixes, and test improvements help new contributors get involved.
7. Plan for maintenance. If you cannot review changes or answer issues, the project will stall no matter how strong the initial idea is.

Useful first-project checklist
- Clear README with project purpose, setup steps, and examples.
- CONTRIBUTING guide with contribution standards.
- CODE_OF_CONDUCT to set expectations for collaboration.
- Starter issues labeled for beginners.
- A realistic roadmap so contributors can see where help is needed.

## Finding People to Work With

Good collaborators usually join projects that are easy to understand and easy to contribute to.

- Share the project in places where the audience already gathers: GitHub, Discord communities, Reddit, student groups, meetups, and class or bootcamp communities.
- Open beginner-friendly issues with precise descriptions, acceptance criteria, and setup instructions.
- Ask for help on small, concrete tasks first. People are more likely to contribute to a well-defined improvement than to a vague request.
- Write contribution docs that make the first pull request feel safe and predictable.
- Respond quickly and respectfully to questions and pull requests. Slow or unclear communication often drives contributors away.

## Why Other Opinions Matter

Other opinions matter because open source projects are meant to be used by more than one person. What feels obvious to the maintainer may be confusing to a new contributor or user.

- Different contributors notice different problems: unclear naming, missing setup steps, weak tests, or assumptions that exclude beginners.
- Review from others improves technical quality by catching bugs, edge cases, and design mistakes earlier.
- Outside feedback helps prioritize the features people actually need instead of the features the maintainer assumes they need.
- A project that welcomes discussion usually becomes more durable because decisions are documented and challenged before they become costly.

Strong open source projects are rarely the result of one perfect opinion. They improve through repeated review, clearer documentation, and contributions from people with different backgrounds and goals.

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
- Notebook file should be valid `.ipynb` JSON with:
  - top-level `cells` array
  - each cell containing `cell_type`, `metadata`, and `source`
  - `source` as a string or list of strings
- Preferred cell metadata:
  - `metadata.language` set to `markdown` or `python` when applicable
  - `metadata.id` preserved for existing cells when editing notebooks
- Keep notebooks deterministic for CI:
  - avoid environment-specific absolute paths in code cells
  - avoid large binary outputs and clear unnecessary execution output
  - keep walkthrough notebooks mostly markdown unless code execution is required
- Notebook checks run in CI via `.github/workflows/notebook-checks.yml` and `.github/scripts/check_notebooks.py`.
  - If checks fail, validate JSON structure first, then cell shape (`cell_type`, `metadata`, `source`).

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

## PR Checklist (Quick)

Use this short checklist when opening a PR. See `CONTRIBUTING.md` above for full guidance.

- Title and description clearly explain the change and link related issues.
- Branch name is descriptive (e.g., `add-python-two-sum-template`).
- Run `pre-commit` locally and fix formatting issues: `pre-commit run --all-files`.
- Include or update tests where applicable; run `pytest` and ensure tests pass.
- Update `languages/python/problems/README.md` or relevant README if adding content.
- Add any new dependencies to `requirements-dev.txt` or the relevant project `requirements.txt`.

## Example: Add a new problem (fast steps)

1. Copy `languages/python/problems/templates/PROBLEM_TEMPLATE.md` to `languages/python/problems/NN-problem-name.md`.
2. Fill Title, Difficulty, Topics, Statement, Examples, Constraints, and Canonical solution field.
3. Add a solution under `languages/python/problems/solutions/NN-problem-name.py` using the solution template.
4. Add tests in `languages/python/problems/tests/test_NN_problem_name.py` using the test template.
5. Run `pre-commit run --all-files` and `pytest` before opening a PR.

