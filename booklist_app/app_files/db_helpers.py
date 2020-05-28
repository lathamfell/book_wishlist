import sqlite3

from flask import current_app

from app_files.config import constants


def update_user(user):
    conn = sqlite3.connect(constants.DB_NAME)
    cur = conn.cursor()
    current_app.logger.debug(f"Updating users {user['email']}")

    query = f"""UPDATE Users SET first_name = "{user['first_name']}", last_name = "{user['last_name']}", password = "{user['password']}" WHERE email = "{user['email']}";"""
    cur.execute(query)
