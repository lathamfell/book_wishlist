import sqlite3

from flask import current_app

from app_files.config import constants
import flask_settings
from cryptography.fernet import Fernet


class DBInterface:
    def __init__(self):
        self.conn = sqlite3.connect(flask_settings.DB_NAME)
        self.cur = self.conn.cursor()

    def execute_query(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()
        self.conn.close()

    def execute_query_with_fetchone(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        res = cur.fetchone()
        self.conn.commit()
        self.conn.close()
        return res

    def execute_query_with_fetchall(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        res = cur.fetchall()
        self.conn.commit()
        self.conn.close()
        return res

    def add_user(self, user):
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        encrypted_pw = cipher_suite.encrypt(bytes(user["password"], "utf-8"))

        query = f"""INSERT INTO Users (email, first_name, last_name, password) VALUES ("{user['email']}", "{user['first_name']}", "{user['last_name']}", "{encrypted_pw}");"""
        self.execute_query(query)

    def get_user(self, user_email):
        query = f"""SELECT email, first_name, last_name FROM Users WHERE email="{user_email}" """
        res = self.execute_query_with_fetchone(query)
        return res

    def update_user(self, user):
        query = f"""UPDATE Users SET first_name = "{user['first_name']}", last_name = "{user['last_name']}", password = "{user['password']}" WHERE email = "{user['email']}";"""
        self.execute_query(query)

    def add_book(self, book):
        query = f"""INSERT INTO Books (isbn, title, author, pub_date) VALUES ("{book['isbn']}", "{book['title']}", "{book['author']}", "{book['pub_date']}");"""
        self.execute_query(query)

    def get_book(self, isbn):
        query = f"""SELECT isbn, title, author, pub_date FROM Books WHERE isbn="{isbn}" """
        res = self.execute_query_with_fetchone(query)
        return res

    def get_list(self, email):
        query = f"""SELECT * FROM Lists WHERE user_email="{email}"; """
        res = self.execute_query_with_fetchall(query)
        return res

    def add_book_to_list(self, email, isbn):
        query = f"""INSERT OR IGNORE INTO Lists (user_email, isbn) VALUES ("{email}", "{isbn}"); """
        self.execute_query(query)

    @staticmethod
    def setup_database():
        conn = sqlite3.connect(flask_settings.DB_NAME)
        cur = conn.cursor()

        DBInterface.create_user_table(cursor=cur)
        DBInterface.create_book_table(cursor=cur)
        DBInterface.create_list_table(cursor=cur)

        conn.commit()
        conn.close()

    @staticmethod
    def create_user_table(cursor):
        query = """
        CREATE TABLE IF NOT EXISTS Users (
            email VARCHAR(75) PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            password VARCHAR(50));"""
        cursor.execute(query)

    @staticmethod
    def create_book_table(cursor):
        query = """
        CREATE TABLE IF NOT EXISTS Books (
            isbn VARCHAR(13) PRIMARY KEY,
            title VARCHAR(50),
            author VARCHAR(50),
            pub_date DATE);"""
        cursor.execute(query)

    @staticmethod
    def create_list_table(cursor):
        query = """
        CREATE TABLE IF NOT EXISTS Lists (
            user_email email VARCHAR(75),
            isbn VARCHAR(13),
            FOREIGN KEY(user_email) REFERENCES Users(email),
            FOREIGN KEY(isbn) REFERENCES Books(isbn),
            PRIMARY KEY(user_email, isbn)); """
        cursor.execute(query)

    @staticmethod
    def clear_database():
        conn = sqlite3.connect(flask_settings.DB_NAME)
        cur = conn.cursor()
        cur.execute("""DROP TABLE IF EXISTS Users""")
        cur.execute("""DROP TABLE IF EXISTS Books""")
        cur.execute("""DROP TABLE IF EXISTS Lists""")
        conn.commit()
        conn.close()
