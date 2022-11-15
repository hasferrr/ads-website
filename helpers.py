import sqlite3
from datetime import datetime
from functools import wraps

from flask import redirect, session
import matplotlib.pyplot as plt
from numpy import arange as arange


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


def horizontal_bar(height, bars, file_name="foo", bar_color='#69b3a2'):
    """
    Plotting a Horizontal Barplot using Matplotlib
    https://www.python-graph-gallery.com/2-horizontal-barplot
    """

    """
    Matplotlib and :RuntimeError: main thread is not in main loop:
    https://stackoverflow.com/questions/52839758/matplotlib-and-runtimeerror-main-thread-is-not-in-main-loop
    """
    plt.switch_backend('agg')

    # Example
    # height = [30, 120, 5505, 180, 450]  y-axis
    # bars = ('A', 'B', 'C', 'D', 'E')    x-axis
    y_pos = arange(len(bars))

    # Create horizontal bars
    plt.barh(y_pos, height, color=bar_color)

    # Create names on the x-axis
    plt.yticks(y_pos, bars)
    plt.xticks(height, height)

    # Save graphic
    plt.tight_layout()
    plt.savefig("static/img/" + file_name + ".png")

    # Clear plot
    plt.close()
    plt.cla()
    plt.clf()

