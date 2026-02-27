"""
Expense Tracker — Starter Code
================================

YOUR TASK: Fill in every function marked with TODO.
Read the README.md in this folder FIRST for the full instructions.

TIME ESTIMATE: 1–2 hours

IMPORTANT — If You Get Stuck:
    1. Re-read the README section for the step you're on.
    2. Write pseudocode (plain English steps) before real code.
    3. Build and test ONE function at a time — don't write everything at once.
    4. Use an AI assistant (like Copilot Chat) to ASK QUESTIONS about
       concepts you don't understand — for example:
         "How do I use .get() on a dictionary in Python?"
         "How do I format a float as currency ($24.50)?"
         "What does a generator expression do in sum()?"
       DO NOT ask AI to write the solution for you. The learning happens
       when YOUR brain figures out how to connect the pieces. AI is a
       tutor, not a shortcut. If AI writes your code, you learned nothing.
    5. Python docs for date handling: https://docs.python.org/3/library/datetime.html

PLANNING — Answer these BEFORE writing any code (fill in below):

    Data model for a single expense:
        - id (int): Unique identifier — generated as max existing ID + 1
        - amount (float): Dollar amount — float is fine for this project
          (acknowledging that 0.1 + 0.2 != 0.3 in floating point, but
          for a personal tracker this precision is acceptable)
        - category (str): One of the predefined categories
        - description (str): What the expense was for
        - date (str): "YYYY-MM-DD" format string

    Data model for the collection:
        - A list of dictionaries
        - Each expense has a unique 'id' so we can tell apart two
          expenses with the same amount and category

    Summary algorithms (plan BEFORE coding):
        - Total: sum() with a generator expression — O(n) single pass
        - By category: dictionary accumulation with .get() — O(n) single pass
        - Biggest: max() with key=lambda — O(n) single pass

    Function inventory:
        - load_expenses / save_expenses — data persistence layer
        - add_expense — prompt user, create record, save
        - list_expenses — display table, optional category filter
        - get_total — sum all amounts
        - get_by_category — group and sum by category
        - get_biggest — find the largest expense
        - show_summary — call the above three and format output with bar chart
        - delete_expense — remove by number after confirmation
        - format_currency — helper to display "$24.50" consistently
        - main — menu loop
"""

import json
import os
from datetime import date


# ============================================================
# CONSTANTS
# ============================================================
# Keeping valid categories in a tuple (not a list) because:
#   1. They shouldn't be modified at runtime — tuple signals immutability
#   2. Easy to validate user input: if category in CATEGORIES
#   3. Single source of truth — add a category by changing one line
# ============================================================

CATEGORIES = ("food", "transport", "entertainment", "shopping", "bills", "health", "other")
DATA_FILE = "expenses.json"


# ============================================================
# DATA LAYER
# ============================================================
# Same pattern as the Contact Book — these are the ONLY functions
# that touch the file. Everything else works with in-memory data.
# ============================================================

def load_expenses(filepath=DATA_FILE):
    """
    Load expenses from a JSON file.

    Parameters:
        filepath (str): Path to the JSON file.

    Returns:
        list[dict]: All expense records. Empty list if file doesn't exist.
    """
    # TODO: Implement this (same pattern as Contact Book — try/except for
    # FileNotFoundError and json.JSONDecodeError)
    pass


def save_expenses(expenses, filepath=DATA_FILE):
    """
    Save all expenses to a JSON file.

    Parameters:
        expenses (list[dict]): The complete expense list.
        filepath (str): Path to the JSON file.

    Returns:
        None
    """
    # TODO: Implement this (json.dump with indent=2)
    pass


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def format_currency(amount):
    """
    Format a number as a dollar amount string.

    Parameters:
        amount (float): The amount to format.

    Returns:
        str: Formatted like "$24.50" (always 2 decimal places).

    Why a helper function for this:
        Without this, you'd write f"${amount:.2f}" in 10 different places.
        If you later need to change the format (e.g., add thousands separators),
        you change it in ONE place.
    """
    # TODO: Implement this — it's one line!
    # Hint: return f"${amount:.2f}"
    pass


def generate_id(expenses):
    """
    Generate a unique ID for a new expense.

    Parameters:
        expenses (list[dict]): All current expenses.

    Returns:
        int: A unique ID (max existing ID + 1, or 1 if list is empty).

    Why not just use len(expenses) + 1:
        If you delete expense #3 from a list of 5, len becomes 4.
        The next add would get ID 5, which already exists!
        Using max ID + 1 avoids collisions even after deletions.
    """
    # TODO: Implement this
    # Hint: if not expenses: return 1
    #       else: return max(e["id"] for e in expenses) + 1
    pass


# ============================================================
# EXPENSE OPERATIONS
# ============================================================

def add_expense(expenses):
    """
    Prompt the user for expense details and add it to the list.

    Parameters:
        expenses (list[dict]): Current expenses (modified in place).

    Returns:
        dict: The newly created expense record.

    Steps:
        1. Ask for amount (validate it's a positive number)
        2. Ask for category (validate it's in CATEGORIES)
        3. Ask for description (any text)
        4. Ask for date (default to today if user presses Enter)
        5. Generate a unique ID
        6. Create the expense dict, append, and save
    """
    # TODO: Implement this function
    # Hints:
    #   - For amount: use a while loop, try float(input()), catch ValueError
    #   - For category: show the options, validate with `if cat in CATEGORIES`
    #   - For date: use date.today().isoformat() as the default
    #     input(f"Date (YYYY-MM-DD, Enter for today): ") or date.today().isoformat()
    pass


def list_expenses(expenses, category_filter=None):
    """
    Display expenses in a formatted table, optionally filtered by category.

    Parameters:
        expenses (list[dict]): All expenses.
        category_filter (str or None): If provided, only show this category.

    Returns:
        None — prints to console.

    Why the filter is a parameter and not a separate function:
        Filtering and displaying are tightly related. One function with
        an optional parameter is simpler than two functions with
        duplicated display logic. DRY principle.
    """
    # TODO: Implement this function
    # Hints:
    #   - If category_filter is set, filter the list first:
    #     filtered = [e for e in expenses if e["category"] == category_filter]
    #   - Print a header row with columns: #, Date, Category, Amount, Description
    #   - Use f-string alignment for clean columns
    #   - Show a total at the bottom
    pass


def delete_expense(expenses):
    """
    Delete an expense by number after confirmation.

    Parameters:
        expenses (list[dict]): All expenses (modified in place).

    Returns:
        None
    """
    # TODO: Implement this function
    # Hints: same pattern as Contact Book — list, pick a number, confirm, pop, save
    pass


# ============================================================
# SUMMARY / ANALYSIS FUNCTIONS
# ============================================================
# These functions compute aggregate statistics from the raw data.
# Each one has an algorithm comment explaining the approach.
# ============================================================

def get_total(expenses):
    """
    Calculate the total of all expense amounts.

    Parameters:
        expenses (list[dict]): All expenses.

    Returns:
        float: Total of all amounts.
    """
    # TODO: Implement this
    # Hint: use sum() with a generator expression
    # sum(e["amount"] for e in expenses) — this is O(n), single pass
    pass


def get_by_category(expenses):
    """
    Calculate total spending grouped by category.

    Parameters:
        expenses (list[dict]): All expenses.

    Returns:
        dict: {category_name: total_amount} for each category with spending.

    Algorithm: Single pass through the expenses list, accumulating
    totals in a dictionary keyed by category name.

    Alternative considered: Sort by category first, then group —
    rejected because it's O(n log n) when we only need O(n).
    The dictionary approach uses O(k) extra space where k = number
    of unique categories, which is typically small (< 10).
    """
    # TODO: Implement this function
    # Hints:
    #   - Create an empty dict: totals = {}
    #   - Loop through expenses
    #   - For each: totals[category] = totals.get(category, 0) + amount
    #     (.get() returns 0 if the key doesn't exist yet, avoiding KeyError)
    #   - Return the totals dict
    pass


def get_biggest(expenses):
    """
    Find the single largest expense.

    Parameters:
        expenses (list[dict]): All expenses.

    Returns:
        dict or None: The expense with the largest amount,
                      or None if the list is empty.

    Edge case: if expenses is empty, max() raises ValueError.
    We handle this by checking first and returning None.
    """
    # TODO: Implement this function
    # Hint: if not expenses: return None
    #       return max(expenses, key=lambda e: e["amount"])
    pass


def show_summary(expenses):
    """
    Display a complete spending summary with a bar chart.

    Includes:
        - Total spending and transaction count
        - Average expense amount
        - Category breakdown with proportional bar chart
        - Largest single expense

    Bar chart algorithm:
        1. Find the category with the largest total (gets the full bar, e.g., 20 chars)
        2. Scale all other categories proportionally:
           bar_length = int(category_total / max_total * bar_width)
        3. Use "█" (full block) for filled portion
        4. Use "░" (light shade) for empty portion
    """
    # TODO: Implement this function
    # Hints:
    #   - Call get_total(), get_by_category(), get_biggest()
    #   - For the bar chart, the widest bar should be ~20 characters
    #   - Sort categories by total (descending) for a nice display:
    #     sorted(totals.items(), key=lambda x: x[1], reverse=True)
    #   - Calculate percentage: category_total / grand_total * 100
    #   - Build bars: "█" * filled + "░" * (bar_width - filled)
    pass


# ============================================================
# MAIN MENU
# ============================================================

def main():
    """
    Run the expense tracker application.

    Flow:
        1. Load expenses from file
        2. Show menu in a loop
        3. Route to the appropriate function
        4. Save after modifications
        5. Quit when user chooses
    """
    expenses = load_expenses()

    # TODO: Implement the menu loop
    # Menu options:
    #   1) Add expense
    #   2) List expenses
    #   3) View summary
    #   4) Delete expense
    #   5) Quit
    #
    # For "List expenses" — ask if they want to filter by category
    # For "Quit" — print total and goodbye
    pass


# Main guard
if __name__ == "__main__":
    main()


# ============================================================
# WHAT I LEARNED (fill this in AFTER you finish)
# ============================================================
# Friend:    ...
# Employer:  ...
# Professor: ...
# ============================================================
