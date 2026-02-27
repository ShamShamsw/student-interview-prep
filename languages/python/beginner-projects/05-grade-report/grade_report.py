"""
Student Grade Report — Starter Code
======================================

Reads student grade data from a CSV file, computes individual and class-wide
statistics, assigns letter grades, and produces a formatted report.

Usage:
    python grade_report.py                  # uses default grades.csv
    python grade_report.py my_grades.csv    # uses a custom file

YOUR TASK: Fill in every function marked with TODO.
Read the README.md in this folder FIRST for the full instructions.

TIME ESTIMATE: 1.5–2 hours

IMPORTANT — If You Get Stuck:
    1. Re-read the README section for the step you're on.
    2. Work through the math on paper first — pick one student, calculate
       their percentage by hand, then verify your code matches.
    3. Test functions individually before connecting them.
    4. Use an AI assistant (like Copilot Chat) to ASK QUESTIONS about
       concepts you don't understand — for example:
         "How do I use csv.DictReader in Python?"
         "How does statistics.stdev work?"
         "How do I right-align a number in an f-string?"
       DO NOT ask AI to write the solution for you. The learning happens
       when YOUR brain connects the pieces. AI is a tutor, not a
       shortcut — if AI writes your code, you skip the struggle that
       builds real understanding.
    5. Python docs: https://docs.python.org/3/library/csv.html
                    https://docs.python.org/3/library/statistics.html

PLANNING — Answer these BEFORE writing any code (fill in below):

    Data model (after reading the CSV):
        - A dictionary keyed by student name, where each value is a list
          of assignment dictionaries:
          {"Alice": [{"assignment": "HW1", "score": 45, "max_score": 50}, ...]}
        - Why keyed by student? Because every operation (total, grade, report)
          is per-student. Pre-grouping avoids repeated filtering.

    Processing pipeline:
        1. Read CSV → raw rows
        2. Group rows by student name → dict of lists
        3. For each student: sum scores, sum max_scores, calculate percentage
        4. Assign letter grade based on percentage
        5. Calculate class stats: average, highest, lowest, std dev, distribution
        6. Sort students by percentage (descending) for rankings
        7. Format and print the report + save to file

    Grade scale:
        A: 90–100%   B: 80–89%   C: 70–79%   D: 60–69%   F: below 60%

    Functions:
        - load_grades(filepath) → dict of student assignments
        - calculate_student_results(assignments) → summary dict
        - assign_letter_grade(percentage) → "A"/"B"/"C"/"D"/"F"
        - calculate_class_stats(all_results) → stats dict
        - format_bar(percentage, width) → "██████░░░░"
        - format_student_report(name, results) → formatted string
        - format_class_summary(stats) → formatted string
        - format_rankings_table(sorted_students) → formatted string
        - generate_report(filepath) → full report string
        - main() → orchestrate everything
"""

import csv
import statistics
import sys
from datetime import date


# ============================================================
# DATA LOADING
# ============================================================

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
    a flat list of rows because every downstream operation needs data
    grouped by student. Grouping during loading means we do it once.

    Why csv.DictReader instead of csv.reader:
        DictReader gives us named columns (row["student_name"])
        instead of index-based access (row[0]). More readable and
        less error-prone if column order changes.
    """
    # TODO: Implement this function
    # Hints:
    #   - Open the file and create a csv.DictReader
    #   - The CSV columns are: student_name, assignment_name, score, max_score
    #   - Loop through rows, grouping by student_name into a dict
    #   - Convert score and max_score to int (they come in as strings from CSV)
    #   - Example structure of the result:
    #     {
    #       "Alice": [
    #         {"assignment": "Homework 1", "score": 45, "max_score": 50},
    #         {"assignment": "Midterm", "score": 82, "max_score": 100},
    #       ],
    #       "Bob": [...]
    #     }
    pass


# ============================================================
# CALCULATIONS
# ============================================================

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
        standard in education.
    """
    # TODO: Implement this function
    # Hints:
    #   - total_earned = sum(a["score"] for a in student_assignments)
    #   - total_possible = sum(a["max_score"] for a in student_assignments)
    #   - percentage = round(total_earned / total_possible * 100, 1)
    #   - letter_grade = assign_letter_grade(percentage)
    #   - Return a dict with all the above plus the original assignments
    pass


def assign_letter_grade(percentage):
    """
    Convert a percentage to a letter grade.

    Parameters:
        percentage (float): Score as a percentage (0–100+).

    Returns:
        str: One of "A", "B", "C", "D", "F".

    Using if/elif because boundaries are ranges, not exact matches.
    """
    # TODO: Implement this function
    # Grade scale: A >= 90, B >= 80, C >= 70, D >= 60, F < 60
    pass


def calculate_class_stats(all_results):
    """
    Calculate class-wide statistics from all student results.

    Parameters:
        all_results (dict[str, dict]): Mapping of student name → result dict
            (as returned by calculate_student_results).

    Returns:
        dict with keys:
            - "average" (float): Mean percentage across all students
            - "highest" (tuple): (percentage, student_name)
            - "lowest" (tuple): (percentage, student_name)
            - "std_dev" (float): Standard deviation of percentages
            - "grade_distribution" (dict): {"A": count, "B": count, ...}

    Why statistics.stdev() instead of manual implementation:
        Standard library functions are tested and optimized.
        Rolling our own adds bug risk for no benefit. In interviews,
        mentioning you'd use the standard library shows practical sense.
    """
    # TODO: Implement this function
    # Hints:
    #   - Extract all percentages: [r["percentage"] for r in all_results.values()]
    #   - Use statistics.mean() for average
    #   - Use max/min with a key function for highest/lowest
    #   - Use statistics.stdev() for standard deviation (needs >= 2 students)
    #   - Count grades with a loop or Counter from collections
    pass


# ============================================================
# REPORT FORMATTING
# ============================================================

def format_bar(percentage, width=20):
    """
    Create a text-based progress bar.

    Parameters:
        percentage (float): Value between 0 and 100.
        width (int): Total width of the bar in characters.

    Returns:
        str: A string like "██████████████░░░░░░"

    How the scaling works:
        filled = round(percentage / 100 * width)
        This maps 0% → 0 blocks, 50% → half, 100% → full.
        round() avoids systematic undercount vs int().
    """
    # TODO: Implement this — about 3 lines
    # Hint:
    #   filled = round(percentage / 100 * width)
    #   return "█" * filled + "░" * (width - filled)
    pass


def format_student_report(name, results):
    """
    Format a single student's detailed grade report.

    Parameters:
        name (str): Student name.
        results (dict): Student results from calculate_student_results.

    Returns:
        str: Formatted multi-line report string for this student.

    Shows each assignment with score and percentage, plus the total
    with a progress bar and letter grade.
    """
    # TODO: Implement this function
    # Hints:
    #   - Build a list of lines, join with "\\n" at the end
    #   - For each assignment: f"  {name:<15} {score:>3}/{max:>3}  ({pct:>5.1f}%)"
    #   - Add a separator line, then the total with bar and grade
    #   - Use format_bar() for the visual bar
    pass


def format_class_summary(stats, all_results):
    """
    Format the class-wide summary section.

    Parameters:
        stats (dict): Class statistics from calculate_class_stats.
        all_results (dict): All student results (for count).

    Returns:
        str: Formatted class summary string.

    Includes: average, highest, lowest, std dev, and grade distribution bar chart.
    """
    # TODO: Implement this function
    # Hints:
    #   - Print each stat on its own line
    #   - For grade distribution, show a bar chart similar to the expense tracker
    #   - Handle singular vs plural: "1 student" vs "2 students"
    pass


def format_rankings_table(sorted_students):
    """
    Create a bordered table showing student rankings.

    Parameters:
        sorted_students (list[tuple]): List of (name, percentage, grade)
            tuples, sorted by percentage descending.

    Returns:
        str: A formatted table string.

    Build the table as a list of strings, then join with newlines.
    This is cleaner than printing each row because:
        1. The caller decides when/where to output
        2. Easier to test — compare strings instead of capturing stdout
        3. The function is pure (no side effects)
    """
    # TODO: Implement this function
    # Hints:
    #   - Use box-drawing characters: ┌ ─ ┬ ┐ │ ├ ┼ ┤ └ ┴ ┘
    #   - Or use simpler +---+ style borders if box-drawing is confusing
    #   - Columns: Rank, Student, Score, Grade
    pass


# ============================================================
# MAIN PIPELINE
# ============================================================

def generate_report(filepath="grades.csv"):
    """
    Orchestrate the full pipeline: load → calculate → format → display + save.

    Parameters:
        filepath (str): Path to the input CSV file.

    Returns:
        str: The complete formatted report text.

    Architecture note: This function acts as a "controller" — it calls
    other functions in sequence but contains minimal logic itself.
    Each step is delegated to a specialized function.
    """
    # TODO: Implement this function
    # Steps:
    #   1. Load grades with load_grades(filepath)
    #   2. Calculate results for each student
    #   3. Calculate class stats
    #   4. Sort students by percentage (descending)
    #   5. Build the report by calling the format functions
    #   6. Print the report to the console
    #   7. Save the report to "grade_report.txt"
    #   8. Return the report string
    pass


def main():
    """
    Entry point — determine the CSV file to use and generate the report.
    """
    # Allow custom file path from command line, default to grades.csv
    filepath = sys.argv[1] if len(sys.argv) > 1 else "grades.csv"

    # TODO: Call generate_report(filepath) and handle FileNotFoundError
    # Hint:
    #   try:
    #       generate_report(filepath)
    #   except FileNotFoundError:
    #       print(f"Error: File '{filepath}' not found.")
    #       print("Make sure grades.csv exists in the same directory.")
    pass


if __name__ == "__main__":
    main()


# ============================================================
# WHAT I LEARNED (fill this in AFTER you finish)
# ============================================================
# Friend:    ...
# Employer:  ...
# Professor: ...
# ============================================================
