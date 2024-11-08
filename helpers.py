import csv
import datetime
import pytz
import requests
import urllib
import uuid

from flask import redirect, render_template, request, session
from functools import wraps
from cs50 import SQL

db = SQL("sqlite:///fp.db")

def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def get_month_number(month_name):
    month_map = {
        "January": "01", "February": "02", "March": "03",
        "April": "04", "May": "05", "June": "06",
        "July": "07", "August": "08", "September": "09",
        "October": "10", "November": "11", "December": "12"
    }
    return month_map.get(month_name)

def get_expenses_and_totals(username, month_name):
    month_number = get_month_number(month_name)
    expenses = db.execute("""
        SELECT category, description, amount, strftime('%d', timedate) || '-' ||
        CASE strftime('%m', timedate)
            WHEN '01' THEN 'Gen' WHEN '02' THEN 'Feb'
            WHEN '03' THEN 'Mar' WHEN '04' THEN 'Apr'
            WHEN '05' THEN 'Mag' WHEN '06' THEN 'Giu'
            WHEN '07' THEN 'Lug' WHEN '08' THEN 'Ago'
            WHEN '09' THEN 'Set' WHEN '10' THEN 'Ott'
            WHEN '11' THEN 'Nov' WHEN '12' THEN 'Dic'
        END AS formatted_date
        FROM expenses WHERE username = ? AND
        strftime('%m', timedate) = ?""", username, month_number)

    category_totals = {}
    for row in expenses:
        category = row['category']
        amount = row['amount']
        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount
    expenses_data = {
        "labels": list(category_totals.keys()),
        "amounts": list(category_totals.values())
    }
    return expenses, expenses_data

def last_expenses(username):
    return db.execute("""
        SELECT category, description, amount,
        strftime('%d', timedate) || '-' ||
        CASE strftime('%m', timedate)
            WHEN '01' THEN 'Gen' WHEN '02' THEN 'Feb'
            WHEN '03' THEN 'Mar' WHEN '04' THEN 'Apr'
            WHEN '05' THEN 'Mag' WHEN '06' THEN 'Giu'
            WHEN '07' THEN 'Lug' WHEN '08' THEN 'Ago'
            WHEN '09' THEN 'Set' WHEN '10' THEN 'Ott'
            WHEN '11' THEN 'Nov' WHEN '12' THEN 'Dic'
        END AS formatted_date
        FROM expenses
        WHERE username = ?
        ORDER BY timedate DESC
        LIMIT 5""", username)
