import sqlite3
from datetime import datetime
from functools import wraps

from flask import redirect, session


def login_required(f):
    """
    Login Required Decorator
    https://flask.palletsprojects.com/en/2.2.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def connect_db(db="dvdkuranglaku.db"):
    con = sqlite3.connect(db)
    cur = con.cursor()
    return con, cur


def username_validation(username):
    if not username.isascii():
        return 1
    specialchars = "`~!@#$%^&*()-=+}{[\|];:,.<>/?' " + '"'
    for i in range(len(username)):
        if username[i] in specialchars:
            return 2
    return 0


def get_today_date():
    return datetime.today().strftime('%Y-%m-%d')
