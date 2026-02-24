# JavaScript Interview Prep

Welcome to the JavaScript section! This contains the same coding problems implemented in JavaScript, perfect for:
- **Frontend developers** preparing for FAANG interviews
- **Full-stack engineers** who prefer JavaScript
- **Node.js developers** practicing algorithms
- Anyone learning algorithms in JavaScript

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
├── problems/
│   ├── 01-two-sum.md
│   ├── 02-valid-parentheses.md
│   └── ...
├── solutions/
│   ├── 01-two-sum.js
│   ├── 02-valid-parentheses.js
│   └── ...
└── tests/
    ├── 01-two-sum.test.js
     ├── 02-valid-parentheses.test.js
    └── ...
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

## 📊 Problem Categories

### Arrays & Hashing (10 problems)
- Two Sum, Valid Anagram, Group Anagrams, etc.

### Two Pointers (4 problems)
- Valid Palindrome, 3Sum, Container With Most Water, etc.

### Sliding Window (4 problems)
- Longest Substring, Permutation in String, etc.

### Binary Search (5 problems)
- Binary Search, Search Rotated Array, etc.

### Linked Lists (3 problems)
- Reverse List, Detect Cycle, Merge Lists

### Trees & Graphs (5 problems)
- Valid BST, Level Order Traversal, Islands, etc.

### Dynamic Programming (2 problems)
- Coin Change, Kth Largest Element

## 🎯 Tips for JavaScript Solutions

1. **Use modern ES6+ features**: Arrow functions, destructuring, spread operator
2. **Prefer `const` and `let`** over `var`
3. **Use built-in methods**: `map()`, `filter()`, `reduce()`
4. **Handle edge cases**: `null`, `undefined`, empty arrays
5. **Write clean code**: Meaningful variable names, comments for complex logic

## 🔗 Resources

- [MDN JavaScript Reference](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [JavaScript.info](https://javascript.info/)
- [You Don't Know JS](https://github.com/getify/You-Dont-Know-JS)

## 🤝 Contributing

Want to add more JavaScript solutions? See [CONTRIBUTING.md](../../CONTRIBUTING.md)

---

**Happy Coding!** 🚀
