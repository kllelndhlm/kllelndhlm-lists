from flask import session, render_template, redirect
from db import db
from werkzeug.security import check_password_hash, generate_password_hash

def new_list(session_list_name):
    sql = "SELECT COUNT(*) FROM list WHERE list_name=:session_list_name"
    result = db.session.execute(sql, {"session_list_name":session_list_name})
    count = result.fetchone()[0]
    sql = "SELECT username, list_name, artist, song, genre, year FROM list WHERE list_name=:session_list_name"
    result = db.session.execute(sql, {"session_list_name":session_list_name})
    list = result.fetchall()
    return render_template("new_list.html", count=count, list=list)

def insert_list_row(username, list_name, artist, song, genre, year):
    sql = "INSERT INTO list (username, list_name, artist, song, genre, year) VALUES (:username, :list_name, :artist, :song, :genre, :year)"
    db.session.execute(sql, {"username":username, "list_name":list_name, "artist":artist, "song":song, "genre":genre, "year":year})
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
    sql = "SELECT COUNT(DISTINCT list_name) FROM list"
    result = db.session.execute(sql)
    count = result.fetchone()[0]
    sql = "SELECT artist, COUNT(artist) AS artist_occurence FROM list GROUP BY artist ORDER BY artist_occurence DESC"
    result = db.session.execute(sql)
    most_frequent_artist = result.fetchall()
    sql = "SELECT artist, song, COUNT(song) AS song_occurence FROM list GROUP BY artist, song ORDER BY song_occurence DESC"
    result = db.session.execute(sql)
    most_frequent_song = result.fetchall()
    sql = "SELECT genre, COUNT(genre) AS genre_occurence FROM list GROUP BY genre ORDER BY genre_occurence DESC"
    result = db.session.execute(sql)
    most_frequent_genre = result.fetchall()
    sql = "SELECT year, COUNT(year) AS year_occurence FROM list GROUP BY year ORDER BY year_occurence DESC"
    result = db.session.execute(sql)
    most_frequent_year = result.fetchall()
    return render_template("statistics.html", count=count, most_frequent_artist = most_frequent_artist, most_frequent_song = most_frequent_song,  most_frequent_genre =  most_frequent_genre, most_frequent_year = most_frequent_year)
