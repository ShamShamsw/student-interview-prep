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

---

## Learning Resources

- [System Design Primer (GitHub)](https://github.com/donnemartin/system-design-primer)

````
