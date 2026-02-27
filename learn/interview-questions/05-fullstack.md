# Fullstack Interview Questions

Questions that bridge frontend and backend — end-to-end architecture, integration, deployment, and how all the pieces fit together.

---

## End-to-End Architecture

1. **Walk through what happens when a user types a URL into their browser and presses Enter.**
   _DNS lookup → TCP connection → TLS handshake → HTTP request → server processes → response → browser parses HTML/CSS/JS → renders page._

2. **How do the frontend and backend communicate in a typical web app?**
   _Frontend sends HTTP requests (fetch/axios) to backend API endpoints. Backend processes, queries database, returns JSON._

3. **What is the difference between server-side rendering (SSR), client-side rendering (CSR), and static site generation (SSG)?**
   _SSR: HTML built per-request on server. CSR: blank HTML, JS builds page in browser. SSG: HTML built at build time. Trade-offs: SEO, speed, freshness._

4. **How would you structure a fullstack project's codebase?**
   _Common patterns: monorepo (frontend + backend in one repo) or separate repos. Clear separation of concerns — `/client`, `/server`, `/shared`._

5. **What is an API contract and why should frontend/backend teams agree on one?**
   _A shared definition of endpoints, request/response shapes, and status codes. Prevents integration surprises. Tools: OpenAPI/Swagger._

---

## Data Flow & State

6. **How do you decide what data lives on the client vs. the server?**
   _Server: source of truth, sensitive data, shared state. Client: UI state, optimistic updates, cached copies._

7. **What are cookies, localStorage, and sessionStorage? When would you use each?**
   _Cookies: sent with every request, good for auth. localStorage: persists, 5-10 MB. sessionStorage: cleared on tab close. Never store secrets in any._

8. **What is optimistic UI updating?**
   _Update the UI immediately (assume success), then reconcile if the server returns an error. Makes apps feel faster._

9. **How would you handle form validation across frontend and backend?**
   _Validate on BOTH. Frontend: instant feedback, better UX. Backend: security, never trust client input._

10. **What is the difference between real-time and polling-based updates?**
    _Polling: client repeatedly asks server ("any new data?"). Real-time: server pushes to client (WebSockets, SSE). Real-time is more efficient for frequent updates._

---

## Authentication in Practice

11. **Walk through implementing user signup and login in a fullstack app.**
    _Signup: validate input → hash password (bcrypt) → store in DB. Login: check credentials → create token/session → return to client → client stores and sends with requests._

12. **How do you protect a route that requires authentication?**
    _Backend: middleware checks for valid token/session before handler runs. Frontend: route guard redirects unauthenticated users to login._

13. **What is OAuth and when would you use "Sign in with Google/GitHub"?**
    _OAuth: delegated authentication. User authenticates with provider, provider gives your app a token. Use for: convenience, no password management._

14. **How do you handle user roles and permissions across the stack?**
    _Backend: role-based access control (RBAC) enforced in middleware. Frontend: hide/show UI elements based on role (but NEVER rely on it for security)._

---

## Deployment & Infrastructure

15. **How would you deploy a fullstack application?**
    _Common: frontend static files on CDN/Vercel/Netlify, backend on cloud (Heroku, Railway, AWS). Or: single deployment (Next.js, containerized with Docker)._

16. **What is the difference between development, staging, and production environments?**
    _Dev: local, debug mode. Staging: production-like for QA. Production: live, optimized. Use environment variables to swap configs._

17. **What is CORS and how do you configure it in a fullstack app?**
    _Browser blocks cross-origin requests. Configure backend to allow frontend's origin in `Access-Control-Allow-Origin` header._

18. **How do you manage environment variables across frontend and backend?**
    _Backend: `.env` file + dotenv library. Frontend: build tool injects (NEXT_PUBLIC_, VITE_). NEVER expose secrets to the client bundle._

19. **What is a CDN and how does it improve your app's performance?**
    _Content Delivery Network caches assets at edge locations worldwide. Reduces latency for static files (images, CSS, JS)._

---

## Testing Across the Stack

20. **How would you test a fullstack feature end-to-end?**
    _E2E test (Cypress/Playwright): simulate real user flow — fill form, submit, verify DB change, check UI update._

21. **What is integration testing vs. unit testing? Where do you draw the line?**
    _Unit: one function in isolation. Integration: multiple parts working together (API route + database). Integration catches wiring bugs unit tests miss._

22. **How do you mock an API for frontend development before the backend is ready?**
    _Mock server (MSW, json-server), hardcoded fixtures, or tools like Postman mock servers. Develop against the agreed API contract._

---

## Debugging & Problem-Solving

23. **A user reports "the page is blank." How do you debug it?**
    _Check: console errors (JS crash?), network tab (API failing?), server logs (500 error?), deployment (latest code live?). Reproduce step-by-step._

24. **The API is slow. How would you investigate?**
    _Check: database queries (N+1, missing index?), network latency, payload size, server resources, caching opportunities._

25. **How do you handle errors gracefully across the stack?**
    _Backend: consistent error response format, proper status codes, logging. Frontend: error boundaries, user-friendly messages, retry logic._

---

## System Design (Fullstack Scope)

26. **Design a simple URL shortener. What components do you need?**
    _Frontend: input form + redirect page. Backend: generate short code, store mapping in DB. Redirect: look up code → 301 redirect to original URL._

27. **Design a basic chat application. What technologies would you use?**
    _WebSockets for real-time messaging. Backend: Node/Python server, database for history. Frontend: message list, input box, connection management._

28. **How would you implement file uploads in a web app?**
    _Frontend: form with `<input type="file">`, multipart/form-data. Backend: receive file, validate (type, size), store (disk or S3). Return URL._

29. **Design a notification system. How do you handle real-time delivery?**
    _Server-sent events or WebSockets for push notifications. Fallback: polling. Store in DB for history. Mark read/unread._

30. **How would you implement search functionality for a content-heavy site?**
    _Simple: SQL LIKE / ILIKE queries. Better: full-text search (PostgreSQL tsvector, Elasticsearch). Frontend: debounced input, result highlighting._

---

## How to Study These

- Build a complete project with frontend + backend + database + auth
- Practice deploying it — the deployment process teaches you more than you expect
- Draw architecture diagrams on paper before coding
- When something breaks, trace the full request from browser → server → database and back
- Read production incident postmortems — they teach fullstack thinking
