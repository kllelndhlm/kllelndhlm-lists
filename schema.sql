CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);
CREATE TABLE entries (
    id SERIAL PRIMARY KEY,
    username TEXT,
    list_name TEXT UNIQUE,
    artist TEXT,
    song TEXT,
    genre TEXT,
    year TEXT
);
