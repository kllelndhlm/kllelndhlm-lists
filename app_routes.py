from app import app
from db import db
import db, register_login, app_lists, app_comments
from flask import Flask
from flask import redirect, render_template, request, session, abort
from os import getenv
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text
import secrets

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        session["csrf_token"] = secrets.token_hex(16)
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

@app.route("/register_new_list_name",methods=["GET", "POST"])
def register_new_list_name():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    new_list_name = request.form["list_name"]
    session["list_name"] = new_list_name
    if app_lists.register_new_list_name(new_list_name):
        return redirect("/new_list")
    else:
        return render_template("register_new_list_name_error.html")

@app.route("/new_list", methods=["GET"])
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
    del session["csrf_token"]
    return redirect("/new_list_name")

@app.route("/insert_list_row", methods=["GET","POST"])
def insert_list_row():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    username = session["username"]
    list_name = session["list_name"]
    artist = request.form["artist"]
    song = request.form["song"]
    genre = request.form["genre"]
    year = request.form["year"]
    visible = 1
    app_lists.insert_list_row(username, list_name, artist, song, genre, year, visible)
    return redirect("/new_list")

@app.route("/statistics")
def statistics():
    return app_lists.statistics()

@app.route("/list_page/<string:list_name>", methods=["GET"])
def list_page(list_name):
    return app_lists.list_page(list_name)

@app.route("/send_comment", methods=["GET","POST"])
def send_comment():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    username = session["username"]
    list_name = request.form["list_name"]
    content = request.form["comment"]
    visible = 1
    if app_comments.send_comment(username, list_name, content, visible):
        return list_page(list_name)
    else:
        return render_template("error.html",message="Jotain meni pieleen :|")

@app.route("/hide_comment", methods=["GET","POST"])
def hide_comment():
    comment_id = request.form["comment_id"]
    list_name = request.form["list_name"]
    visible = 0
    if app_comments.hide_comment(comment_id, visible):
        return list_page(list_name)
    else:
        return render_template("error.html",message="Jotain meni pieleen :|")

@app.route("/hide_list", methods=["GET","POST"])
def hide_list():
    list_id = request.form["list_id"]
    list_name = request.form["list_name"]
    visible = 0
    if app_lists.hide_list(list_id, visible):
        return redirect("/statistics")
    else:
        return render_template("error.html",message="Jotain meni pieleen :|")


