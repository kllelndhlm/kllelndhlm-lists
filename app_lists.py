from flask import session, render_template, redirect, request
from db import db
from werkzeug.security import check_password_hash, generate_password_hash
import secrets

def new_list(session_list_name):
    sql = "SELECT COUNT(*) FROM list WHERE list_name=:session_list_name"
    result = db.session.execute(sql, {"session_list_name":session_list_name})
    count = result.fetchone()[0]
    sql = "SELECT username, list_name, artist, song, genre, year FROM list WHERE list_name=:session_list_name"
    result = db.session.execute(sql, {"session_list_name":session_list_name})
    list = result.fetchall()
    return render_template("new_list.html", count=count, list=list)

def insert_list_row(username, list_name, artist, song, genre, year, visible):
    sql = "INSERT INTO list (username, list_name, artist, song, genre, year, visible) VALUES (:username, :list_name, :artist, :song, :genre, :year, :visible)"
    db.session.execute(sql, {"username":username, "list_name":list_name, "artist":artist, "song":song, "genre":genre, "year":year, "visible":visible})
    db.session.commit()
    return True

def register_new_list_name(new_list_name):
    sql = "SELECT COUNT(*) FROM list WHERE list_name=:new_list_name"
    result = db.session.execute(sql, {"new_list_name":new_list_name})
    count = result.fetchone()[0]
    if count == 0:
        return True
    else:
        return False

def statistics():
    sql = "SELECT DISTINCT list_name, username FROM list WHERE visible=1"
    result = db.session.execute(sql)
    distinct_list = result.fetchall()
    sql = "SELECT COUNT(DISTINCT list_name) FROM list WHERE visible=1"
    result = db.session.execute(sql)
    count = result.fetchone()[0]
    sql = "SELECT * FROM list"
    result = db.session.execute(sql)
    lists = result.fetchall()
    sql = "SELECT artist, COUNT(artist) AS artist_occurence FROM list WHERE visible=1 GROUP BY artist ORDER BY artist_occurence DESC LIMIT 3"
    result = db.session.execute(sql)
    most_frequent_artist = result.fetchall()
    sql = "SELECT artist, song, COUNT(song) AS song_occurence FROM list WHERE visible=1 GROUP BY artist, song ORDER BY song_occurence DESC LIMIT 3"
    result = db.session.execute(sql)
    most_frequent_song = result.fetchall()
    sql = "SELECT genre, COUNT(genre) AS genre_occurence FROM list WHERE visible=1 GROUP BY genre ORDER BY genre_occurence DESC LIMIT 3"
    result = db.session.execute(sql)
    most_frequent_genre = result.fetchall()
    sql = "SELECT year, COUNT(year) AS year_occurence FROM list WHERE visible=1 GROUP BY year ORDER BY year_occurence DESC LIMIT 3"
    result = db.session.execute(sql)
    most_frequent_year = result.fetchall()
    return render_template("statistics.html", distinct_list = distinct_list, count=count, lists=lists, most_frequent_artist = most_frequent_artist, most_frequent_song = most_frequent_song,  most_frequent_genre =  most_frequent_genre, most_frequent_year = most_frequent_year)

def list_page(page_name):
    sql = "SELECT * FROM list WHERE list_name=:page_name AND visible=1"
    result = db.session.execute(sql, {"page_name":page_name})
    list = result.fetchall()
    sql = "SELECT * FROM message WHERE list_name=:page_name AND visible=1"
    result = db.session.execute(sql, {"page_name":page_name})
    comments = result.fetchall()
    page_name = page_name
    return render_template("list_page.html", list = list, comments = comments, page_name = page_name)

def hide_list(list_id, visible):
    sql = "UPDATE list SET visible=0 WHERE list_name=:list_id;"
    db.session.execute(sql, {"list_id":list_id})
    db.session.commit()
    return True
