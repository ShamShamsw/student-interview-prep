# Frontend Interview Questions

Questions specific to frontend and UI engineering roles — HTML, CSS, JavaScript, frameworks, and user experience.

---

## HTML & Semantics

1. **What is semantic HTML and why does it matter?**
   _Using elements like `<header>`, `<nav>`, `<main>`, `<article>` instead of generic `<div>`. Improves accessibility, SEO, and readability._

2. **What is the difference between `<div>` and `<span>`?**
   _`<div>` is block-level (takes full width). `<span>` is inline (flows with text)._

3. **What does the `DOCTYPE` declaration do?**
   _Tells the browser which version of HTML to use. `<!DOCTYPE html>` triggers standards mode._

4. **Explain the difference between `id` and `class` attributes.**
   _`id` is unique per page (one element). `class` can be shared across many elements._

5. **What is accessibility (a11y)? Name 3 things you'd check.**
   _Making sites usable for everyone. Check: alt text on images, keyboard navigation, color contrast._

---

## CSS & Layout

6. **Explain the CSS box model.**
   _Content → Padding → Border → Margin. `box-sizing: border-box` includes padding/border in width._

7. **What is the difference between Flexbox and CSS Grid?**
   _Flexbox: one-dimensional (row or column). Grid: two-dimensional (rows and columns)._

8. **How does `position: relative` differ from `position: absolute`?**
   _Relative: offset from normal position, still in flow. Absolute: removed from flow, positioned relative to nearest positioned ancestor._

9. **What is specificity in CSS? How do you resolve conflicts?**
   _Inline > ID > class > element. More specific selectors override less specific ones._

10. **How would you make a website responsive?**
    _Media queries, fluid widths (%, vw/vh), flexible images, mobile-first design._

---

## JavaScript Core

11. **What is the difference between `let`, `const`, and `var`?**
    _`var`: function-scoped, hoisted. `let`: block-scoped, reassignable. `const`: block-scoped, not reassignable._

12. **Explain closures with an example.**
    _A function that remembers variables from its outer scope even after that scope has returned._

13. **What is the event loop? How does JavaScript handle asynchronous code?**
    _JS is single-threaded. The event loop processes the call stack, then microtasks (promises), then macrotasks (setTimeout)._

14. **What is the difference between `==` and `===`?**
    _`==` coerces types before comparing. `===` checks value AND type without coercion. Prefer `===`._

15. **Explain `this` in JavaScript. How does it differ in arrow functions?**
    _`this` depends on how a function is called. Arrow functions inherit `this` from their enclosing scope._

16. **What are Promises? How do `async`/`await` work?**
    _Promises represent future values. `async`/`await` is syntactic sugar that makes promise chains read like synchronous code._

17. **What is the difference between `null` and `undefined`?**
    _`undefined`: variable declared but not assigned. `null`: intentionally empty value._

18. **What is event delegation and why is it useful?**
    _Attach one listener to a parent instead of one per child. Events bubble up; check `event.target`. Better performance for dynamic lists._

---

## Frameworks & Libraries

19. **What problem does React (or Vue/Angular) solve that plain JS doesn't?**
    _Declarative UI, component reuse, efficient DOM updates, state management._

20. **What is the virtual DOM? Why does React use it?**
    _A lightweight in-memory representation of the real DOM. React diffs it to minimize expensive DOM updates._

21. **Explain component lifecycle in React (or your preferred framework).**
    _Mount → Update → Unmount. In React: `useEffect` with dependencies handles side effects across these phases._

22. **What is state management? When would you reach for a state management library?**
    _Centralized data store. Useful when many components need the same data or when prop drilling gets unwieldy._

23. **What is server-side rendering (SSR)? When is it beneficial?**
    _HTML rendered on the server before sending to the client. Benefits: SEO, faster first paint, better for slow connections._

---

## Performance & Best Practices

24. **How would you diagnose a slow web page?**
    _Browser DevTools: Network tab (large assets), Performance tab (long tasks), Lighthouse audit._

25. **What is lazy loading and when would you use it?**
    _Defer loading resources until needed (images below fold, code-split routes). Reduces initial load time._

26. **Explain CORS. Why does the browser enforce it?**
    _Cross-Origin Resource Sharing. Browser blocks requests to different origins by default. Server must allow it with headers._

27. **What is the critical rendering path?**
    _HTML parse → DOM → CSSOM → render tree → layout → paint. Blocking CSS/JS delays first render._

28. **How do you handle browser compatibility issues?**
    _Feature detection (not user-agent sniffing), polyfills, autoprefixer, testing across browsers, progressive enhancement._

---

## Testing Frontend Code

29. **How would you test a React component?**
    _Unit: React Testing Library to render and assert. Integration: test component interactions. E2E: Cypress or Playwright._

30. **What is snapshot testing? When is it useful and when is it not?**
    _Captures rendered output and compares to saved snapshot. Good for catching unintended changes. Bad when output changes frequently._

---

## How to Study These

- If you don't use a framework yet, focus on HTML/CSS/JS Core first
- Build a small project to solidify each concept (a todo app, a weather widget)
- Use browser DevTools daily — open the console, inspect elements, profile performance
- Practice explaining concepts without jargon, as if to a non-technical person
