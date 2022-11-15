from flask import Flask, render_template, request, redirect, session
from flask_session import Session

from account import account_page
from helpers import login_required, connect_db, get_today_date, horizontal_bar


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

    # POST ROUTE
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

        stock_now = cur.execute("SELECT stock FROM produk WHERE judul LIKE ?;",
                                            (judul[:-7],)).fetchall()[0][0]

        stock_now = int(stock_now)

        if stock_now >= int(kuantitas):

            cur.execute("INSERT INTO sewa (user_id, judul, kuantitas, tanggal_pengembalian, tanggal_sewa) VALUES (?, ?, ?, ?, ?)",
                (session["user_id"], judul, kuantitas, tanggal_pengembalian, tanggal_sewa))
            cur.execute("UPDATE produk SET stock = ? WHERE judul LIKE ?",
                (stock_now - int(kuantitas), judul[:-7]))
            con.commit()

            sewa_id = cur.execute("SELECT sewa_id FROM sewa WHERE user_id = ? ORDER BY sewa_id DESC LIMIT 1;",
                                    (session["user_id"],)).fetchall()[0][0]
            cur.execute("INSERT INTO pembayaran (sewa_id, metode_pembayaran) VALUES (?, ?)",
                (sewa_id, metode_pembayaran))
            con.commit()

        else:
            return render_template("error.html", error="sorry, out of stock")

        return render_template("home.html", username=username, nama=nama)

    # GET ROUTE
    else:

        products = cur.execute("SELECT judul, tahun FROM produk ORDER BY judul").fetchall()
        # products = [('The Shawshank Redemption', 1994), ('The Godfather', 1972),..

        list_of_judul = []
        for i in products:
            list_of_judul.append(f"{i[0]} ({i[1]})")

        return render_template("home.html", username=username, nama=nama, list_of_judul=list_of_judul)




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

    # Plotting a Horizontal Barplot

    genres = ["Horror","Fantasy","Drama","Romance","Action","Animation","Documentary"]

    genres_favs_tot = []
    for i in genres:
        temp = cur.execute(f"SELECT SUM({i}) FROM genre").fetchall()[0][0]
        genres_favs_tot.append(temp)

    g_rev = []
    for i in genres:
        g_rev.append(i)
    g_rev.reverse()

    genres_favs_tot_rev = []
    for i in genres_favs_tot:
        genres_favs_tot_rev.append(i)
    genres_favs_tot_rev.reverse()


    img_name = str(session["user_id"]) + "starter_genre"
    horizontal_bar(genres_favs_tot_rev, g_rev, img_name)

    return render_template("data.html", users=users, pelanggan=pelanggan, sewa=sewa, genre=genre, img_name=img_name, genres_favs_tot=genres_favs_tot, genres=genres)




@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="404 Page not found"), 404
