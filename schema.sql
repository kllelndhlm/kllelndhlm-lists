CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);
CREATE TABLE list (
    id SERIAL PRIMARY KEY,
    username TEXT,
    list_name TEXT,
    artist TEXT,
    song TEXT,
    genre TEXT,
    year TEXT,
    visible INT
);
CREATE TABLE message (
    id SERIAL PRIMARY KEY,
    username TEXT,
    list_name TEXT,
    content TEXT,
    visible INT,
    sent_at TIMESTAMP
);
