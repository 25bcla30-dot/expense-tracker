from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("expenses.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def home():
    conn = get_db()
    if request.method == "POST":
        title = request.form["title"]
        amount = request.form["amount"]
        category = request.form["category"]
        conn.execute(
            "INSERT INTO expenses (title, amount, category) VALUES (?, ?, ?)",
            (title, amount, category),
        )
        conn.commit()
        conn.close()
        return redirect("/")

    expenses = conn.execute("SELECT * FROM expenses ORDER BY id DESC").fetchall()
    total = sum(e["amount"] for e in expenses)
    conn.close()
    return render_template("index.html", expenses=expenses, total=total)
@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete(expense_id):
    conn = get_db()
    conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    return redirect("/")

init_db()

if __name__ == "__main__":
    app.run(debug=True)