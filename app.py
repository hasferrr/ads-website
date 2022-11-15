from flask import Flask, render_template, request, redirect, session
from flask_session import Session

from account import account_page
from helpers import login_required, connect_db, get_today_date


# Configure app
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Blueprints
app.register_blueprint(account_page)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["GET", "POST"])
def index():

    # If user has NOT been logged in
    if session.get("user_id") is None:
        return render_template("index.html")


    # If user LOGGED IN
    # Connect to database
    con, cur = connect_db()
    users_pelanggan = cur.execute("SELECT * FROM users JOIN pelanggan WHERE users.id = pelanggan.user_id AND users.id = ?",
                                    (session["user_id"],))
    users_pelanggan = users_pelanggan.fetchall()[0]

    username = users_pelanggan[1]
    nama = users_pelanggan[5]

    if request.method == "POST":

        judul = request.form.get("judul")
        kuantitas = request.form.get("kuantitas")
        tanggal_pengembalian = request.form.get("tanggal_pengembalian")
        tanggal_sewa = get_today_date()
        metode_pembayaran = request.form.get("pilih_metode_pembayaran")

        if not judul:
            return render_template("error.html", error="must provide data")
        if not kuantitas:
            return render_template("error.html", error="must provide data")
        if not tanggal_pengembalian:
            return render_template("error.html", error="must provide data")
        if not metode_pembayaran:
            return render_template("error.html", error="must provide data")

        cur.execute("INSERT INTO sewa (user_id, judul, kuantitas, tanggal_pengembalian, tanggal_sewa) VALUES (?, ?, ?, ?, ?)",
            (session["user_id"], judul, kuantitas, tanggal_pengembalian, tanggal_sewa))
        con.commit()

        sewa_id = cur.execute("SELECT sewa_id FROM sewa WHERE user_id = ? ORDER BY sewa_id DESC LIMIT 1;",
                                (session["user_id"],)).fetchall()[0][0]
        cur.execute("INSERT INTO pembayaran (sewa_id, metode_pembayaran) VALUES (?, ?)",
            (sewa_id, metode_pembayaran))
        con.commit()


        return render_template("home.html", username=username, nama=nama)

    else:
        return render_template("home.html", username=username, nama=nama)




@app.route("/sewa", methods=["GET"])
@login_required
def sewa():
    return redirect("/")



@app.route("/data", methods=["GET"])
@login_required
def data():

    con, cur = connect_db()
    users = cur.execute("SELECT * FROM users").fetchall()
    pelanggan = cur.execute("SELECT * FROM pelanggan").fetchall()
    sewa = cur.execute("SELECT * FROM sewa").fetchall()
    genre = cur.execute("SELECT * FROM genre").fetchall()

    return render_template("data.html", users=users, pelanggan=pelanggan, sewa=sewa, genre=genre)




@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="404 Page not found"), 404
