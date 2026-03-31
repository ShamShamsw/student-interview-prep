# JavaScript Interview Prep

This track contains JavaScript interview problem solutions with Jest tests.

It is best for:
- Frontend engineers preparing for coding interviews
- Full-stack developers who want JavaScript-first practice
- Node.js learners building algorithm fluency

## Current Coverage

This track is currently partial.

| Problem | Solution | Tests |
|---------|----------|-------|
| 01-two-sum | Yes | Yes |
| 15-valid-palindrome | Yes | Yes |
| Remaining problems | Not yet ported | Not yet ported |

To help port additional problems, see [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Quick Start

Prerequisites:
- Node.js 16+
- npm

From [languages/javascript](./):

```bash
npm install
npm test
```

Useful commands:

```bash
# Run one test file
npm test -- 01-two-sum

# Coverage
npm run test:coverage

# Lint and auto-fix
npm run lint
npm run lint:fix
```

## Folder Structure

```text
languages/javascript/
  solutions/    # Problem implementations (NN-problem-name.js)
  tests/        # Jest tests (NN-problem-name.test.js)
  package.json  # Scripts and dependencies
```

## Workflow For Adding A Problem

1. Create a solution file in `solutions/` named `NN-problem-name.js`.
2. Export a single function matching the problem requirement.
3. Create a matching Jest file in `tests/` named `NN-problem-name.test.js`.
4. Add at least 5 test cases:
   - Normal case
   - Edge case
   - Duplicate/value-collision case (if relevant)
   - Empty/minimum input case
   - Large input or stress-style case
5. Add JSDoc for time and space complexity.
6. Run `npm test` and `npm run lint` before opening a PR.

## Solution Quality Checklist

- Uses `const`/`let` (no `var`)
- Handles invalid/empty input safely
- Avoids mutation unless required
- Includes clear variable names and concise logic
- Complexity is documented and accurate

## Reference

- [MDN JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [JavaScript.info](https://javascript.info/)
- [You Don't Know JS](https://github.com/getify/You-Dont-Know-JS)
