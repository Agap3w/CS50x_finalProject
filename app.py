import os

from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, get_expenses_and_totals, last_expenses
# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///fp.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    #mando html a schermo
    return render_template("index.html", username = session["username"])

@app.route("/todo", methods=["GET", "POST"])
@login_required
def todo():
    #when users submit, save the 2 variables
    if request.method == "POST":
        todo=request.form.get("todo")
        prio=request.form.get("prio")

        # reject empty input
        if not todo or not prio:
            flash("Missing information. Try Again")
            return redirect("/todo")
        
        # reject duplicates
        if db.execute("SELECT * FROM todos WHERE username = ? AND item = ?", session["username"], todo):
            flash("This todo already exists. Try Again")
            return redirect("/todo")


        # update todos table inserting new item
        db.execute("INSERT INTO todos (username, category, item, status) VALUES (?,?,?,?)",session["username"], prio, todo, "open")

        return redirect("/todo")
    
    else: #if GET mando html
        todo_history = db.execute("SELECT item, category FROM todos WHERE username = ? ORDER BY timedate DESC LIMIT 5", session["username"])
        return render_template("todo.html", todo_history=todo_history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password")

        # Remember which user has logged in (storing id and username)
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/wordz", methods=["GET", "POST"])
@login_required
def wordz():
    # POST(=tasto remove) rimuove la riga dalla table todos e aggiorna pagina
    if request.method == "POST":
        item_remove = request.form.get("remove")
        if item_remove:
            db.execute("DELETE FROM todos WHERE item = ?", item_remove)
            return redirect(url_for("wordz"))

    #GET, calcolo tabelle urgent e backlog e mando html a schermo
    else:
        user_todo_urgent = db.execute("SELECT item, timedate FROM todos WHERE username = ? AND category = ? AND status = ?", session["username"], "urgent", "open")
        for row in user_todo_urgent:
            row['timedate'] = datetime.strptime(row['timedate'], '%Y-%m-%d %H:%M:%S')  # Adjust format as needed
            row['delay'] = (datetime.now() - row['timedate']).days
        user_todo_backlog = db.execute("SELECT item, timedate FROM todos WHERE username = ? AND category = ? AND status = ?", session["username"], "backlog", "open")
        for row in user_todo_backlog:
            row['timedate'] = datetime.strptime(row['timedate'], '%Y-%m-%d %H:%M:%S')  # Adjust format as needed
            row['delay'] = (datetime.now() - row['timedate']).days

        return render_template("wordz.html", user_todo_urgent=user_todo_urgent, user_todo_backlog=user_todo_backlog)



@app.route("/register", methods=["GET", "POST"])
def register():

    # Forget any user_id
    session.clear()

    if request.method == "POST":

        # Add the user's entry into the database
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username")

        # Ensure password was submitted
        elif not password or not confirmation:
            return apology("must provide password two times")

        # If psw not corrispondent
        elif password!=confirmation:
            return apology("the 2 passwords provided are different")

        #insert row into db
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?,?)", username, generate_password_hash(password))
            return redirect("/")
        # sarebbe meglio mettere errore specifico (UNIQUE constraint failed: users.username) ma non trovo sintassi con lib sQL
        except:
            return apology("username already exists")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/expense", methods=["GET", "POST"])
@login_required
def expense():

    if request.method == "POST":
        category=request.form.get("category")
        description=request.form.get("description")
        amount=request.form.get("amount")

        # reject empty input
        if not category or not amount or not description:
            return apology("Please fill all the checkbox.")

        # reject amount<=0
        amount=int(amount)
        if amount<=0:
            return apology("Please insert a number bigger than 0 :)")

        # update expense table inserting expsense
        db.execute("INSERT INTO expenses (username, category, description, amount) VALUES (?,?,?,?)", session["username"], category, description, amount)

        return redirect("/expense")

    else:
        user_last_expenses=last_expenses(session["username"])
        return render_template("expense.html", user_last_expenses=user_last_expenses)

@app.route("/numberz", methods=["GET", "POST"])
@login_required
def numberz():
    selected_month = None
    if request.method == "POST":
        selected_month = request.form.get('month')
    #else:
        # Default to the current month if no form is submitted
        #selected_month = datetime.now().strftime('%B')  # Get the full month name

    selected_month_expenses, expenses_data = get_expenses_and_totals(session["username"], selected_month)
    return render_template("numberz.html", selected_month=selected_month, selected_month_expenses=selected_month_expenses, expenses_data=expenses_data)