import sqlite3
from datetime import date
from pathlib import Path
from fastmcp import FastMCP

mcp = FastMCP(name="ExpenseTracker")
CATEGORY_PATH =  Path(__file__).resolve().parent / "categories.json"
# Store the database in the same folder as this Python file
DB_PATH = Path(__file__).resolve().parent / "expenses.db"


def db_init():
    """Create the expenses table if it does not already exist."""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            date_of_add TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@mcp.tool
def add_expense(name: str, category: str, price: float):
    """Add a new expense to the expenses database."""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses (name, category, date_of_add, price)
        VALUES (?, ?, ?, ?)
    """, (name, category, date.today().isoformat(), price))

    conn.commit()
    conn.close()


@mcp.tool
def get_expenses_by_category(category: str):
    """Return all expenses belonging to the specified category."""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, category, date_of_add, price
        FROM expenses
        WHERE category = ?
    """, (category,))

    expenses = cursor.fetchall()

    conn.close()

    return expenses


@mcp.tool
def delete_expense(expense_id: int):
    """Delete an expense from the database using its ID."""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM expenses
        WHERE id = ?
    """, (expense_id,))

    conn.commit()
    conn.close()


@mcp.tool
def get_expenses_by_date(expense_date: str):
    """Return all expenses added on the specified date."""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, category, date_of_add, price
        FROM expenses
        WHERE date_of_add = ?
    """, (expense_date,))

    expenses = cursor.fetchall()

    conn.close()

    return expenses
#MIME type tells the client what kind of data your resource returns
#scheme://resource-name
 # │          │
#  │          └── name/identifier of resource
#  └───────────── type/category of resource
   
@mcp.resource("expense://categories" , mime_type="application/json")
def categories():
    with open(CATEGORY_PATH , "r") as file:
        return file.read()


if __name__ == "__main__":
    db_init()
    mcp.run()