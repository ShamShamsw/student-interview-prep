# Beginner Project 03: Contact Book

**Time:** 1–1.5 hours  
**Difficulty:** Beginner  
**Focus:** Planning data persistence, CRUD operations, file I/O with JSON, writing comments that explain design trade-offs

---

## Why This Project?

Almost every application in the real world does four things: **Create, Read, Update, Delete** (CRUD). A contact book is the simplest possible CRUD app. If you can build this, you understand the pattern behind every database-backed application — the same pattern interviewers ask about in backend questions.

This project also introduces **data persistence** — your program saves data to a file so information isn't lost when the program closes. This is a fundamental concept that many beginners miss.

---

## The Importance of Comments

In this project, focus on **architecture comments** — comments that explain how pieces fit together, not just what one line does.

### Architecture comments explain the big picture:
```python
# === DATA LAYER ===
# All functions below handle reading and writing the contacts.json file.
# The rest of the app should NEVER open the file directly — it should
# always go through these functions. This separation means if we later
# switch from JSON to a database, we only change these functions.

def load_contacts(filepath="contacts.json"):
    ...

def save_contacts(contacts, filepath="contacts.json"):
    ...
```

### Decision comments explain trade-offs:
```python
# I'm storing contacts as a list of dictionaries instead of a dictionary
# keyed by name because:
# 1. Two people can have the same name (list allows duplicates)
# 2. We might want to sort by different fields later
# 3. It maps directly to JSON arrays, making persistence simple
#
# Trade-off: looking up a specific contact is O(n) instead of O(1).
# For a small personal contact book, this is fine. If we had thousands
# of contacts, we'd want a dictionary keyed by a unique ID.
```

This is exactly the kind of reasoning interviewers love to hear.

---

## Requirements

Build a command-line contact book that supports:

1. **Add** a new contact (name, phone, email)
2. **List** all contacts in a clean formatted table
3. **Search** contacts by name (partial match)
4. **Update** an existing contact's phone or email
5. **Delete** a contact
6. **Save** contacts to a JSON file automatically
7. **Load** contacts from the JSON file on startup

### Example session:

```
=== Contact Book ===
Loaded 3 contacts from contacts.json

What would you like to do?
  1) Add a contact
  2) List all contacts
  3) Search contacts
  4) Update a contact
  5) Delete a contact
  6) Quit

Choice: 2

┌────┬──────────────┬──────────────┬─────────────────────┐
│ #  │ Name         │ Phone        │ Email               │
├────┼──────────────┼──────────────┼─────────────────────┤
│  1 │ Alice Smith  │ 555-0101     │ alice@example.com   │
│  2 │ Bob Jones    │ 555-0102     │ bob@example.com     │
│  3 │ Charlie Lee  │ 555-0103     │ charlie@example.com │
└────┴──────────────┴──────────────┴─────────────────────┘

Choice: 3
Search for: ali

Found 1 result(s):
  1. Alice Smith — 555-0101 — alice@example.com

Choice: 4
Enter the number of the contact to update: 1
Updating Alice Smith. Press Enter to keep the current value.
  Name [Alice Smith]: 
  Phone [555-0101]: 555-9999
  Email [alice@example.com]: 
Updated! Alice Smith's phone changed to 555-9999.

Choice: 6
Saved 3 contacts. Goodbye!
```

---

## STOP — Plan Before You Code

Spend **15 minutes** planning. Write your answers as a comment block at the top of your file.

### Planning Questions

1. **Data structure for a single contact:**
   - What fields does each contact need?
   - What type is each field? (all strings? some optional?)
   - Will you use a dictionary, a named tuple, or a dataclass?
   - **Write your choice and explain WHY** (at least 3 lines of reasoning)

2. **Data structure for the collection of contacts:**
   - List of contacts? Dictionary keyed by what?
   - How will you identify a specific contact for update/delete? (by index? by name? by unique ID?)
   - **Write your choice and the trade-offs** you considered

3. **File format for persistence:**
   - Why JSON? What alternatives exist? (CSV, plain text, pickle, SQLite)
   - What happens if the file doesn't exist yet? (first run)
   - What happens if the file is corrupted? (malformed JSON)

4. **Function inventory:**
   List every function you'll need. For each, write:
   - Name
   - Parameters
   - Return value
   - One sentence describing what it does
   
   Aim for 7–10 functions. If you have fewer than 6, your functions are probably doing too much.

5. **Build order:**
   Which functions will you build and test first? What can you demo before the whole program works?

   Suggested order:
   1. `load_contacts` + `save_contacts` (test with a hardcoded list)
   2. `add_contact` + `list_contacts` (now you can add and see results)
   3. `search_contacts` (adds read capability)
   4. `update_contact` + `delete_contact` (complete CRUD)
   5. Main menu loop (ties it all together)

---

## Step-by-Step Instructions

### Step 1: Plan and write the comment block (15 minutes)

Create `contacts.py`. Write your complete planning block. **This should be 25–30+ lines.** Include:
- Data structure decisions with reasoning
- Complete function inventory
- Build order
- Known edge cases

### Step 2: Write the data layer — `load_contacts` and `save_contacts` (10 minutes)

These two functions are the foundation. Nothing else works without them.

```python
# === DATA LAYER ===
# These functions are the ONLY part of the program that touches the file.
# Every other function works with in-memory data (a list of dicts).
# This separation is called the "repository pattern" — it isolates
# how data is stored from how data is used.

import json
import os

def load_contacts(filepath="contacts.json"):
    """
    Load contacts from a JSON file.

    Parameters:
        filepath (str): Path to the JSON file. Defaults to "contacts.json".

    Returns:
        list[dict]: A list of contact dictionaries. Returns an empty list
        if the file doesn't exist (first run) or if the JSON is invalid.

    Error handling:
        - FileNotFoundError: normal on first run, return empty list
        - json.JSONDecodeError: file is corrupted, warn user, return empty list
        We NEVER crash on load — the user can always start fresh.
    """
    # TODO: implement this
    pass

def save_contacts(contacts, filepath="contacts.json"):
    """
    Save the full contact list to a JSON file.

    Parameters:
        contacts (list[dict]): The complete list of contact dictionaries.
        filepath (str): Path to the JSON file.

    Returns:
        None

    Design choice: we save the ENTIRE list every time, not just the
    changed contact. This is simpler and fine for a small dataset.
    For thousands of records, you'd want a database with individual updates.
    """
    # TODO: implement this
    pass
```

**Test this immediately:** Create a small test list, save it, then load it back and print it. Confirm the round trip works before moving on.

### Step 3: Write `add_contact` (5 minutes)

Prompts for name, phone, and email, creates a dictionary, adds it to the list.

Add comments for:
- Why you strip whitespace from inputs
- How you handle empty/blank inputs (require name, but phone and email are optional?)
- Why the function modifies the list in place vs. returning a new list

### Step 4: Write `list_contacts` (5 minutes)

Displays all contacts in a formatted table. If there are no contacts, print a helpful message instead of an empty table.

```python
# Formatting tip: use f-strings with width specifiers for aligned columns.
# f"{'Name':<20}" left-aligns "Name" in a 20-character-wide field.
# The < means left-align, the number is the width.
```

Add a comment explaining why you chose the column widths you did.

### Step 5: Write `search_contacts` (5 minutes)

Takes a search string and returns all contacts whose name contains that string (case-insensitive).

```python
def search_contacts(contacts, query):
    """
    Search contacts by name (case-insensitive partial match).

    Parameters:
        contacts (list[dict]): All contacts.
        query (str): The search string.

    Returns:
        list[dict]: Contacts whose name contains the query string.

    Why partial match instead of exact match:
        Users rarely remember full names exactly. Typing "ali" should
        find "Alice Smith". This is the same behavior as Ctrl+F in a
        browser — users expect it to work this way.
    """
    # TODO: implement
    pass
```

### Step 6: Write `update_contact` and `delete_contact` (10 minutes)

For update: show the current values and let the user press Enter to keep them unchanged. This is a common UX pattern — add a comment explaining why it's user-friendly.

For delete: always confirm before deleting. Add a comment about why confirmation matters.

```python
# Safety: always ask "Are you sure?" before a destructive operation.
# In production code, you'd implement "soft delete" (mark as deleted
# but keep the data) instead of actual deletion. For this project,
# real deletion is fine since we have the JSON file as a backup.
```

### Step 7: Write the main menu loop (10 minutes)

Use a `while True` loop with the menu options. Map user input to function calls.

```python
def main():
    """
    Run the contact book application.

    Architecture:
        1. Load contacts from file (or start empty)
        2. Show menu in a loop
        3. Dispatch to the appropriate function based on user choice
        4. Save after every modification (add, update, delete)
        5. Exit cleanly when user chooses Quit

    Why save after every change (not just on quit):
        If the program crashes or the user force-closes the terminal,
        changes since the last save would be lost. Saving after each
        modification prevents data loss. The performance cost of writing
        a small JSON file is negligible.
    """
    # TODO: implement
    pass
```

### Step 8: Test the complete flow (10 minutes)

Test these scenarios:
- Start fresh (no JSON file) → add 3 contacts → quit → restart → contacts are still there
- Search with different casing ("ALICE", "alice", "Alice") → all should match
- Update only the phone (leave name and email unchanged)
- Delete a contact → confirm it's gone from the list
- Open `contacts.json` in a text editor → it should be readable, nicely formatted JSON

---

## Comment Checklist

- [ ] Planning block at the top (25+ lines) with data structure reasoning and trade-offs
- [ ] `load_contacts` and `save_contacts` have architecture comments explaining the repository pattern
- [ ] Every function has a complete docstring
- [ ] At least 3 "design choice" or "why" comments throughout the code
- [ ] Error handling code has comments explaining what each case means
- [ ] The save-after-every-modification decision is commented and justified
- [ ] The main loop structure has a comment explaining its flow
- [ ] `if __name__ == "__main__"` guard is present with a comment

---

## Stretch Goals

1. Add a "favorite" flag and a command to list favorites only (comment on why booleans in your data model)
2. Sort contacts by name alphabetically in the list view (comment on Python's sort vs. sorted)
3. Export contacts to a CSV file (comment on when CSV is better than JSON and vice versa)
4. Add the ability to undo the last action (hint: save a copy of the list before each change)
