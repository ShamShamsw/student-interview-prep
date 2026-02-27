````markdown
# System Design Basics (Beginner-Friendly)

Learn the fundamentals of designing scalable systems — essential for many technical interviews.

## What is system design?

System design is about architecting software systems to meet specific requirements:
- Handle many users (scalability)
- Stay available during failures (reliability)
- Respond quickly (performance)
- Easy to maintain (simplicity)

## When you'll need this

- Mid-level and senior interviews
- Full-stack or backend roles
- Architecture discussions in your projects

## This guide covers

1. How to approach system design questions
2. Key concepts and tradeoffs
3. Common patterns
4. Beginner-friendly exercises

---

## System Design Interview Format

**Typical flow (45 minutes)**

1. **Clarify requirements (5 min)**
   - Functional: What features must it have?
   - Non-functional: How many users? How fast? How reliable?

2. **High-level design (10 min)**
   - Draw boxes: client, server, database, cache
   - Show data flow with arrows

3. **Deep dive (20 min)**
   - Pick 2-3 components to discuss in detail
   - Explain API contracts, data models, algorithms

4. **Bottlenecks and scaling (10 min)**n+   - "What breaks first when traffic increases?"
   - Propose solutions: caching, load balancing, replication

---

## Key Concepts

### 1. Back-of-Envelope Calculations

Estimate system capacity needs quickly.

**Common numbers to memorize:**
- 1 million requests per day ≈ 12 requests/second
- 1 billion requests per day ≈ 12,000 requests/second
- Storage: 1 character ≈ 1 byte
- Typical web request: 1-10 KB
- Typical image: 100 KB - 1 MB
- Video (1 min, 720p): ~10-50 MB

**Example:**  
Q: How much storage for 10 million users posting 1 photo/week for 1 year?  
A: 10M users × 1 photo/week × 52 weeks/year × 500 KB/photo = 260 TB

### 2. Load Balancers

A load balancer distributes incoming traffic across multiple servers so no single server is overwhelmed.

**Why it matters:**
- Increases availability — if one server dies, traffic is sent to healthy ones
- Enables horizontal scaling — add more servers behind the balancer
- Can handle SSL termination, saving backend servers CPU time

**Common strategies:**
| Strategy | How it works | Best for |
|----------|-------------|----------|
| Round Robin | Requests go to each server in turn | Equal-capacity servers |
| Least Connections | Routes to the server with fewest active connections | Variable request durations |
| IP Hash | Same client IP always goes to the same server | Session affinity needs |
| Weighted | Servers with more capacity get more traffic | Mixed hardware |

**Tools:** Nginx, HAProxy, AWS ALB/NLB, Cloudflare

### 3. Caching

Caching stores frequently accessed data in a faster layer so you don't recompute or re-fetch it every time.

**Cache levels (closest to user → farthest):**
1. **Browser cache** — static assets (images, CSS, JS) with `Cache-Control` headers
2. **CDN cache** — edge servers worldwide (Cloudflare, CloudFront)
3. **Application cache** — in-memory store like Redis or Memcached
4. **Database query cache** — the database caches repeated query results

**Common caching strategies:**

| Strategy | How it works | Trade-off |
|----------|-------------|-----------|
| Cache-aside | App checks cache → miss → query DB → populate cache | Simple; cache can become stale |
| Write-through | Write to cache AND DB at the same time | Consistent; slower writes |
| Write-behind | Write to cache, async write to DB later | Fast writes; risk of data loss |
| Read-through | Cache itself fetches from DB on miss | Clean app code; cache must support it |

**When to cache:** Read-heavy data that changes infrequently (user profiles, product listings, config).  
**When NOT to cache:** Rapidly changing data, security-sensitive data, data that must be real-time.

### 4. Databases

**Relational (SQL):** PostgreSQL, MySQL
- Structured schema with tables, rows, columns
- ACID transactions (Atomicity, Consistency, Isolation, Durability)
- Great for: e-commerce, banking, anything with clear relationships
- Use JOINs to connect related data

**Non-relational (NoSQL):**
| Type | Examples | Best for |
|------|----------|----------|
| Document | MongoDB, Firestore | Flexible/nested data (CMS, user profiles) |
| Key-Value | Redis, DynamoDB | Simple lookups, caching, sessions |
| Column-Family | Cassandra, HBase | Write-heavy analytics, time-series |
| Graph | Neo4j, Amazon Neptune | Social networks, recommendation engines |

**Key concepts:**
- **Indexing:** Create indexes on frequently queried columns for faster lookups (B-tree for range queries, hash for exact match)
- **Replication:** Copy data to read replicas for higher read throughput
- **Sharding:** Split data across databases by a shard key (user ID, region) for horizontal scale
- **Normalization vs. Denormalization:** Normalized = less redundancy, more JOINs. Denormalized = faster reads, more storage.

### 5. CDN (Content Delivery Network)

A CDN caches static content on servers distributed around the world, closer to users.

**How it works:**
1. User requests an image from `cdn.example.com`
2. CDN routes request to the nearest edge server
3. If cached → serve immediately (fast!)
4. If not cached → fetch from origin server, cache it, then serve

**What to put on a CDN:** Images, CSS, JS bundles, videos, fonts, static HTML pages.

**Key decisions:**
- **TTL (Time to Live):** How long before cache expires? Short TTL = fresher content. Long TTL = better performance.
- **Invalidation:** How to update content? Purge specific files, or use versioned filenames (`app.v2.js`).

**Tools:** Cloudflare, AWS CloudFront, Fastly, Akamai

### 6. DNS (Domain Name System)

DNS translates human-readable domain names (like `example.com`) to IP addresses (like `93.184.216.34`).

**Lookup flow:**
1. Browser checks local cache
2. OS checks its cache
3. Query recursive DNS resolver (ISP or 8.8.8.8)
4. Resolver queries root → TLD (.com) → authoritative nameserver
5. IP address returned and cached at each level

**In system design, DNS matters for:**
- Routing users to the nearest data center (GeoDNS)
- Failover — DNS can route away from unhealthy servers
- Load distribution across multiple IPs

### 7. Message Queues

A message queue lets services communicate asynchronously — the sender puts a message on the queue, and the receiver processes it when ready.

**Why use one:**
- **Decouple services** — sender doesn't need to know about the receiver
- **Handle traffic spikes** — queue absorbs bursts, workers process at their own pace
- **Retry failed work** — messages stay on the queue until successfully processed

**Common tools:**
| Tool | Strengths |
|------|-----------|
| RabbitMQ | Flexible routing, delivery guarantees, multiple protocols |
| Apache Kafka | High throughput, distributed log, message replay, event streaming |
| AWS SQS | Fully managed, zero infra, simple dead-letter queues |
| Redis Streams | Lightweight, good if you already use Redis |

**Use cases:** Sending emails, processing image uploads, order fulfillment, log aggregation.

---

## Common Patterns

### Client-Server

The most fundamental pattern. A client (browser, mobile app) sends requests to a server, which processes them and returns responses.

```
[Client] ---HTTP Request---> [Server] ---Query---> [Database]
[Client] <--HTTP Response--- [Server] <--Result--- [Database]
```

### Pub/Sub (Publish-Subscribe)

Publishers send messages to topics without knowing who's listening. Subscribers listen to topics they care about.

**Example:** An e-commerce app publishes an "order.placed" event. The inventory service, email service, and analytics service all subscribe independently.

**Tools:** Kafka topics, Redis Pub/Sub, Google Cloud Pub/Sub, AWS SNS.

### Microservices

Break a large application into small, independently deployable services that communicate over the network.

| Aspect | Monolith | Microservices |
|--------|----------|---------------|
| Deployment | One big deploy | Deploy each service independently |
| Scaling | Scale everything together | Scale only what's needed |
| Complexity | Simple to start | More operational overhead (networking, monitoring) |
| Team structure | Everyone works on one codebase | Teams own individual services |

**When to use:** When your team and product are large enough that independent deployment and scaling matter. Don't start with microservices — earn your complexity.

### Event-Driven Architecture

Components communicate through events rather than direct calls. When something happens (user signs up, order placed), an event is emitted, and interested services react.

**Benefits:**
- Loose coupling between services
- Easy to add new reactions without changing the source
- Natural fit for async workflows

**Example flow:**
```
User signs up → "user.created" event emitted
  → Email service sends welcome email
  → Analytics service records signup
  → Recommendation service creates initial profile
```

### API Gateway

A single entry point that routes requests to the appropriate backend service. Handles cross-cutting concerns like auth, rate limiting, and logging.

```
[Client] → [API Gateway] → [User Service]
                          → [Order Service]
                          → [Product Service]
```

**Tools:** Kong, AWS API Gateway, Nginx as a gateway.

---

## Beginner-Friendly Exercises

Practice thinking through these designs. Don't worry about getting them perfect — focus on the process.

### Exercise 1: Design a URL Shortener

**Requirements:** User pastes a long URL, gets a short URL. Clicking the short URL redirects to the original.

**Think about:**
- How do you generate short codes? (hash, counter, random)
- Where do you store the mapping? (database table: short_code → original_url)
- How does redirect work? (look up code → 301/302 redirect)
- What about duplicate URLs? (same URL gets same short code, or a new one each time?)
- How would you handle 1 million URLs/day? (caching popular redirects, database indexing)

### Exercise 2: Design a Paste Bin

**Requirements:** User pastes text, gets a shareable link. Optional: expiration, syntax highlighting.

**Think about:**
- Storage: database for metadata, object storage (S3) for large pastes
- Access patterns: write once, read many → cache heavily
- Expiration: TTL field, background job to clean up expired pastes
- Abuse prevention: rate limiting, content size limits

### Exercise 3: Design a Simple Chat Application

**Requirements:** Two users can send messages to each other in real time.

**Think about:**
- Protocol: WebSockets for real-time, HTTP for history
- Message storage: database for persistence, in-memory for active connections
- Online status: heartbeat/ping mechanism
- Scaling: how do you route messages when users are on different servers? (message broker)

### Exercise 4: Design a Basic Notification System

**Requirements:** Send push, email, and SMS notifications. Users can set preferences.

**Think about:**
- User preferences table: which channels are enabled per user
- Message queue: decouple notification creation from delivery
- Multiple providers: email (SendGrid), SMS (Twilio), push (Firebase)
- Retry logic: what if a provider is temporarily down?
- Rate limiting: don't spam users

### Exercise 5: Design a File Storage Service (like Dropbox)

**Requirements:** Upload, download, and share files. Sync across devices.

**Think about:**
- Upload: chunked upload for large files, resumable
- Storage: object storage (S3) for files, database for metadata
- Sync: track file versions, detect changes, conflict resolution
- Sharing: access control lists (ACLs), shareable links with permissions

---

## Quick Reference: System Design Building Blocks

| Component | What it does | When to use it |
|-----------|-------------|----------------|
| Load Balancer | Distributes traffic across servers | Multiple server instances |
| Cache (Redis) | Stores frequently accessed data in memory | Read-heavy workloads |
| CDN | Serves static assets from edge locations | Global users, static content |
| Message Queue | Async communication between services | Decoupling, background jobs |
| Database (SQL) | Structured data with relationships | Transactions, complex queries |
| Database (NoSQL) | Flexible schema, horizontal scale | High write volume, unstructured data |
| API Gateway | Single entry point for multiple services | Microservices architecture |
| DNS | Domain name → IP address resolution | Every web application |
| Object Storage (S3) | Store large files (images, videos) | User uploads, backups |
| Search Engine | Full-text search (Elasticsearch) | Search features, log analysis |

---

## Learning Resources

- [System Design Primer (GitHub)](https://github.com/donnemartin/system-design-primer) — comprehensive open-source guide
- [ByteByteGo](https://bytebytego.com/) — visual system design explanations
- [Grokking System Design](https://www.designgurus.io/course/grokking-the-system-design-interview) — structured interview prep course
- [Designing Data-Intensive Applications](https://dataintensive.net/) — the definitive book on distributed systems
- [High Scalability Blog](http://highscalability.com/) — real-world architecture case studies

````
