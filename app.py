import os

from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
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

    #creo 1° tabella con portfolio
    portfolio = db.execute("SELECT item, quantity FROM portfolio WHERE username = ? and quantity !=0", session["username"])
    asset=0
    for row in portfolio:
        info=lookup(row["item"])
        if info:
            row["price"]=info["price"]
            row["tot_item_value"]=row["price"]*row["quantity"]
            asset += row["tot_item_value"]

    #creo 2° tabella con recap cash
    result = db.execute("SELECT cash FROM users WHERE username = ?", session["username"])
    cash = result[0]["cash"]

    #mando html a schermo
    return render_template("index.html", portfolio=portfolio, username=session["username"], cash=cash, asset=asset)

@app.route("/todo", methods=["GET", "POST"])
@login_required
def todo():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol=request.form.get("symbol")
        quantity=request.form.get("shares")

        # reject empty input
        if not symbol or not quantity:
            return apology("Please fill both checkbox.")

        # reject quantity<=0
        try:
            quantity = int(quantity)
            if quantity <= 0:
                return apology("Please insert a number bigger than 0 :)")
        except ValueError:
            return apology("Please insert a valid integer")

        # check if symbol exìsts
        if not lookup(symbol):
            return apology("Please enter a valid symbol.")

        # Recupero i valori per le operazioni
        price=lookup(symbol)["price"]
        user_cash = db.execute("SELECT cash from users where username = ?", session["username"])[0]['cash']
        transaction_amount = quantity * price

        # check if I have enough money?
        if user_cash < transaction_amount:
            return apology("Sorry, it seems you do not have enough money for this transaction.")

        # update users table reflecting expense
        db.execute("UPDATE users SET cash = cash - ? WHERE username = ?", transaction_amount, session["username"])

        # update history table inserting transaction
        db.execute("INSERT INTO history (username, transaction_type, item, price, quantity) VALUES (?,?,?,?,?)",session["username"], "buy", symbol, price, quantity)

        #user already had this item in portfolio table? to understand if create from zero or increase
        item_count = db.execute("SELECT COUNT(*) FROM portfolio WHERE username = ? AND item = ?", session["username"], symbol)[0]['COUNT(*)']
        # update portfolio table reflecting +item/quantity
        if item_count > 0:
            db.execute("UPDATE portfolio SET quantity = (quantity + ?) WHERE username = ? and item = ?", quantity, session["username"], symbol) #increase
        else:
            db.execute("INSERT INTO portfolio (username, item, quantity) VALUES (?,?,?)",session["username"], symbol, quantity) #create from zero

        return redirect("/")

    if request.method == "GET":
        return render_template("todo.html")


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
def quote():

    if request.method == "POST":
        symbol = request.form.get("symbol") #registro il search input
        #se campo vuoto rimando errore
        if not symbol:
            return apology("Please enter a valid symbol.")
        else:
            search=lookup(symbol) #fz lookup restituisce dict 2 key: user_id e username
            #se non esiste questo simbolo rimando errore
            if not search:
                return apology("Please enter a valid symbol.")
            # inserisco ricerca in tabella sql 'history', la aggiorno, e rimando template html con risposta
            else:
                db.execute("INSERT INTO history (username, transaction_type, item, price) VALUES (?,?,?,?)",session["username"], "search", symbol, search["price"])
                search_history = db.execute("SELECT item, price FROM history WHERE transaction_type = ? AND username = ? LIMIT 10", "search", session["username"])
                return render_template("wordz.html", search_history=search_history, search=search)

    else: #if GET mando html
        search_history = db.execute("SELECT item, price FROM history WHERE transaction_type = ? AND username = ? LIMIT 10", "search", session["username"])
        return render_template("wordz.html", search_history=search_history)

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
    if request.method == "POST":
        selected_month = request.form.get('month')
    else:
        # Default to the current month if no form is submitted
        selected_month = datetime.now().strftime('%B')  # Get the full month name

    selected_month_expenses, expenses_data = get_expenses_and_totals(session["username"], selected_month)
    return render_template("numberz.html", selected_month=selected_month, selected_month_expenses=selected_month_expenses, expenses_data=expenses_data)
