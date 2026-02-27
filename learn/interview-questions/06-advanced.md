# Advanced Interview Questions

Deeper questions on system design, scalability, distributed systems, design patterns, and architecture trade-offs — typically asked for mid-level and senior roles.

---

## System Design Fundamentals

1. **How would you design a system that needs to handle 10,000 requests per second?**
   _Load balancer → multiple app servers → database with read replicas → caching layer (Redis) → CDN for static assets. Horizontal scaling is key._

2. **Explain CAP theorem. What trade-offs does it force?**
   _Consistency, Availability, Partition tolerance — pick two. In practice, partitions happen, so you choose between consistency (CP) and availability (AP)._

3. **What is eventual consistency? When is it acceptable?**
   _Data converges to a consistent state over time (not instantly). Acceptable: social media feeds, analytics. Not acceptable: bank transfers._

4. **How would you design a rate limiter?**
   _Algorithms: token bucket, sliding window. Store counters per user/IP in Redis. Return 429 when limit exceeded. Consider distributed rate limiting across servers._

5. **Explain the trade-offs between SQL and NoSQL for a specific use case.**
   _E-commerce (SQL): strong schema, transactions, relationships. Real-time chat (NoSQL): flexible schema, fast writes, denormalized data._

---

## Scalability & Performance

6. **What is database sharding? When would you use it?**
   _Splitting data across multiple databases by a shard key (user ID, region). Use when a single database can't handle the load. Adds complexity._

7. **Explain read replicas. How do they improve performance?**
   _Copies of the primary database that handle read queries. Primary handles writes. Works when read:write ratio is high (most apps)._

8. **What is a CDN and how would you design content delivery for a global app?**
   _Edge servers worldwide caching static + dynamic content. Route users to nearest edge. Invalidation strategies: TTL, purge on update._

9. **How do you handle a thundering herd problem?**
   _Many requests hit the same expired cache key simultaneously. Solutions: cache stampede lock, staggered expiration, request coalescing._

10. **Explain connection pooling. Why is it important?**
    _Reuse database connections instead of opening/closing per request. Reduces overhead. Tools: PgBouncer (PostgreSQL), built-in ORM pools._

---

## Distributed Systems

11. **What is a distributed transaction? How do you maintain consistency across services?**
    _Transaction spanning multiple services. Patterns: two-phase commit (2PC), saga pattern (compensating transactions). Sagas are more common in microservices._

12. **Explain the saga pattern with an example.**
    _Order service → Payment service → Inventory service. If payment fails, compensating action reverses the order. Each step has a rollback action._

13. **What is a message broker? Compare RabbitMQ, Kafka, and SQS.**
    _RabbitMQ: traditional queue, delivery guarantees. Kafka: distributed log, high throughput, replay. SQS: managed, simple, no infra to manage._

14. **How do you handle partial failures in a microservices system?**
    _Circuit breaker pattern, retries with exponential backoff, fallback responses, bulkhead isolation, health checks._

15. **What is service discovery and why do microservices need it?**
    _Mechanism for services to find each other's addresses (Consul, Kubernetes DNS). Necessary because instances scale up/down dynamically._

---

## Design Patterns & Architecture

16. **Explain SOLID principles. Give an example of violating one.**
    _Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, Dependency Inversion. Violation: a class that handles both user auth and email sending (SRP)._

17. **What is the difference between composition and inheritance? When do you prefer each?**
    _Inheritance: "is-a" (Dog extends Animal). Composition: "has-a" (Car has an Engine). Prefer composition — it's more flexible and avoids deep hierarchies._

18. **Explain the Observer pattern. Where have you seen it?**
    _Subject notifies subscribers when state changes. Examples: event listeners in JS, pub/sub systems, React state updates._

19. **What is dependency injection and why is it useful?**
    _Pass dependencies into a class/function instead of creating them inside. Enables testing (mock dependencies), loose coupling._

20. **What is the strangler fig pattern?**
    _Incrementally replace a legacy system by routing features to the new system one by one while the old system still runs. Low-risk migration strategy._

---

## Data Engineering & Storage

21. **When would you use a relational database vs. a document store vs. a graph database?**
    _Relational: structured data with relationships (e-commerce). Document: flexible/nested data (CMS). Graph: complex relationships (social networks, recommendations)._

22. **Explain database indexing strategies. When can indexes hurt?**
    _B-tree (range queries), hash (exact lookups), composite (multi-column). Indexes slow down writes and use storage. Don't over-index._

23. **What is CQRS (Command Query Responsibility Segregation)?**
    _Separate read and write models. Write model optimized for data integrity, read model optimized for queries. Useful at scale but adds complexity._

24. **How do you handle data consistency between a cache and a database?**
    _Strategies: cache-aside (read: check cache, miss → query DB, populate cache), write-through (update both), write-behind (update cache, async write to DB)._

25. **What is event sourcing?**
    _Store events (facts) instead of current state. Rebuild state by replaying events. Benefits: full audit trail, time travel, event-driven architecture._

---

## Security at Scale

26. **How would you store passwords securely?**
    _Hash with bcrypt/argon2 (adaptive, with salt). NEVER store plain text. NEVER use fast hashes (MD5, SHA)._

27. **Explain the principle of least privilege. How do you apply it?**
    _Give each component only the permissions it needs. DB users with limited access, API keys scoped to specific actions, IAM roles._

28. **What is a DDoS attack? How would you mitigate one?**
    _Distributed Denial of Service: overwhelm with traffic. Mitigate: CDN/WAF (Cloudflare), rate limiting, auto-scaling, traffic analysis._

29. **How do you handle secrets management in a production system?**
    _Use a secrets manager (AWS Secrets Manager, HashiCorp Vault, environment variables in CI/CD). Never commit secrets to source control._

30. **What is zero-trust architecture?**
    _Never trust, always verify — even inside the network. Every request is authenticated and authorized. Micro-segmentation, mutual TLS._

---

## Answering System Design Questions

These tips apply to design questions at any level:

1. **Clarify requirements first** — ask about scale, users, features, constraints
2. **Start with a high-level diagram** — boxes and arrows, major components
3. **Identify the data model** — what are we storing, how is it structured?
4. **Walk through the main flows** — user creates a post, user reads a feed, etc.
5. **Discuss trade-offs explicitly** — "We could use X, but Y would be better here because..."
6. **Add depth where asked** — caching, database choice, failure handling
7. **It's OK to say "I don't know"** — followed by "but I'd research it by looking into..."

---

## How to Study These

- Start with the fundamentals (system design, scalability) before jumping to patterns
- Draw architecture diagrams by hand — it forces you to think about components and connections
- Read engineering blogs: Netflix, Uber, Stripe, and Cloudflare publish excellent deep dives
- Practice with classic design problems: URL shortener, chat system, Twitter feed, notification service
- Study one design pattern per week and find it in real codebases
- When using any tool (database, cache, queue), understand WHY you're using it, not just HOW

---

## Model Answers

### Model Answer: "Explain CAP theorem. What trade-offs does it force?" (#2)

> "CAP theorem states that a distributed system can only guarantee two of three properties simultaneously:
>
> - **Consistency** — every read receives the most recent write (all nodes see the same data at the same time)
> - **Availability** — every request receives a response, even if some nodes are down
> - **Partition Tolerance** — the system continues operating even if network communication between nodes drops
>
> In practice, network partitions WILL happen in distributed systems, so you're really choosing between CP and AP:
>
> - **CP (Consistency + Partition Tolerance):** During a partition, the system refuses to serve requests rather than risk returning stale data. Example: a banking system — you'd rather show an error than let someone overdraft because two nodes disagree on the balance. Tools: HBase, MongoDB (in default config), etcd.
>
> - **AP (Availability + Partition Tolerance):** During a partition, the system continues serving requests but some nodes may return stale data. Example: a social media feed — it's okay if a user sees a post a few seconds late rather than getting an error page. Tools: Cassandra, DynamoDB, CouchDB.
>
> Most real-world systems don't make a global CP/AP choice — they tune consistency per operation. For example, an e-commerce system might be CP for inventory counts (don't oversell) but AP for product recommendations (stale is fine)."

### Model Answer: "How would you design a rate limiter?" (#4)

> "A rate limiter controls how many requests a user or IP can make within a time window. Let me walk through the design.
>
> **Requirements:** Limit each user to 100 requests per minute. Return HTTP 429 (Too Many Requests) when exceeded.
>
> **Algorithm — Sliding Window Counter:**
> I'd use a sliding window approach in Redis. For each user, I maintain a sorted set where each member is a request timestamp.
>
> On each request:
> 1. Remove all entries older than 60 seconds from the sorted set
> 2. Count remaining entries
> 3. If count < 100: add current timestamp, allow request
> 4. If count ≥ 100: reject with 429 and a `Retry-After` header
>
> **Alternative algorithms:**
> - **Token Bucket:** Each user has a bucket that fills at a steady rate (e.g., 100 tokens/minute). Each request consumes a token. Simple, allows bursts up to bucket capacity.
> - **Fixed Window:** Count requests in fixed 1-minute windows. Simple but has a boundary problem — a user could make 100 requests at 0:59 and 100 at 1:01, hitting 200 in 2 seconds.
> - **Leaky Bucket:** Requests enter a queue processed at a fixed rate. Smooths traffic but adds latency.
>
> **Distributed rate limiting:** With multiple app servers, each server can't count independently. I'd use Redis as a shared counter — it's fast (in-memory), supports atomic operations (`INCR`, `EXPIRE`), and all servers see the same counts.
>
> **Implementation in practice:**
> I'd implement this as middleware that runs before the route handler. The middleware checks Redis, and either passes the request through or returns 429. I'd include rate limit headers in every response (`X-RateLimit-Remaining`, `X-RateLimit-Reset`) so clients can self-regulate."

### Model Answer: "What is the saga pattern? Give an example." (#12)

> "The saga pattern manages distributed transactions across multiple services by breaking them into a sequence of local transactions, each with a compensating action (rollback) if something fails.
>
> **Example — E-commerce order flow:**
>
> When a user places an order, three services are involved:
> 1. **Order Service** — creates the order record
> 2. **Payment Service** — charges the credit card
> 3. **Inventory Service** — reserves the items
>
> **Happy path:**
> ```
> Order Service: Create order (status: pending)
>   → Payment Service: Charge $50
>     → Inventory Service: Reserve 2 items
>       → Order Service: Update order (status: confirmed)
> ```
>
> **Failure path (payment fails):**
> ```
> Order Service: Create order (status: pending)
>   → Payment Service: Charge $50 — FAILS (insufficient funds)
>     → Compensating action: Order Service cancels the order
> ```
>
> **Failure path (inventory fails):**
> ```
> Order Service: Create order (status: pending)
>   → Payment Service: Charge $50 — succeeds
>     → Inventory Service: Reserve items — FAILS (out of stock)
>       → Compensating actions (reverse order):
>          Payment Service: Refund $50
>          Order Service: Cancel order
> ```
>
> There are two coordination approaches:
> - **Choreography:** Each service emits events and listens for events from others. Simpler but harder to trace the full flow.
> - **Orchestration:** A central saga coordinator tells each service what to do and handles failures. Easier to understand and debug, but the orchestrator is a single point of failure.
>
> The key advantage over a traditional distributed transaction (2PC) is that sagas don't hold locks across services, so they're more performant and resilient. The trade-off is that your system is in a temporarily inconsistent state during the saga — you need to design for that."
