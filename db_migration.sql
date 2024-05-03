CREATE DATABASE todo_db;
\c todo_db;

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    task TEXT
);
