# Backend Interview Questions

Questions for backend and server-side engineering roles — APIs, databases, authentication, architecture, and infrastructure.

---

## APIs & Web Services

1. **What is a REST API? What are its key constraints?**
   _Representational State Transfer. Stateless, client-server, uniform interface, resource-based URLs, standard HTTP methods._

2. **Explain the main HTTP methods: GET, POST, PUT, PATCH, DELETE.**
   _GET: read. POST: create. PUT: full update/replace. PATCH: partial update. DELETE: remove._

3. **What are HTTP status codes? Give examples of 2xx, 4xx, and 5xx.**
   _2xx: success (200 OK, 201 Created). 4xx: client error (400 Bad Request, 404 Not Found). 5xx: server error (500 Internal Server Error)._

4. **What is the difference between REST and GraphQL?**
   _REST: multiple endpoints, fixed response shape. GraphQL: single endpoint, client requests exactly what it needs._

5. **What is middleware? Give an example.**
   _Code that runs between request and response (logging, auth checks, CORS headers). Express/Django use middleware extensively._

---

## Databases

6. **What is the difference between SQL and NoSQL databases?**
   _SQL: relational, structured schema, ACID (PostgreSQL, MySQL). NoSQL: flexible schema, various models — document, key-value, graph (MongoDB, Redis)._

7. **What is database normalization? Why does it matter?**
   _Organizing tables to reduce redundancy. Normal forms (1NF, 2NF, 3NF) prevent update anomalies._

8. **Explain primary keys, foreign keys, and indexes.**
   _Primary key: unique row identifier. Foreign key: links to another table's primary key. Index: speeds up queries on a column._

9. **What is an ORM? Name pros and cons.**
   _Object-Relational Mapping (SQLAlchemy, Prisma). Pro: write queries in your language. Con: can generate inefficient SQL, hides complexity._

10. **How would you handle database migrations in a production system?**
    _Use migration tools (Alembic, Flyway). Version control migrations. Test on staging first. Make backward-compatible changes._

---

## Authentication & Security

11. **Explain the difference between authentication and authorization.**
    _Authentication: "Who are you?" (login). Authorization: "What can you do?" (permissions/roles)._

12. **What is JWT? How does token-based auth work?**
    _JSON Web Token. Server creates a signed token on login. Client sends it with each request. Server verifies the signature._

13. **What is the difference between sessions and tokens?**
    _Sessions: server stores state (session ID in cookie). Tokens: stateless, client holds the token (JWT). Trade-off: memory vs. token size._

14. **What is HTTPS and why is it important?**
    _HTTP over TLS/SSL. Encrypts data in transit to prevent eavesdropping and tampering._

15. **Name 3 common security vulnerabilities and how to prevent them.**
    _SQL injection (parameterized queries), XSS (sanitize output), CSRF (tokens). See OWASP Top 10._

---

## Server Architecture

16. **What is the difference between monolithic and microservices architecture?**
    _Monolith: single deployable unit. Microservices: small, independent services communicating over the network. Trade-off: simplicity vs. scalability._

17. **Explain the request-response lifecycle in a web server.**
    _Client sends HTTP request → DNS → server receives → middleware → routing → handler logic → database query → build response → send back._

18. **What is caching? Name different levels of caching.**
    _Storing computed results to avoid re-computing. Levels: browser cache, CDN, application cache (Redis), database query cache._

19. **What is a message queue? When would you use one?**
    _Async communication between services (RabbitMQ, SQS). Use for: email sending, image processing, any task that can be deferred._

20. **What are environment variables and why should you use them?**
    _Config values set outside code (API keys, database URLs). Keeps secrets out of source control, enables different configs per environment._

---

## DevOps & Deployment Basics

21. **What is CI/CD? Why is it important?**
    _Continuous Integration: auto-run tests on every push. Continuous Deployment: auto-deploy passing builds. Catches bugs early, speeds delivery._

22. **What is Docker and why would you use it?**
    _Containerization platform. Packages app + dependencies into a portable image. "Works on my machine" solved._

23. **Explain the difference between horizontal and vertical scaling.**
    _Vertical: bigger machine (more RAM/CPU). Horizontal: more machines behind a load balancer. Horizontal scales further._

24. **What is a reverse proxy? Give an example.**
    _Server that sits in front of your app (Nginx, HAProxy). Handles SSL termination, load balancing, caching._

25. **What are logs and monitoring? What tools would you use?**
    _Logs: structured output from your app. Monitoring: track metrics/alerts. Tools: ELK stack, Prometheus/Grafana, Datadog._

---

## Data & Processing

26. **What is an API rate limiter and why would you implement one?**
    _Limits requests per user/IP over a time window. Prevents abuse, protects backend resources._

27. **What is pagination? How would you implement it?**
    _Returning data in chunks. Offset-based: `?page=2&limit=20`. Cursor-based: `?after=abc123` (better for large/changing datasets)._

28. **What is the N+1 query problem and how do you fix it?**
    _Fetching a list, then querying individually for each item's related data. Fix: eager loading / JOIN queries._

29. **Explain idempotency. Why is it important for APIs?**
    _Same request produces the same result no matter how many times it's called. Critical for retries (PUT, DELETE should be idempotent)._

30. **What is a webhook?**
    _Reverse API call — the server sends an HTTP request to YOUR endpoint when an event occurs (e.g., payment completed)._

---

## How to Study These

- Build a small API (Express, Flask, FastAPI) that implements CRUD + auth
- Use Postman or `curl` to test your endpoints
- Set up a local database and practice writing raw SQL before relying on an ORM
- Containerize your project with Docker
- Read through the OWASP Top 10 for security awareness

---

## Model Answers

### Model Answer: "What is a REST API? What are its key constraints?" (#1)

> "REST stands for Representational State Transfer. It's an architectural style for building APIs over HTTP where each URL represents a resource.
>
> The key constraints are:
> 1. **Client-Server** — frontend and backend are separate, connected only through the API
> 2. **Stateless** — each request contains all the information the server needs; the server doesn't remember previous requests
> 3. **Uniform Interface** — resources are identified by URLs, manipulated through standard HTTP methods (GET, POST, PUT, DELETE), and representations are often JSON
> 4. **Cacheable** — responses can indicate whether they're cacheable to improve performance
> 5. **Layered System** — client doesn't know if it's talking directly to the server or through a load balancer/proxy
>
> In practice, a RESTful API for a blog might look like:
> - `GET /api/posts` — list all posts
> - `GET /api/posts/42` — get post #42
> - `POST /api/posts` — create a new post (body contains the data)
> - `PUT /api/posts/42` — replace post #42
> - `DELETE /api/posts/42` — delete post #42
>
> The main benefit is that any client (web, mobile, CLI) can consume the same API because it follows predictable conventions."

### Model Answer: "What is JWT? How does token-based auth work?" (#12)

> "JWT stands for JSON Web Token. It's a compact, self-contained way to transmit authentication information between the client and server.
>
> Here's the flow:
> 1. User sends their credentials (username + password) to `POST /login`
> 2. Server verifies the credentials against the database (password checked against a bcrypt hash)
> 3. If valid, server creates a JWT containing a payload (user ID, role, expiration time) and signs it with a secret key
> 4. Server sends the JWT back to the client
> 5. Client stores it (usually in an httpOnly cookie or localStorage) and sends it in the `Authorization: Bearer <token>` header with every subsequent request
> 6. Server verifies the signature on each request — if valid, it trusts the payload without a database lookup
>
> A JWT has three parts separated by dots: `header.payload.signature`. The header specifies the algorithm (e.g., HS256). The payload contains claims (user data). The signature ensures the token hasn't been tampered with.
>
> The main advantage over sessions is that JWTs are stateless — the server doesn't need to store session data in memory or a database. The trade-off is that you can't easily revoke a JWT before it expires (unlike sessions where you just delete the server-side record). Common solutions are short expiration times with refresh tokens, or a token blacklist in Redis."

### Model Answer: "What is caching? Name different levels of caching." (#18)

> "Caching is storing the result of an expensive operation so you can serve it quickly on subsequent requests instead of recomputing it.
>
> There are several levels, from closest to the user to farthest:
>
> 1. **Browser cache** — the browser stores static assets (CSS, JS, images) based on `Cache-Control` and `ETag` headers. This is why refreshing a page is faster the second time.
> 2. **CDN cache** — edge servers like Cloudflare cache content at locations around the world, reducing latency for global users.
> 3. **Application cache** — an in-memory store like Redis or Memcached sitting in front of your database. You'd cache things like user session data, frequently accessed product listings, or computed leaderboards.
> 4. **Database query cache** — some databases (like MySQL) cache the results of repeated identical queries.
>
> The most common strategy I've used is cache-aside: the application checks Redis first, and on a miss, queries the database, stores the result in Redis with a TTL, and returns it. This works well for read-heavy data that doesn't change every second, like user profiles or configuration.
>
> The main challenge is cache invalidation — making sure stale data doesn't get served after an update. The classic joke is: 'There are only two hard things in computer science: cache invalidation and naming things.'"
