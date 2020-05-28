import sqlite3

from flask import current_app

from app_files.config import constants
import flask_settings
from cryptography.fernet import Fernet


def add_user(user):
    conn = sqlite3.connect(flask_settings.DB_NAME)
    cur = conn.cursor()
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    encrypted_pw = cipher_suite.encrypt(bytes(user["password"], "utf-8"))

    query = f"""INSERT INTO Users (email, first_name, last_name, password) VALUES ("{user['email']}", "{user['first_name']}", "{user['last_name']}", "{encrypted_pw}");"""
    cur.execute(query)
    conn.commit()
    conn.close()


def get_user(user_email):
    conn = sqlite3.connect(flask_settings.DB_NAME)
    cur = conn.cursor()
    query = f"""SELECT * FROM Users WHERE email="{user_email}" """
    cur.execute(query)
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res


def update_user(user):
    conn = sqlite3.connect(flask_settings.DB_NAME)
    cur = conn.cursor()
    current_app.logger.debug(f"Updating users {user['email']}")

    query = f"""UPDATE Users SET first_name = "{user['first_name']}", last_name = "{user['last_name']}", password = "{user['password']}" WHERE email = "{user['email']}";"""
    cur.execute(query)
    conn.commit()
    conn.close()


def setup_database():
    conn = sqlite3.connect(flask_settings.DB_NAME)
    cur = conn.cursor()

    create_user_table(cursor=cur)
    create_book_table(cursor=cur)
    create_list_table(cursor=cur)

    conn.commit()
    conn.close()


def create_user_table(cursor):
    query = """
    CREATE TABLE IF NOT EXISTS Users (
        email VARCHAR(75) PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        password VARCHAR(50));"""
    cursor.execute(query)


def create_book_table(cursor):
    query = """
    CREATE TABLE IF NOT EXISTS Books (
        isbn VARCHAR(13) PRIMARY KEY,
        title VARCHAR(50),
        author VARCHAR(50),
        pub_date DATE);"""
    cursor.execute(query)


def create_list_table(cursor):
    query = """
    CREATE TABLE IF NOT EXISTS Lists (
        user_email email VARCHAR(75),
        isbn VARCHAR(13),
        FOREIGN KEY(user_email) REFERENCES Users(email),
        FOREIGN KEY(isbn) REFERENCES Books(isbn),
        PRIMARY KEY(user_email, isbn)); """
    cursor.execute(query)


def clear_database():
    conn = sqlite3.connect(flask_settings.DB_NAME)
    cur = conn.cursor()
    cur.execute("""DROP TABLE IF EXISTS Users""")
    cur.execute("""DROP TABLE IF EXISTS Books""")
    cur.execute("""DROP TABLE IF EXISTS Lists""")
    conn.commit()
    conn.close()
