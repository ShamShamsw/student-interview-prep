# Beginner Project 05: Student Grade Report

**Time:** 1.5–2 hours  
**Difficulty:** Beginner+  
**Focus:** End-to-end planning, multi-module architecture, reading from files, formatted reports, thorough documentation as if writing for a teammate

---

## Why This Project?

This is the capstone of the beginner projects. You'll read data from a file, process it through several stages, and produce a polished report. This mirrors real-world data pipelines — **Extract, Transform, Report**. The project is intentionally larger to exercise your ability to plan an entire system from scratch, decompose it into clean functions, and write comments that someone else could follow without talking to you.

---

## The Importance of Comments

For this project, write comments as if **a teammate will maintain your code after you leave.** This is the most common real-world commenting scenario and exactly what interviewers are evaluating.

### Three levels of documentation this project requires:

**Level 1 — Module-level docstrings** (one per file):
```python
"""
grade_report.py — Student Grade Report Generator

Reads student grade data from a CSV file, computes individual and class-wide
statistics, assigns letter grades, and produces a formatted report.

Usage:
    python grade_report.py                    # uses default grades.csv
    python grade_report.py my_grades.csv      # uses a custom file

Data format:
    The input CSV must have these columns:
        student_name, assignment_name, score, max_score
    Scores are raw points (not percentages). This program converts to
    percentages internally for all calculations.

Author: [Your Name]
Date: [Date]
"""
```

**Level 2 — Section separators** showing the architecture at a glance:
```python
# ============================================================
# DATA LOADING
# ============================================================

# ... data loading functions ...

# ============================================================
# CALCULATIONS
# ============================================================

# ... calculation functions ...

# ============================================================
# REPORT GENERATION
# ============================================================

# ... report functions ...
```

**Level 3 — Inline comments** explaining WHY, not WHAT:
```python
# Good: explains WHY
# Round to one decimal place for display — more precision implies
# false accuracy since assignments are graded in whole points
percentage = round(total_earned / total_possible * 100, 1)

# Bad: explains WHAT (the code already says this)
# Calculate the percentage
percentage = round(total_earned / total_possible * 100, 1)
```

---

## Requirements

### Input: CSV data file

Create a sample `grades.csv` file your program will read:

```
student_name,assignment_name,score,max_score
Alice,Homework 1,45,50
Alice,Homework 2,38,50
Alice,Midterm,82,100
Alice,Project,90,100
Alice,Final,88,100
Bob,Homework 1,50,50
Bob,Homework 2,42,50
Bob,Midterm,71,100
Bob,Project,65,100
Bob,Final,73,100
Charlie,Homework 1,30,50
Charlie,Homework 2,28,50
Charlie,Midterm,55,100
Charlie,Project,40,100
Charlie,Final,48,100
Diana,Homework 1,48,50
Diana,Homework 2,50,50
Diana,Midterm,95,100
Diana,Project,98,100
Diana,Final,97,100
Ethan,Homework 1,40,50
Ethan,Homework 2,35,50
Ethan,Midterm,78,100
Ethan,Project,72,100
Ethan,Final,81,100
```

### Processing:

1. Read the CSV file into a structured data format
2. Calculate each student's **total percentage** (total earned points / total possible points × 100)
3. Assign letter grades using this scale:
   - **A**: 90–100%
   - **B**: 80–89%
   - **C**: 70–79%
   - **D**: 60–69%
   - **F**: Below 60%
4. Calculate class statistics: average, highest, lowest, standard deviation, grade distribution

### Output: Formatted report

```
╔══════════════════════════════════════════════════════════════╗
║              STUDENT GRADE REPORT                           ║
║              Generated: 2026-02-27                          ║
╚══════════════════════════════════════════════════════════════╝

Students: 5 | Assignments: 5 per student

── Individual Reports ──────────────────────────────────────────

Diana
  Homework 1:    48/50   (96.0%)
  Homework 2:    50/50  (100.0%)
  Midterm:       95/100  (95.0%)
  Project:       98/100  (98.0%)
  Final:         97/100  (97.0%)
  ───────────────────────────────
  Total:        388/400  (97.0%)  ██████████████████░░ A

Alice
  Homework 1:    45/50   (90.0%)
  Homework 2:    38/50   (76.0%)
  Midterm:       82/100  (82.0%)
  Project:       90/100  (90.0%)
  Final:         88/100  (88.0%)
  ───────────────────────────────
  Total:        343/400  (85.8%)  █████████████████░░░ B

Ethan
  Homework 1:    40/50   (80.0%)
  Homework 2:    35/50   (70.0%)
  Midterm:       78/100  (78.0%)
  Project:       72/100  (72.0%)
  Final:         81/100  (81.0%)
  ───────────────────────────────
  Total:        306/400  (76.5%)  ███████████████░░░░░ C

Bob
  Homework 1:    50/50  (100.0%)
  Homework 2:    42/50   (84.0%)
  Midterm:       71/100  (71.0%)
  Project:       65/100  (65.0%)
  Final:         73/100  (73.0%)
  ───────────────────────────────
  Total:        301/400  (75.3%)  ███████████████░░░░░ C

Charlie
  Homework 1:    30/50   (60.0%)
  Homework 2:    28/50   (56.0%)
  Midterm:       55/100  (55.0%)
  Project:       40/100  (40.0%)
  Final:         48/100  (48.0%)
  ───────────────────────────────
  Total:        201/400  (50.3%)  ██████████░░░░░░░░░░ F

── Class Summary ───────────────────────────────────────────────

Class average:    76.9%
Highest:          97.0% (Diana)
Lowest:           50.3% (Charlie)
Std deviation:    16.3%

Grade distribution:
  A: █████████████████████████ 1 student  (20%)
  B: █████████████████████████ 1 student  (20%)
  C: ██████████████████████████████████████████████████ 2 students (40%)
  D:                          0 students ( 0%)
  F: █████████████████████████ 1 student  (20%)

── Sorted Rankings ─────────────────────────────────────────────

┌──────┬──────────────┬───────────┬───────┐
│ Rank │ Student      │ Score     │ Grade │
├──────┼──────────────┼───────────┼───────┤
│  1   │ Diana        │  97.0%    │  A    │
│  2   │ Alice        │  85.8%    │  B    │
│  3   │ Ethan        │  76.5%    │  C    │
│  4   │ Bob          │  75.3%    │  C    │
│  5   │ Charlie      │  50.3%    │  F    │
└──────┴──────────────┴───────────┴───────┘

Report saved to grade_report.txt
```

---

## STOP — Plan Before You Code

Spend **20–30 minutes** planning. This is a larger project — solid planning is the difference between finishing in 2 hours and struggling for 4.

### Planning Questions

1. **Data model — how will you represent the data in memory?**
   - After reading the CSV, what structure holds all the data?
   - Option A: List of dictionaries → `[{"name": "Alice", "assignment": "HW1", "score": 45, "max": 50}, ...]`
   - Option B: Dictionary of students → `{"Alice": [{"assignment": "HW1", "score": 45, "max": 50}, ...], ...}`
   - Option C: Something else?
   - **Which is best for THIS project? Consider:** what operations do you need? (per-student totals → you need to group by student. Option B is pre-grouped. Option A needs grouping.)
   - **Write down your choice and WHY.** This is the most important planning decision.

2. **Processing pipeline — what steps happen to the data and in what order?**
   - Step 1: Read CSV → raw rows
   - Step 2: Group by student (if Option A) or structure into your model
   - Step 3: Calculate per-student totals and percentages
   - Step 4: Assign letter grades
   - Step 5: Calculate class statistics
   - Step 6: Sort students (by what? percentage? alphabetical? plan this!)
   - Step 7: Generate formatted report
   - **Draw this pipeline as comments in your file**

3. **Function inventory — list EVERY function you'll need:**
   - Data: `load_grades(filepath)` → your data model
   - Calculations: `calculate_percentage(earned, possible)`, `assign_letter_grade(percentage)`, `calculate_class_stats(student_results)`
   - Standard deviation: will you use `statistics.stdev()`? Or implement manually? (Hint: use the library — comment WHY you chose the library over manual.)
   - Report: `format_student_report(student_data)`, `format_class_summary(stats)`, `format_rankings_table(students_sorted)`, `generate_full_report(all_data)`
   - Utility: `format_bar(percentage, width=20)`, `save_report(text, filepath)`
   - Main: `main()`
   - **That's 10+ functions.** List them all with one-line descriptions before writing any code.

4. **Error handling — what can go wrong?**
   - CSV file doesn't exist → show a helpful error message
   - CSV has wrong columns → detect and report
   - Score is greater than max_score → is this invalid or extra credit?
   - No students in the file → handle the empty case
   - **Write down each error case and how you'll handle it**

5. **Output formatting plan:**
   - How will you align the columns in the individual reports? (hint: f-string alignment like `f"{name:<15}"`)
   - How will you draw the table borders? (use box-drawing characters: `┌ ─ ┬ ┐ │ ├ ┼ ┤ └ ┴ ┘`)
   - How does the bar chart scale? (same approach as the Expense Tracker — widest bar = full width, others proportional)

---

## Step-by-Step Instructions

### Step 1: Create the files and write your plan (20–30 minutes)

Create two files:
- `grades.csv` — copy the sample data from above
- `grade_report.py` — your Python program

In `grade_report.py`, start with:
1. The module-level docstring (see example above)
2. Your planning block (40+ lines) covering all 5 planning questions
3. Section separators for the architecture
4. Function stubs with complete docstrings (no bodies yet — just `pass`)

**At this point, you should have 80+ lines of comments and docstrings and zero working code. That's correct. That IS the plan.**

### Step 2: Read the CSV data (10 minutes)

```python
import csv

def load_grades(filepath):
    """
    Read student grade data from a CSV file.

    Parameters:
        filepath (str): Path to the CSV file.

    Returns:
        dict[str, list[dict]]: A dictionary mapping student names to their
        list of assignments. Each assignment is a dict with keys:
            - "assignment" (str): Name of the assignment
            - "score" (int): Points earned
            - "max_score" (int): Points possible

    Raises:
        FileNotFoundError: If the CSV file doesn't exist.
        ValueError: If the CSV is missing required columns.

    Design decision: Returns a dict keyed by student name rather than
    a flat list of rows because every downstream operation (calculating
    totals, generating reports) needs data grouped by student. Grouping
    during loading means we do it once, not repeatedly.
    """
    # TODO: implement
    pass
```

**Comment requirements:**
- Explain WHY you chose `csv.DictReader` over `csv.reader` (named columns vs. index-based access)
- Comment on how you validate the data

**Test immediately:** Load the CSV, print the dictionary, verify it looks right.

### Step 3: Calculate per-student results (10 minutes)

```python
def calculate_student_results(student_assignments):
    """
    Calculate total score, percentage, and letter grade for one student.

    Parameters:
        student_assignments (list[dict]): List of assignment records
            for a single student.

    Returns:
        dict: Summary with keys:
            - "assignments" (list[dict]): Original assignment list
            - "total_earned" (int): Sum of all scores
            - "total_possible" (int): Sum of all max_scores
            - "percentage" (float): Overall percentage, rounded to 1 decimal
            - "letter_grade" (str): Letter grade (A/B/C/D/F)

    Why percentage is total_earned/total_possible, NOT averaging per-assignment:
        If a student scores 50/50 on homework and 50/100 on the final,
        averaging percentages gives (100% + 50%) / 2 = 75%.
        But total-based gives 100/150 = 66.7%.
        The second method weights harder assignments more, which is
        standard in education. We use total-based here deliberately.
    """
    # TODO: implement
    pass


def assign_letter_grade(percentage):
    """
    Convert a percentage to a letter grade.

    Parameters:
        percentage (float): Score as a percentage (0-100+).

    Returns:
        str: One of "A", "B", "C", "D", "F".

    Implementation note: Using a series of if/elif rather than a dictionary
    lookup because the grade boundaries are ranges, not exact values.
    A dictionary approach would work with something like:
        grades = {9: "A", 8: "B", 7: "C", 6: "D"}
        return grades.get(int(percentage) // 10, "F")
    But that breaks for 100% (10 // 10 = 10, not in dict) and for edge
    cases like 89.5%. The if/elif approach is clearer and handles all cases.
    """
    # TODO: implement
    pass
```

**Test:** Calculate results for Alice manually (343/400 = 85.75% → B). Verify your function matches.

### Step 4: Calculate class-wide statistics (10 minutes)

```python
import statistics

def calculate_class_stats(all_results):
    """
    Calculate class-wide statistics from all student results.

    Parameters:
        all_results (dict[str, dict]): Mapping of student name → result dict
            (as returned by calculate_student_results).

    Returns:
        dict with keys:
            - "average" (float): Mean percentage across all students
            - "highest" (tuple): (percentage, student_name) of top student
            - "lowest" (tuple): (percentage, student_name) of bottom student
            - "std_dev" (float): Standard deviation of percentages
            - "grade_distribution" (dict): {"A": count, "B": count, ...}

    Why we use statistics.stdev() instead of implementing manually:
        Standard library functions are tested, optimized, and immediately
        recognizable. Rolling our own would need comments explaining
        the formula, add potential for bugs, and make reviewers wonder
        why we didn't use the library. In interviews, mentioning that
        you'd use the standard library shows practical engineering sense.
    """
    # TODO: implement
    pass
```

**Test:** Manually calculate: average of (97.0, 85.8, 76.5, 75.3, 50.3) = 76.98. Verify your function.

### Step 5: Format the individual student reports (15 minutes)

Build the individual report section. This is where your f-string alignment skills matter.

```python
def format_bar(percentage, width=20):
    """
    Create a text-based progress bar.

    Parameters:
        percentage (float): Value between 0 and 100.
        width (int): Total width of the bar in characters.

    Returns:
        str: A string like "██████████████░░░░░░" (width characters total).

    How the scaling works:
        filled = round(percentage / 100 * width)
        This maps 0% → 0 blocks, 50% → 10 blocks, 100% → 20 blocks.
        round() is used instead of int() to avoid systematic undercount —
        int(99.5 / 100 * 20) = 19, but round(99.5 / 100 * 20) = 20.
    """
    # TODO: implement
    pass
```

**Comment requirement:** Every column alignment choice must have a comment. For example:
```python
# Right-align score in a 3-character field so single and double digit
# scores line up: " 45/50" and " 8/10" both look clean in the report.
line = f"  {assignment:<15} {score:>3}/{max_score:<3}  ({percentage:>5.1f}%)"
```

### Step 6: Format the class summary and rankings table (15 minutes)

Build the summary section with the grade distribution bar chart and the rankings table.

```python
def format_rankings_table(sorted_students):
    """
    Create a bordered table showing student rankings.

    Parameters:
        sorted_students (list[tuple]): List of (name, percentage, grade)
            tuples, sorted by percentage descending.

    Returns:
        str: A complete formatted table as a multi-line string.

    Implementation approach: Build the table as a list of strings, then
    join with newlines. This is cleaner than printing each row because:
    1. The caller decides when/where to output (screen, file, or both)
    2. Easier to test — compare strings instead of capturing stdout
    3. The function is pure (no side effects), which is a best practice
    """
    # TODO: implement
    pass
```

### Step 7: Generate the full report and save (10 minutes)

```python
def generate_report(filepath="grades.csv"):
    """
    Orchestrate the full processing pipeline and produce the report.

    This is the top-level function that connects all the pieces:
        CSV file → load → calculate → format → display + save

    Parameters:
        filepath (str): Path to the input CSV file.

    Returns:
        str: The complete formatted report text.

    Architecture note: This function acts as a "controller" — it calls
    other functions in sequence but contains minimal logic itself. Each
    step is delegated to a specialized function. This separation means
    you can test formatting independently from calculations, and swap
    the CSV source for a database later without changing the report logic.
    """
    # TODO: implement
    pass
```

Save the report to both the console and a `.txt` file.

### Step 8: Test thoroughly (10 minutes)

- Run with the sample CSV → verify output matches the example above
- Check the math manually for at least 2 students
- Try a CSV with only 1 student → does it handle "1 student" (not "1 students")?
- Try a missing CSV → does it show a helpful error?
- Check that `grade_report.txt` is written correctly
- **Count your comments:** aim for a comment-to-code ratio of at least 1:2 (one comment line for every two code lines)

---

## Comment Checklist

- [ ] Module-level docstring with usage instructions (10+ lines)
- [ ] Planning block with all 5 planning decisions explained (40+ lines)
- [ ] Section separators organizing the code into logical groups
- [ ] Every function has a complete docstring with Parameters, Returns, and at least one design note
- [ ] Data model choice is documented with alternatives considered
- [ ] The grading approach (total-based vs. average-based) is explained
- [ ] Library usage (`csv`, `statistics`) is justified
- [ ] At least 3 functions document an alternative approach and why it was rejected
- [ ] All f-string formatting alignment choices are commented
- [ ] The bar chart scaling math is explained step by step
- [ ] Error handling has comments explaining what could go wrong
- [ ] `if __name__ == "__main__"` guard present with comment

---

## Stretch Goals

1. Accept a command-line argument for the CSV path using `sys.argv` (comment: why `sys.argv` vs. `argparse` for a simple case?)
2. Add weighted categories — homework counts 20%, midterm 30%, final 50% (comment: how does this change your calculation approach?)
3. Generate an HTML version of the report with CSS styling (comment: when would a team choose HTML over plain text output?)
4. Add a "student at risk" flag for anyone below 65% (comment: where in the pipeline should this check happen and why?)
5. Read multiple CSV files and combine them (comment: what happens when student names overlap across files?)
