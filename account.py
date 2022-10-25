from flask import Blueprint, render_template, request, redirect, session, flash
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, connect_db, username_validation

"""
Modular Applications with Blueprints
https://flask.palletsprojects.com/en/2.2.x/blueprints/
"""
account_page = Blueprint('account_page', __name__, template_folder='templates')







@account_page.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Ensure that user log out first before log in
    if session.get("user_id") is not None:
        return render_template("error.html", error="please log out first")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username and password was submitted
        if not request.form.get("username"):
            return render_template("error.html", error="must provide username")

        if not request.form.get("password"):
            return render_template("error.html", error="must provide password")

        # Query database for username
        con, cur = connect_db()
        rows = cur.execute("SELECT * FROM users WHERE username=:name", {"name": request.form.get("username").lower()})
        rows = list(rows.fetchall())

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            con.close()
            return render_template("error.html", error="invalid username or password")

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Redirect user to home page
        con.close()
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")







@account_page.route("/logout")
@login_required
def logout():
    """Forget user id"""

    # Pop session
    if session.get("user_id") is not None:
        session.pop("user_id")

    return redirect("/")







@account_page.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Ensure that user log out first before register
    if session.get("user_id") is not None:
        return render_template("error.html", error="please log out first")

    # User reached route via POST
    if request.method == "POST":

        ####### ENSURE SECTION #######
        ####### username & password #######

        # Ensure username and password was submitted
        username = request.form.get("username")
        if not username:
            return render_template("error.html", error="must provide username")

        password = request.form.get("password")
        if not password or not request.form.get("confirmation"):
            return render_template("error.html", error="must provide password")

        # Check length
        if len(username) > 26 or len(username) < 3:
            return render_template("error.html", error="too long/short")
        if len(password) < 8:
            return render_template("error.html", error="password at least 8 chars length")

        # Confirmation
        if password != request.form.get("confirmation"):
            return render_template("error.html", error="password doesn't match")

        # Username Validation
        validity = username_validation(username)
        if validity == 1:
            return render_template("error.html", error="invalid char(s)")
        elif validity == 2:
            return render_template("error.html", error="symbols are not allowed (except: _ )")

        del username
        username = request.form.get("username").lower()

        # Query data
        con, cur = connect_db()
        users_database = cur.execute("SELECT username FROM users")

        # Ensure submitted username not already taken
        for user in users_database.fetchall():
            if user[0] == username:
                con.close()
                return render_template("error.html", error="username is already taken")


        ######## ADDING SECTION #######

        # Add them to users table in database
        hash = generate_password_hash(password)
        cur.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash))
        con.commit()

        # Set session
        session["user_id"] = cur.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()[0][0]

        con.close()
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("register.html")
