from app import app
from flask import redirect, render_template, request, session
import register_login, db

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["get","post"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if register_login.login(username,password):
            session["username"] = username
            return redirect("/")
        else:
            return render_template("error_message.html",message="Käyttäjätunnus tai salasana väärin")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if register_login.register(username,password):
            return redirect("/")
        else:
            return render_template("error.html",message="Rekisteröinti ei onnistunut")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/login_new_list_name",methods=["POST"])
def login_new_list_name():
    list_name = request.form["list_name"]
    session["list_name"] = list_name
    return redirect("/new_list")


@app.route("/logout_list_name")
def logout_list_name():
    del session["list_name"]
    return redirect("/new_list_name")

@app.route("/new_list")
def new_list():
    session_list_name = session["list_name"]
    sql = "SELECT COUNT(*) FROM list WHERE list_name=:session_list_name"
    result = db.session.execute(sql, {"session_list_name":session_list_name})
    count = result.fetchone()[0]
    sql = "SELECT username, list_name, artist, song, genre, year FROM list WHERE list_name=:session_list_name"
    result = db.session.execute(sql, {"session_list_name":session_list_name})
    list = result.fetchall()
    return render_template("new_list.html", count=count, list=list)

@app.route("/new_list_name")
def list_name():
    return render_template("new_list_name.html")


@app.route("/send", methods=["POST"])
def send():
    username = session["username"]
    list_name = session["list_name"]
    artist = request.form["artist"]
    song = request.form["song"]
    genre = request.form["genre"]
    year = request.form["year"]
    sql = "INSERT INTO list (username, list_name, artist, song, genre, year) VALUES (:username, :list_name, :artist, :song, :genre, :year)"
    db.session.execute(sql, {"username":username, "list_name":list_name, "artist":artist, "song":song, "genre":genre, "year":year})
    db.session.commit()
    return redirect("/new_list")

@app.route("/statistics")
def statistics():
    sql = "SELECT COUNT(DISTINCT list_name) FROM list"
    result = db.session.execute(sql)
    count = result.fetchone()[0]
    sql = "SELECT artist, COUNT(artist) AS artist_occurence FROM list GROUP BY artist ORDER BY artist_occurence DESC"
    result = db.session.execute(sql)
    most_frequent_artist = result.fetchall()
    sql = "SELECT song, COUNT(song) AS song_occurence FROM list GROUP BY song ORDER BY song_occurence DESC"
    result = db.session.execute(sql)
    most_frequent_song = result.fetchall()
    sql = "SELECT genre, COUNT(genre) AS genre_occurence FROM list GROUP BY genre ORDER BY genre_occurence DESC"
    result = db.session.execute(sql)
    most_frequent_genre = result.fetchall()
    sql = "SELECT year, COUNT(year) AS year_occurence FROM list GROUP BY year ORDER BY year_occurence DESC"
    result = db.session.execute(sql)
    most_frequent_year = result.fetchall()
    return render_template("statistics.html", count=count, most_frequent_artist = most_frequent_artist, most_frequent_song = most_frequent_song,  most_frequent_genre =  most_frequent_genre, most_frequent_year = most_frequent_year)
