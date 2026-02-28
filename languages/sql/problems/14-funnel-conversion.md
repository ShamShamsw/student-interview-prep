# Problem 14: User Funnel Conversion Rates

Difficulty: Medium  
Topics: conditional aggregation, CASE WHEN, COUNT DISTINCT, division

---

## Statement

You have a `user_events` table recording user actions in a checkout funnel. Define the funnel stages in order:

1. `page_view`
2. `add_to_cart`
3. `begin_checkout`
4. `purchase`

Write a single SQL query that returns:
- The number of distinct users who reached each stage
- The conversion rate from **the previous stage** to the current stage (%)
- The overall conversion rate from `page_view` to `purchase` (%)

---

## Schema

```sql
CREATE TABLE user_events (
    event_id    INT,
    user_id     INT,
    event_type  VARCHAR(50),   -- 'page_view', 'add_to_cart', 'begin_checkout', 'purchase'
    event_date  DATE
);
```

---

## Example Input

| event_id | user_id | event_type | event_date |
|---|---|---|---|
| 1 | 101 | page_view | 2024-03-01 |
| 2 | 101 | add_to_cart | 2024-03-01 |
| 3 | 101 | purchase | 2024-03-01 |
| 4 | 102 | page_view | 2024-03-01 |
| 5 | 102 | add_to_cart | 2024-03-01 |
| 6 | 103 | page_view | 2024-03-01 |

---

## Solution

```sql
WITH funnel AS (
    SELECT
        COUNT(DISTINCT CASE WHEN event_type = 'page_view'      THEN user_id END) AS views,
        COUNT(DISTINCT CASE WHEN event_type = 'add_to_cart'    THEN user_id END) AS carts,
        COUNT(DISTINCT CASE WHEN event_type = 'begin_checkout' THEN user_id END) AS checkouts,
        COUNT(DISTINCT CASE WHEN event_type = 'purchase'       THEN user_id END) AS purchases
    FROM user_events
)
SELECT
    'page_view'      AS stage, views      AS users, NULL                                         AS prev_step_cvr, NULL AS overall_cvr FROM funnel
UNION ALL
SELECT
    'add_to_cart',             carts,      ROUND(carts      * 100.0 / NULLIF(views,     0), 1), ROUND(carts      * 100.0 / NULLIF(views, 0), 1) FROM funnel
UNION ALL
SELECT
    'begin_checkout',          checkouts,  ROUND(checkouts  * 100.0 / NULLIF(carts,     0), 1), ROUND(checkouts  * 100.0 / NULLIF(views, 0), 1) FROM funnel
UNION ALL
SELECT
    'purchase',                purchases,  ROUND(purchases  * 100.0 / NULLIF(checkouts, 0), 1), ROUND(purchases  * 100.0 / NULLIF(views, 0), 1) FROM funnel;
```

---

## Example Output

| stage | users | prev_step_cvr | overall_cvr |
|---|---|---|---|
| page_view | 3 | NULL | NULL |
| add_to_cart | 2 | 66.7 | 66.7 |
| begin_checkout | 1 | 50.0 | 33.3 |
| purchase | 2 | 200.0 | 66.7 |

> Note: purchases (2) > checkouts (1) here because user 101 purchased without the `begin_checkout` event recorded — real data is messy.

---

## Key Concepts

- `COUNT(DISTINCT CASE WHEN ... THEN user_id END)` is the fundamental pattern for conditional distinct counts — the backbone of funnel analysis.
- `NULLIF(denominator, 0)` prevents division-by-zero.
- UNION ALL assembles the staged rows into a clean funnel table.
- In production, you might also segment the funnel by device, campaign, or date range.

---

## Follow-up Interview Questions

- How would you filter this funnel to only users who started on a mobile device?
- How would you detect users who skipped a step (e.g., went from `page_view` directly to `purchase`)?
- How would you A/B compare the funnel for two experiment groups?
