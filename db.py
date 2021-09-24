import sqlite3

conn = sqlite3.connect("books.sqlite")

cursor = conn.cursor()
sql_query = """ CREATE TABLE book (
    id integer PRIMARY KEY,
    author text NOT NULL,
    title text NOT NULL,
    page_number text NOT NULL
)"""
cursor.execute(sql_query)
