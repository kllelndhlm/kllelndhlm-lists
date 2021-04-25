from app import app
from db import db
import db, register_login, app_lists
from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text

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
            return render_template("login_error.html")

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
            return render_template("register_error.html")

@app.route("/new_list_name")
def new_list_name():
    return render_template("new_list_name.html")

@app.route("/register_new_list_name",methods=["POST"])
def register_new_list_name():
    new_list_name = request.form["list_name"]
    session["list_name"] = new_list_name
    if app_lists.register_new_list_name(new_list_name):
        return redirect("/new_list")
    else:
        return render_template("register_new_list_name_error.html")

@app.route("/new_list")
def new_list():
    session_list_name = session["list_name"]
    return app_lists.new_list(session_list_name)

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/logout_list_name")
def logout_list_name():
    del session["list_name"]
    return redirect("/new_list_name")

@app.route("/insert_list_row", methods=["POST"])
def insert_list_row():
    username = session["username"]
    list_name = session["list_name"]
    artist = request.form["artist"]
    song = request.form["song"]
    genre = request.form["genre"]
    year = request.form["year"]
    app_lists.insert_list_row(username, list_name, artist, song, genre, year)
    return redirect("/new_list")

@app.route("/statistics")
def statistics():
    return app_lists.statistics()
 
