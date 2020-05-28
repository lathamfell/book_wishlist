from flask_api import status
from app_files.config import constants
import sqlite3
from app_files import db_helpers


class AddUserRouteHandler:
    def __init__(self, request):
        self.request = request
        self.ret_val = None
        self.user = request.json

    def add_user(self):
        db_helpers.add_user(user=self.user)
        self.ret_val = ({"status": "User added"}, status.HTTP_200_OK)
        return self.ret_val


class GetUserRouteHandler:
    def __init__(self, request):
        self.request = request
        self.ret_val = None
        self.user_email = request.args["email"]

    def get_user(self):
        user_data = db_helpers.get_user(user_email=self.user_email)
        self.ret_val = ({"status": "User returned", "data": user_data}, status.HTTP_200_OK)
        return self.ret_val


class GetListRouteHandler:
    def __init__(self, request):
        self.request = request
        self.ret_val = None

    def get_list(self):
        self.ret_val = ({"status": "List returned"}, status.HTTP_200_OK)
        return self.ret_val


class UpdateUserRouteHandler:
    def __init__(self, request):
        self.request = request
        self.ret_val = None

    def update_user(self):
        self.ret_val = ({"status": "User updated"}, status.HTTP_200_OK)
        return self.ret_val


class DeleteUserRouteHandler:
    def __init__(self, request):
        self.request = request
        self.ret_val = None

    def delete_user(self):
        self.ret_val = ({"status": "User deleted"}, status.HTTP_200_OK)
        return self.ret_val


class AddBookRouteHandler:
    def __init__(self, request):
        self.request = request
        self.ret_val = None

    def add_book(self):
        self.ret_val = ({"status": "Book added"}, status.HTTP_200_OK)
        return self.ret_val


class GetBookRouteHandler:
    def __init__(self, request):
        self.request = request
        self.ret_val = None

    def get_book(self):
        self.ret_val = ({"status": "Book returned"}, status.HTTP_200_OK)
        return self.ret_val


class UpdateBookRouteHandler:
    def __init__(self, request):
        self.request = request
        self.ret_val = None

    def update_book(self):
        self.ret_val = ({"status": "Book updated"}, status.HTTP_200_OK)
        return self.ret_val


class DeleteBookRouteHandler:
    def __init__(self, request):
        self.request = request
        self.ret_val = None

    def delete_book(self):
        self.ret_val = ({"status": "Book deleted"}, status.HTTP_200_OK)
        return self.ret_val


class AddBookToListRouteHandler:
    def __init__(self, request):
        self.request = request
        self.ret_val = None

    def add_book_to_list(self):
        self.ret_val = ({"status": "Book added to list"}, status.HTTP_200_OK)
        return self.ret_val


class RemoveBookFromListRouteHandler:
    def __init__(self, request):
        self.request = request
        self.ret_val = None

    def remove_book_from_list(self):
        self.ret_val = ({"status": "Book removed from list"}, status.HTTP_200_OK)
        return self.ret_val
