CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);
CREATE TABLE entries (
    id SERIAL PRIMARY KEY,
    username TEXT,
    entry_name TEXT,
    artist TEXT,
    song TEXT,
    genre TEXT,
    year TEXT
);
