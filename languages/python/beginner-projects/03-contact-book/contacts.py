"""
Contact Book — Starter Code
=============================

YOUR TASK: Fill in every function marked with TODO.
Read the README.md in this folder FIRST for the full instructions.

TIME ESTIMATE: 1–1.5 hours

IMPORTANT — If You Get Stuck:
    1. Re-read the README section for the step you're on.
    2. Write out what you want in plain English BEFORE writing Python.
    3. Build and test ONE function at a time. Don't write everything then debug.
    4. Use an AI assistant (like Copilot Chat) to ASK QUESTIONS about
       concepts you don't understand — for example:
         "How do I read and write JSON files in Python?"
         "How do I search for a substring inside a string?"
         "What does json.dump vs json.dumps do?"
       DO NOT ask AI to write the solution for you. The learning happens
       when YOUR brain figures out how to connect the pieces. AI is a
       tutor, not a shortcut. If AI writes your code, you skip the
       struggle that actually builds understanding.
    5. Check the Python docs: https://docs.python.org/3/library/json.html

PLANNING — Answer these BEFORE writing any code (fill in below):

    Data structure for a single contact:
        - A dictionary with keys: "name", "phone", "email"
        - Why dict? Named access (contact["name"]) is clearer than index-based
        - Alternative: named tuple — rejected because we need to modify contacts
          for updates, and tuples are immutable

    Data structure for the collection:
        - A list of dictionaries
        - I'll identify contacts by their position in the list (index)
        - Trade-off: lookup is O(n) not O(1), but for a personal contact
          book with < 100 entries, this is fine

    Persistence:
        - JSON file (contacts.json) — human-readable, Python has built-in support
        - If file doesn't exist: start with an empty list (first run)
        - If file is corrupted: warn the user, start with an empty list

    Function inventory:
        1. load_contacts(filepath) — read contacts from JSON file
        2. save_contacts(contacts, filepath) — write contacts to JSON file
        3. add_contact(contacts) — prompt user, create dict, append to list
        4. list_contacts(contacts) — display all contacts in a table
        5. search_contacts(contacts, query) — find by name (partial match)
        6. update_contact(contacts) — modify an existing contact's fields
        7. delete_contact(contacts) — remove a contact after confirmation
        8. main() — menu loop tying everything together

    Build order:
        1. load_contacts + save_contacts (test with hardcoded data)
        2. add_contact + list_contacts (now I can add and see results)
        3. search_contacts (read capability)
        4. update_contact + delete_contact (complete CRUD)
        5. main menu loop (ties it all together)
"""

import json
import os

# ============================================================
# DATA LAYER
# ============================================================
# All functions below handle reading/writing the contacts.json file.
# The rest of the app should NEVER open the file directly — it
# always goes through these functions. This separation means if
# we later switch from JSON to a database, we only change here.
# ============================================================

CONTACTS_FILE = "contacts.json"


def load_contacts(filepath=CONTACTS_FILE):
    """
    Load contacts from a JSON file.

    Parameters:
        filepath (str): Path to the JSON file. Defaults to "contacts.json".

    Returns:
        list[dict]: A list of contact dictionaries.
                    Returns an empty list if the file doesn't exist (first run)
                    or if the JSON is invalid (corrupted file).

    Error handling:
        - FileNotFoundError: normal on first run — return empty list
        - json.JSONDecodeError: file is corrupted — warn user, return empty list
        We NEVER crash on load — the user can always start fresh.
    """
    # TODO: Implement this function
    # Hints:
    #   - Use a try/except block to handle missing and corrupted files
    #   - Open the file with open(filepath, "r") and use json.load() to parse
    #   - Catch FileNotFoundError — return []
    #   - Catch json.JSONDecodeError — print a warning, return []
    pass


def save_contacts(contacts, filepath=CONTACTS_FILE):
    """
    Save the full contact list to a JSON file.

    Parameters:
        contacts (list[dict]): The complete list of contact dictionaries.
        filepath (str): Path to the JSON file.

    Returns:
        None

    Design choice: We save the ENTIRE list every time, not just the
    changed contact. This is simpler and totally fine for a small dataset.
    For thousands of records, you'd want a database with individual updates.
    """
    # TODO: Implement this function
    # Hints:
    #   - Open the file with open(filepath, "w") and use json.dump()
    #   - Use indent=2 to make the JSON file human-readable
    #   - The "w" mode overwrites the entire file — that's what we want
    pass


# ============================================================
# CONTACT OPERATIONS (CRUD)
# ============================================================
# Create, Read, Update, Delete — the four fundamental operations
# behind almost every application.
# ============================================================


def add_contact(contacts):
    """
    Prompt the user for contact details and add a new contact.

    Parameters:
        contacts (list[dict]): The current contact list (modified in place).

    Returns:
        None

    Why modify in place instead of returning a new list:
        For a simple app, modifying the existing list is straightforward.
        In larger applications, returning a new list (immutability) is
        safer because it avoids unexpected side effects. For this project,
        in-place modification keeps the code simpler.
    """
    # TODO: Implement this function
    # Hints:
    #   - Use input() to ask for name, phone, and email
    #   - Strip whitespace from inputs with .strip()
    #   - Require name (don't allow blank). Phone and email can be optional.
    #   - Create a dictionary: {"name": name, "phone": phone, "email": email}
    #   - Append it to the contacts list
    #   - Call save_contacts() immediately (save after every change!)
    #   - Print a confirmation message
    pass


def list_contacts(contacts):
    """
    Display all contacts in a formatted table.

    Parameters:
        contacts (list[dict]): All contacts.

    Returns:
        None — prints to console.

    If there are no contacts, print a helpful message instead of
    an empty table — the user needs to know what to do next.
    """
    # TODO: Implement this function
    # Hints:
    #   - If len(contacts) == 0, print "No contacts yet. Use 'Add' to create one!"
    #   - Otherwise, print a header row and then each contact
    #   - Use f-strings with width specifiers for aligned columns:
    #     f"{'Name':<20}" left-aligns "Name" in a 20-character-wide field
    #   - Number each contact (starting from 1) so user can reference them
    #     for update/delete
    pass


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
    # TODO: Implement this function
    # Hints:
    #   - Convert query to lowercase with query.lower()
    #   - Loop through contacts and check if query.lower() is in contact["name"].lower()
    #   - Collect matching contacts in a results list and return it
    #   - You could also use a list comprehension:
    #     [c for c in contacts if query.lower() in c["name"].lower()]
    pass


def update_contact(contacts):
    """
    Update an existing contact's fields.

    Shows current values and lets the user press Enter to keep them.
    This is a common UX pattern — faster for the user when they only
    need to change one field.

    Parameters:
        contacts (list[dict]): All contacts (modified in place).

    Returns:
        None
    """
    # TODO: Implement this function
    # Hints:
    #   - First, call list_contacts() so the user can see the numbers
    #   - Ask which contact number to update
    #   - Convert to an index (number - 1, since we display 1-based)
    #   - For each field (name, phone, email):
    #     - Show the current value: f"Name [{contact['name']}]: "
    #     - If the user types something new, use it
    #     - If the user presses Enter (empty string), keep the old value
    #   - Save after updating
    pass


def delete_contact(contacts):
    """
    Delete a contact after confirmation.

    Parameters:
        contacts (list[dict]): All contacts (modified in place).

    Returns:
        None

    Safety: Always ask "Are you sure?" before a destructive operation.
    In production, you'd use "soft delete" (mark as deleted but keep data).
    For this project, real deletion is fine.
    """
    # TODO: Implement this function
    # Hints:
    #   - Show the list so the user can pick a number
    #   - Ask for the contact number to delete
    #   - Show the contact details and ask "Are you sure? (yes/no)"
    #   - Only delete if the user confirms with "yes"
    #   - Use contacts.pop(index) to remove by index
    #   - Save after deleting
    pass


# ============================================================
# MAIN MENU LOOP
# ============================================================
# This is the entry point — a while loop showing options and
# routing to the right function based on user choice.
# ============================================================


def main():
    """
    Run the contact book application.

    Architecture:
        1. Load contacts from file (or start empty on first run)
        2. Show menu in a loop
        3. Call the appropriate function based on user choice
        4. Save after every modification (add, update, delete)
        5. Exit cleanly when user chooses Quit

    Why save after every change (not just on quit):
        If the program crashes or the user force-closes the terminal,
        changes since the last save would be lost. Saving after each
        modification prevents data loss. The performance cost of writing
        a small JSON file is negligible.
    """
    # Load existing contacts (empty list on first run)
    contacts = load_contacts()

    # TODO: Implement the menu loop
    # Hints:
    #   - Print how many contacts were loaded
    #   - Use a while True loop
    #   - Show the menu:
    #       1) Add a contact
    #       2) List all contacts
    #       3) Search contacts
    #       4) Update a contact
    #       5) Delete a contact
    #       6) Quit
    #   - Get the user's choice with input()
    #   - Use if/elif to call the right function
    #   - For "Quit" — print a goodbye message and break
    #   - For search — ask for the search query, call search_contacts,
    #     then display the results
    pass


# Main guard — only starts the app when run directly
if __name__ == "__main__":
    main()


# ============================================================
# WHAT I LEARNED (fill this in AFTER you finish)
# ============================================================
# Friend:    ...
# Employer:  ...
# Professor: ...
# ============================================================
