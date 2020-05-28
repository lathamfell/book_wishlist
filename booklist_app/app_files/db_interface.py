import sqlite3

from flask import current_app

import flask_settings
from app_files import encrypter
from app_files.exceptions import BookNotFoundInList


class DBInterface:
    def __init__(self):
        self.conn = sqlite3.connect(flask_settings.DB_NAME)
        self.cur = self.conn.cursor()

    def execute_query(self, query):
        if not self.conn:
            self.conn = sqlite3.connect(flask_settings.DB_NAME)
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()
        self.conn.close()
        self.conn = None

    def execute_query_with_fetchone(self, query):
        if not self.conn:
            self.conn = sqlite3.connect(flask_settings.DB_NAME)
        cur = self.conn.cursor()
        cur.execute(query)
        res = cur.fetchone()
        self.conn.commit()
        self.conn.close()
        self.conn = None
        return res

    def execute_query_with_fetchall(self, query):
        if not self.conn:
            self.conn = sqlite3.connect(flask_settings.DB_NAME)
        cur = self.conn.cursor()
        cur.execute(query)
        res = cur.fetchall()
        self.conn.commit()
        self.conn.close()
        self.conn = None
        return res

    def add_user(self, user):
        encrypted_pw = encrypter.get_encrypted(user["password"])
        query = f"""INSERT INTO Users (email, first_name, last_name, password) VALUES ("{user['email']}", "{user['first_name']}", "{user['last_name']}", "{encrypted_pw}");"""
        self.execute_query(query)

    def add_book(self, book):
        query = f"""INSERT INTO Books (isbn, title, author, pub_date) VALUES ("{book['isbn']}", "{book['title']}", "{book['author']}", "{book['pub_date']}");"""
        self.execute_query(query)

    def get_user(self, user_email):
        query = f"""SELECT email, first_name, last_name FROM Users WHERE email="{user_email}" """
        res = self.execute_query_with_fetchone(query)
        return res

    def get_book(self, isbn):
        query = (
            f"""SELECT isbn, title, author, pub_date FROM Books WHERE isbn="{isbn}" """
        )
        res = self.execute_query_with_fetchone(query)
        return res

    def get_list(self, email):
        query = f"""SELECT * FROM Lists WHERE user_email="{email}"; """
        res = self.execute_query_with_fetchall(query)
        return res

    def update_user(self, email, user_data_changes):
        current_user_data_query = f"""SELECT first_name, last_name, password FROM Users WHERE email="{email}" """
        current_user_data = self.execute_query_with_fetchone(
            query=current_user_data_query
        )
        new_user_data = {
            "first_name": current_user_data[0],
            "last_name": current_user_data[1],
            "password": current_user_data[2],
        }
        if "first_name" in user_data_changes:
            new_user_data["first_name"] = user_data_changes["first_name"]
        if "last_name" in user_data_changes:
            new_user_data["last_name"] = user_data_changes["last_name"]
        if "password" in user_data_changes:
            new_user_data["password"] = encrypter.get_encrypted(
                user_data_changes["password"]
            )

        query = f"""UPDATE Users SET first_name = "{new_user_data['first_name']}", last_name = "{new_user_data['last_name']}", password = "{new_user_data['password']}" WHERE email = "{email}";"""
        self.execute_query(query)

    def update_book(self, isbn, book_data_changes):
        current_book_data_query = (
            f"""SELECT title, author, pub_date FROM Books WHERE isbn="{isbn}" """
        )
        current_book_data = self.execute_query_with_fetchone(
            query=current_book_data_query
        )
        new_book_data = {
            "title": current_book_data[0],
            "author": current_book_data[1],
            "pub_date": current_book_data[2],
        }
        if "title" in book_data_changes:
            new_book_data["title"] = book_data_changes["title"]
        if "author" in book_data_changes:
            new_book_data["author"] = book_data_changes["author"]
        if "pub_date" in book_data_changes:
            new_book_data["pub_date"] = book_data_changes["pub_date"]

        query = f"""UPDATE Books SET title = "{new_book_data['title']}", author = "{new_book_data['author']}", pub_date = "{new_book_data['pub_date']}" """
        self.execute_query(query)

    def add_book_to_list(self, email, isbn):
        query = f"""INSERT OR IGNORE INTO Lists (user_email, isbn) VALUES ("{email}", "{isbn}"); """
        self.execute_query(query)

    def remove_book_from_list(self, email, isbn):
        count_query = f"""SELECT * FROM Lists WHERE user_email="{email}" AND isbn="{isbn}"; """
        res = self.execute_query_with_fetchone(count_query)
        if res:
            delete_query = f"""DELETE FROM Lists WHERE user_email="{email}" AND isbn="{isbn}"; """
            self.execute_query(delete_query)
        else:
            raise BookNotFoundInList

    def delete_user(self, email):
        delete_user_query = f"""DELETE FROM Users WHERE email="{email}"; """
        self.execute_query(delete_user_query)
        clean_wishlist_query = f"""DELETE FROM Lists WHERE user_email="{email}"; """
        self.execute_query(clean_wishlist_query)

    def delete_book(self, isbn):
        delete_book_query = f"""DELETE FROM Books WHERE isbn="{isbn}"; """
        self.execute_query(delete_book_query)
        clean_wishlist_query = f"""DELETE FROM Lists WHERE isbn="{isbn}"; """
        self.execute_query(clean_wishlist_query)

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
