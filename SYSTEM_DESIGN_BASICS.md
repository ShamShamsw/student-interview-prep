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

4. **Bottlenecks and scaling (10 min)**
   - "What breaks first when traffic increases?"
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

### 2. CAP Theorem (Simplified)

In a distributed system, you can only guarantee 2 of 3:

- **Consistency**: Every read gets the latest write
- **Availability**: Every request gets a response (no guarantee it's latest)
- **Partition Tolerance**: System works despite network failures

**Practical takeaway:**  
Since network failures happen, choose between:
- **CP**: Consistency + Partition Tolerance (e.g., banking systems)
- **AP**: Availability + Partition Tolerance (e.g., social media feeds)

### 3. Horizontal vs Vertical Scaling

| Vertical Scaling | Horizontal Scaling |
|------------------|-------------------|
| Add more CPU/RAM to one server | Add more servers |
| Simple, no code changes | Requires load balancing |
| Has hard limits | Nearly unlimited |
| Single point of failure | More resilient |

**When to use:**
- Start vertical (simpler)
- Scale horizontal when you hit limits (more robust)

### 4. Database Choices

| Use Case | Best Choice | Why |
|----------|-------------|-----|
| Structured data, ACID required | SQL (PostgreSQL, MySQL) | Transactions, relationships |
| Flexible schema, high write volume | NoSQL (MongoDB, Cassandra) | Scalability, speed |
| Key-value lookups | Redis, Memcached | Ultra-fast reads |
| Full-text search | Elasticsearch | Advanced search features |
| Time-series data | InfluxDB, TimescaleDB | Optimized for timestamps |

### 5. Caching Strategy

**When to cache:**
- Read-heavy workloads (reads >> writes)
- Expensive computations
- External API calls

**Common patterns:**

**Cache-Aside (Lazy Loading)**
```
1. Check cache
2. If miss, read from database
3. Store in cache for next time
```

**Write-Through**
```
1. Write to cache
2. Cache writes to database
3. Read always hits cache
```

**Cache Invalidation:**
- TTL (time to live): expire after X seconds
- Manual: clear cache when data updates
- LRU (Least Recently Used): evict oldest items

### 6. Load Balancing

Distribute requests across multiple servers.

**Algorithms:**
- **Round Robin**: A, B, C, A, B, C...
- **Least Connections**: Route to server with fewest active connections
- **Weighted**: Route more traffic to powerful servers

**Benefits:**
- No single point of failure
- Better resource utilization
- Easy to add/remove servers

---

## Common System Design Patterns

### Pattern 1: Read-Heavy System (e.g., News Feed)

```
┌──────────┐
│  Client  │
└────┬─────┘
     │
┌────▼──────────┐
│ Load Balancer │
└────┬──────────┘
     │
┌────▼────────┐      ┌──────────┐
│  Web Server ├─────►│  Cache   │
│  (API)      │◄─────┤ (Redis)  │
└────┬────────┘      └──────────┘
     │
┌────▼────────┐
│  Database   │
│ (read replicas)
└─────────────┘
```

**Key ideas:**
- Cache frequent reads
- Database read replicas for scaling
- CDN for static content

### Pattern 2: Write-Heavy System (e.g., Analytics)

```
┌──────────┐
│  Client  │
└────┬─────┘
     │
┌────▼──────────┐
│ Load Balancer │
└────┬──────────┘
     │
┌────▼────────┐      ┌──────────────┐
│  Web Server ├─────►│ Message Queue│
└─────────────┘      │ (RabbitMQ)   │
                     └──────┬───────┘
                            │
                     ┌──────▼───────┐
                     │   Workers    │
                     │ (async write)│
                     └──────┬───────┘
                            │
                     ┌──────▼───────┐
                     │   Database   │
                     └──────────────┘
```

**Key ideas:**
- Async processing with message queue
- Batch writes for efficiency
- Accept eventual consistency

### Pattern 3: Real-Time System (e.g., Chat)

```
┌──────────┐
│  Client  │
└────┬─────┘
     │ WebSocket
┌────▼──────────┐
│ WebSocket     │
│ Server        │
└────┬──────────┘
     │
┌────▼────────┐      ┌──────────┐
│  Pub/Sub    ├─────►│  Cache   │
│  (Redis)    │      │          │
└─────────────┘      └──────────┘
     │
┌────▼────────┐
│  Database   │
└─────────────┘
```

**Key ideas:**
- WebSocket for bidirectional communication
- Pub/Sub for message broadcasting
- Keep messages in memory for speed

---

## API Design Patterns

### RESTful API Basics

```
GET    /users          - List all users
GET    /users/{id}     - Get one user
POST   /users          - Create user
PUT    /users/{id}     - Update user
DELETE /users/{id}     - Delete user
```

**Best practices:**
- Use nouns, not verbs (`/users` not `/getUsers`)
- Plural names (`/users` not `/user`)
- Versioning: `/v1/users`
- HTTP status codes: 200 OK, 201 Created, 400 Bad Request, 404 Not Found, 500 Error

### Rate Limiting

Prevent abuse by limiting requests per user.

**Algorithms:**
- **Fixed Window**: 100 requests per minute
- **Sliding Window**: More accurate, tracks rolling time
- **Token Bucket**: Allow bursts, refill tokens over time

**Response:**
```
HTTP 429 Too Many Requests
Retry-After: 60
```

---

## Beginner System Design Exercises

### Exercise 1: URL Shortener (Easy)

**Requirements:**
- Convert long URL to short code (e.g., `bit.ly/abc123`)
- Redirect short code to original URL
- Track click count

**Questions to answer:**
1. How do you generate unique short codes?
2. What database schema do you need?
3. How do you handle 1 million requests/day?

<details>
<summary>Click for hints</summary>

- Use base62 encoding (a-z, A-Z, 0-9) for short codes
- Schema: `id, short_code, original_url, created_at, click_count`
- Caching: Store popular URLs in Redis
- Database: Single PostgreSQL server is enough for 1M/day
</details>

### Exercise 2: Image Upload Service (Medium)

**Requirements:**
- Users upload images
- Images are resized to thumbnails
- Users can view/download images

**Questions to answer:**
1. Where do you store images?
2. How do you handle large file uploads?
3. How do you generate thumbnails efficiently?

<details>
<summary>Click for hints</summary>

- Storage: S3 or similar object storage (not database)
- Upload: Direct to S3 with presigned URL
- Thumbnails: Background worker processes after upload
- Database: Store only metadata (S3 key, size, user_id)
</details>

### Exercise 3: Leaderboard System (Medium)

**Requirements:**
- Track user scores
- Show top 100 users in real-time
- Handle 10,000 score updates/second

**Questions to answer:**
1. What data structure stores the leaderboard?
2. How do you update scores efficiently?
3. How do you handle ties?

<details>
<summary>Click for hints</summary>

- Data structure: Redis Sorted Set (O(log n) updates)
- Commands: ZADD, ZRANGE, ZRANK
- Ties: Use timestamp as tiebreaker
- Partitioning: Split by region if global scale
</details>

### Exercise 4: Notification System (Hard)

**Requirements:**
- Send notifications via email, SMS, push
- Users can set preferences (what to receive)
- Handle 1 million notifications/hour

**Questions to answer:**
1. How do you queue notifications?
2. How do you handle failures (email bounces)?
3. How do you prevent duplicate sends?

<details>
<summary>Click for hints</summary>

- Queue: Kafka or RabbitMQ for reliability
- Workers: Process queue async, retry on failure
- Deduplication: Store notification IDs in cache (24 hour TTL)
- Preferences: Check user settings before sending
- Vendors: Use SendGrid (email), Twilio (SMS), FCM (push)
</details>

---

## Tradeoffs to Discuss

Interviewers love when you discuss tradeoffs. Here are common ones:

| Scenario | Option A | Option B | Consider |
|----------|----------|----------|----------|
| Data storage | SQL | NoSQL | Consistency needs, query patterns |
| Caching | Cache-aside | Write-through | Read/write ratio, consistency |
| Scaling | Vertical | Horizontal | Cost, limits, complexity |
| Consistency | Strong | Eventual | User experience, business rules |
| Architecture | Monolith | Microservices | Team size, deployment frequency |

**Template:**  
"I'd choose [Option A] because [reason]. The tradeoff is [downside], which is acceptable given [requirements]. If [requirement changes], I'd switch to [Option B]."

---

## System Design Checklist

Use this during interviews:

- [ ] Clarified functional requirements
- [ ] Clarified non-functional requirements (users, QPS, latency)
- [ ] Estimated capacity (storage, bandwidth)
- [ ] Defined API contracts
- [ ] Drew high-level architecture diagram
- [ ] Chose appropriate database(s)
- [ ] Planned for caching
- [ ] Discussed scaling strategy
- [ ] Identified bottlenecks
- [ ] Proposed monitoring/alerting

---

## Learning Resources

- [System Design Primer (GitHub)](https://github.com/donnemartin/system-design-primer) - Comprehensive free resource
- [Grokking the System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview) - Paid but popular
- [ByteByteGo YouTube](https://www.youtube.com/@ByteByteGo) - Visual explanations
- [High Scalability Blog](http://highscalability.com/) - Real-world case studies

---

## Next Steps

1. Pick one exercise above and design it end-to-end (30 minutes)
2. Draw your architecture on paper or whiteboard
3. Explain your design out loud
4. Write down what you'd do differently if traffic 10x
5. Repeat with a different exercise weekly

Track progress in your [LEARNING_PATH_CHECKLIST.md](LEARNING_PATH_CHECKLIST.md).
