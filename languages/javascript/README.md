# JavaScript Interview Prep

Welcome to the JavaScript section! This contains coding problems implemented in JavaScript, perfect for:
- **Frontend developers** preparing for technical interviews
- **Full-stack engineers** who prefer JavaScript
- **Node.js developers** practicing algorithms
- Anyone learning algorithms in JavaScript

## Current Status

> **This section is a work in progress.** We have 2 of 35 problems ported from the Python section so far. Contributions welcome — see [CONTRIBUTING.md](../../CONTRIBUTING.md) for how to add more solutions and tests.

| Problem | Solution | Tests |
|---------|----------|-------|
| 01 — Two Sum | ✅ | ✅ |
| 15 — Valid Palindrome | ✅ | ✅ |
| 02–14, 16–35 | ❌ Not yet ported | ❌ |

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ installed
- npm or yarn

### Setup

```bash
# Install dependencies
npm install

# Run tests
npm test

# Run specific test
npm test -- 01-two-sum

# Run with coverage
npm run test:coverage
```

## 📁 Structure

```
languages/javascript/
├── README.md (this file)
├── package.json
├── jest.config.js
├── .eslintrc.js
├── solutions/
│   ├── 01-two-sum.js
│   └── 15-valid-palindrome.js
└── tests/
    ├── 01-two-sum.test.js
    └── 15-valid-palindrome.test.js
```

## 💻 Coding Style

We follow the **Airbnb JavaScript Style Guide** with ESLint:

```bash
# Check code style
npm run lint

# Auto-fix issues
npm run lint:fix
```

## 🧪 Testing

Tests are written using **Jest**:

```javascript
// Example test structure
describe('Problem: Two Sum', () => {
  test('should return correct indices', () => {
    expect(twoSum([2, 7, 11, 15], 9)).toEqual([0, 1]);
  });
});
```

## 🎯 Tips for JavaScript Solutions

1. **Use modern ES6+ features**: Arrow functions, destructuring, spread operator
2. **Prefer `const` and `let`** over `var`
3. **Use built-in methods**: `map()`, `filter()`, `reduce()`
4. **Handle edge cases**: `null`, `undefined`, empty arrays
5. **Write clean code**: Meaningful variable names, comments for complex logic

## 🤝 Contributing

Want to add more JavaScript solutions? We'd love the help! Each contribution needs:
1. A solution file in `solutions/` following the naming pattern (`NN-problem-name.js`)
2. A test file in `tests/` with at least 5 test cases (`NN-problem-name.test.js`)
3. JSDoc comments with time/space complexity

See the existing solutions for examples, and [CONTRIBUTING.md](../../CONTRIBUTING.md) for full guidelines.

## 🔗 Resources

- [MDN JavaScript Reference](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [JavaScript.info](https://javascript.info/)
- [You Don't Know JS](https://github.com/getify/You-Dont-Know-JS)
