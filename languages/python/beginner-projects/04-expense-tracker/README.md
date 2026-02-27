# Beginner Project 04: Expense Tracker

**Time:** 1–2 hours  
**Difficulty:** Beginner  
**Focus:** Planning data models, aggregation logic, formatted output, writing comments that document decisions and trade-offs

---

## Why This Project?

The expense tracker adds a layer of complexity beyond simple CRUD — you need to **aggregate and summarize data**. Computing totals by category, finding the biggest expense, and showing spending trends are the same operations you'll use in real backend work and SQL interviews. Planning HOW to compute these summaries is more important than the code itself.

---

## The Importance of Comments

For this project, focus on **algorithm comments** — explaining your approach to calculations and data processing.

### Example of a good algorithm comment:
```python
def get_spending_by_category(expenses):
    """..."""
    # Algorithm: single pass through the expenses list, accumulating
    # totals in a dictionary keyed by category name.
    #
    # Alternative considered: sort by category first, then group —
    # rejected because it's O(n log n) when we only need O(n).
    # The dictionary approach uses O(k) extra space where k = number
    # of unique categories, which is typically small (< 20).
    totals = {}
    for expense in expenses:
        category = expense["category"]
        # .get() returns 0 if the category hasn't been seen yet,
        # avoiding a KeyError without needing a separate if-check
        totals[category] = totals.get(category, 0) + expense["amount"]
    return totals
```

Notice: the comment explains the ALGORITHM (single pass accumulation), the ALTERNATIVE (sort + group), WHY the alternative was rejected (worse time complexity), and the SPACE TRADE-OFF (O(k)). This is interview-level thinking.

---

## Requirements

Build a command-line expense tracker that supports:

1. **Add** an expense (amount, category, description, date)
2. **List** all expenses (with filtering by category or date range)
3. **Summary** — show total spending, spending by category, and biggest expense
4. **Delete** an expense
5. **Persist** all data to a JSON file

### Categories (use these predefined categories):
- Food
- Transport
- Entertainment
- Shopping
- Bills
- Health
- Other

### Example session:

```
=== Expense Tracker ===
Loaded 12 expenses ($487.50 total)

Menu:
  1) Add expense
  2) List expenses
  3) View summary
  4) Delete expense
  5) Quit

Choice: 1
Amount: $24.50
Category (food/transport/entertainment/shopping/bills/health/other): food
Description: Lunch with team
Date (YYYY-MM-DD, Enter for today): 

Added: $24.50 — Food — "Lunch with team" (2026-02-27)

Choice: 3

=== Spending Summary ===
Total expenses:    $512.00 (13 transactions)
Average per item:  $39.38

By category:
  Food:           $156.00  ████████████░░░░░░░░ 30.5%
  Bills:          $145.00  ██████████░░░░░░░░░░ 28.3%
  Transport:       $89.00  ██████░░░░░░░░░░░░░░ 17.4%
  Entertainment:   $65.00  ████░░░░░░░░░░░░░░░░ 12.7%
  Shopping:        $42.00  ███░░░░░░░░░░░░░░░░░  8.2%
  Health:          $15.00  █░░░░░░░░░░░░░░░░░░░  2.9%

Biggest expense:   $85.00 — Bills — "Electric bill" (2026-02-01)

Choice: 2
Filter by category (Enter for all): food

┌────┬────────────┬───────────┬───────────┬───────────────────────┐
│ #  │ Date       │ Category  │ Amount    │ Description           │
├────┼────────────┼───────────┼───────────┼───────────────────────┤
│  1 │ 2026-02-27 │ Food      │ $24.50    │ Lunch with team       │
│  2 │ 2026-02-25 │ Food      │ $45.00    │ Groceries             │
│  3 │ 2026-02-20 │ Food      │ $12.50    │ Coffee shop           │
│  4 │ 2026-02-15 │ Food      │ $74.00    │ Weekly groceries      │
└────┴────────────┴───────────┴───────────┴───────────────────────┘
Food total: $156.00 (4 transactions)
```

---

## STOP — Plan Before You Code

Spend **15–20 minutes** planning. This is the most important part of the project.

### Planning Questions

1. **Data model for a single expense:**
   - What fields does it need? (amount, category, description, date — anything else?)
   - What type is each field? Should amount be float or int (cents)?
   - How will you represent the date? (string in "YYYY-MM-DD" format? a datetime object?)
   - **Write your choices and justify them.** For amount, consider:
     - Float: simple, but `0.1 + 0.2 = 0.30000000000000004` in Python!
     - Integer (cents): avoids floating point issues but you divide by 100 for display
     - For this project, float is fine — add a comment acknowledging the trade-off

2. **Data model for the expense collection:**
   - List of dictionaries with newest first? Oldest first?
   - Should each expense have a unique ID? (Yes — what happens when two expenses have the same amount, category, and description? You need to tell them apart for deletion.)
   - How will you generate IDs? (incrementing counter? UUID? max existing ID + 1?)

3. **Summary calculations — plan the algorithm BEFORE coding:**
   - Total: simple sum — what function/approach?
   - By category: how will you group and sum? (dictionary accumulation? `collections.Counter`? `itertools.groupby`?)
   - Biggest expense: `max()` with a key function? Manual loop?
   - **For each calculation, write the approach in pseudocode**

4. **Function inventory:**
   Plan at least 8–10 functions:
   - Data layer: load, save
   - Operations: add, delete, list (with optional filter)
   - Summaries: total, by-category, biggest
   - Display: format currency, format table row, print bar chart
   - Main: menu loop

5. **Display formatting plan:**
   - How will you format dollar amounts consistently? (`$24.50`, not `$24.5`)
   - How will you build the bar chart? (hint: `"█" * bar_length`)
   - How wide should the bars be? How do you scale them? (biggest category gets full bar, others proportional)

---

## Step-by-Step Instructions

### Step 1: Create the file and write your plan (15–20 minutes)

Create `expenses.py`. Write your planning block — **aim for 30+ lines** covering all decisions above. This planning block IS the most important deliverable of this project.

### Step 2: Define constants and the data layer (10 minutes)

```python
# === CONSTANTS ===
# Keeping valid categories in a constant tuple (not a list) because:
# 1. They shouldn't be modified at runtime — tuple signals immutability
# 2. Easy to validate user input against: `if category in CATEGORIES`
# 3. Single source of truth — if we add a category, we change one line

CATEGORIES = ("food", "transport", "entertainment", "shopping", "bills", "health", "other")

# Default file path — defined as a constant so it's easy to find and change.
# In a real app, this might come from a config file or environment variable.
DATA_FILE = "expenses.json"
```

Then write `load_expenses` and `save_expenses` following the same data-layer pattern from the Contact Book project.

**Test immediately:** Save a hardcoded list, reload it, print it. Confirm the round trip.

### Step 3: Write `add_expense` (10 minutes)

This function needs to:
1. Prompt for amount (validate it's a positive number)
2. Prompt for category (validate it's in the allowed list)
3. Prompt for description (any text is fine)
4. Prompt for date (default to today if the user presses Enter)
5. Generate a unique ID
6. Create the expense dictionary and append to the list
7. Save

**Comment requirements for this function:**
- Explain how you validate the amount (what inputs are rejected and why)
- Explain how you handle the date default
- Explain your ID generation strategy

```python
from datetime import date

def add_expense(expenses):
    """
    Prompt the user for expense details and add it to the list.

    Parameters:
        expenses (list[dict]): The current list of expense records.
            Modified in place — the new expense is appended.

    Returns:
        dict: The newly created expense record.

    Side effects:
        - Modifies the expenses list in place
        - Saves to the data file
        - Prints confirmation to the console

    Design note: This function handles both user input AND data creation.
    In a larger app, you'd separate these (one function for the UI prompt,
    one for creating the record). For this size project, combining them
    keeps the code shorter without sacrificing readability.
    """
    # TODO: implement
    pass
```

### Step 4: Write `list_expenses` with optional filtering (10 minutes)

Support these modes:
- No filter: show all expenses, newest first
- Filter by category: show only matching expenses
- Filter by date range (stretch goal): show expenses within a date range

```python
def list_expenses(expenses, category_filter=None):
    """
    Display expenses in a formatted table, optionally filtered by category.

    Parameters:
        expenses (list[dict]): All expenses.
        category_filter (str or None): If provided, only show this category.

    Returns:
        None — prints to console.

    Why the filter is a parameter and not a separate function:
        Filtering and displaying are tightly related here. Having one
        function with an optional parameter is simpler than having
        list_all_expenses() and list_expenses_by_category() with
        duplicated display logic. DRY principle — Don't Repeat Yourself.
    """
    # TODO: implement
    pass
```

### Step 5: Write the summary functions (15 minutes)

This is where your planning pays off. Implement:

**`get_total(expenses)`** — Return the sum of all amounts.
```python
# Using the built-in sum() with a generator expression.
# This is equivalent to a for loop but more Pythonic.
# Generator expressions are memory-efficient because they don't create
# an intermediate list — they yield one value at a time.
total = sum(e["amount"] for e in expenses)
```

**`get_by_category(expenses)`** — Return a dictionary of `{category: total}`.

Add an algorithm comment explaining your approach (see the example at the top of this README).

**`get_biggest(expenses)`** — Return the single largest expense.
```python
# Using max() with a key function to find the expense with the largest amount.
# key=lambda e: e["amount"] tells max() to compare expenses by their amount
# field, not by their default comparison (which would fail on dicts).
#
# Edge case: if expenses is empty, max() raises ValueError.
# We handle this by checking first and returning None.
```

**`show_summary(expenses)`** — Call the three functions above and format the output, including the bar chart.

```python
def show_summary(expenses):
    """
    Display a complete spending summary with bar chart.

    Includes:
        - Total spending and transaction count
        - Average expense amount
        - Category breakdown with proportional bar chart
        - Largest single expense

    The bar chart works by:
        1. Finding the largest category total (this gets the full bar width)
        2. Scaling all other categories proportionally
        3. Using █ (full block) characters for the filled portion
        4. Using ░ (light shade) characters for the empty portion
        This creates a visual representation that's instantly readable.
    """
    # TODO: implement
    pass
```

**Comment requirement:** The bar chart logic should have step-by-step comments explaining the math.

### Step 6: Write `delete_expense` (5 minutes)

Show the list, ask for the number to delete, confirm, then remove.

### Step 7: Main menu loop (5 minutes)

Same pattern as the Contact Book — while loop with numbered menu options.

### Step 8: Test and verify (10 minutes)

Test these scenarios:
- Add 5+ expenses across different categories → verify summary is correct
- Filter by category → verify totals match the summary
- Delete an expense → verify the summary updates
- Restart the program → verify all data persists
- Check the bar chart → verify the proportions look right
- Try invalid inputs: negative amounts, non-existent categories, bad dates

---

## Comment Checklist

- [ ] Planning block at the top (30+ lines) with data model choices and reasoning
- [ ] Constants have comments explaining why they're constants
- [ ] Data layer functions explain the repository pattern
- [ ] Every summary function has an algorithm comment explaining the approach
- [ ] At least one function documents an alternative approach that was considered and rejected
- [ ] The bar chart logic has step-by-step math comments
- [ ] Edge cases (empty list, missing file) have comments explaining how they're handled
- [ ] Every function has a complete docstring
- [ ] `if __name__ == "__main__"` guard present with comment

---

## Reflect on What You Learned

After finishing, write 2–3 sentences for EACH audience below. Describing data aggregation and algorithm choices at different levels is exactly what system design interviews test.

### To a friend (casual, no jargon)

> _"I built a thing that..."_
>
> Example: "I made a spending tracker that adds up your expenses by category and shows a little bar chart of where your money goes. It remembers everything you enter, even after you close it."

### To an employer (focus on skills and process)

> _"In this project I practiced..."_
>
> Example: "I practiced data aggregation — computing totals, averages, and category breakdowns from raw records. I documented my algorithm choices, including why I used dictionary accumulation over sort-and-group, and built formatted output with proportional bar charts."

### To a professor (technical, precise)

> _"This project demonstrates..."_
>
> Example: "This project demonstrates single-pass O(n) aggregation using dictionary accumulation, formatted console output with proportional visualization, JSON persistence, and thorough algorithm documentation. I analyzed time and space complexity of alternative approaches (sort-based grouping vs. hash-based) and justified my selection in inline comments."

**Write yours in a comment block at the bottom of your Python file:**
```python
# ============================================================
# WHAT I LEARNED
# ============================================================
# Friend:    ...
# Employer:  ...
# Professor: ...
# ============================================================
```

---

## Stretch Goals

1. Add date range filtering to `list_expenses` (comment on parsing and comparing dates)
2. Add a "monthly comparison" view — show this month vs. last month (comment on date arithmetic)
3. Add an "export to CSV" feature (comment: when would CSV be chosen over JSON in a real app?)
4. Let the user define custom categories that persist in the JSON file
