# -*- coding: utf-8 -*-
import logging
import sqlite3

from flask import Flask, jsonify

from app_files.config import constants
from booklist_app import public


def create_app(config_object="booklist_app.flask_settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    configure_logger(app)
    setup_database()
    return app


def register_extensions(app):
    return None


def register_blueprints(app):
    app.register_blueprint(public.views.blueprint)


def register_errorhandlers(app):
    return None


def configure_logger(app):
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


def setup_database():
    conn = sqlite3.connect(constants.DB_NAME)
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
