import sqlite3

connect = sqlite3.connect("db.sqlite")

cursor = connect.cursor()
sql_query = """ create table products(
    id integer primary key,
    name text,
    price integer,
    amount integer
)"""
cursor.execute(sql_query)
