from flask_api import status
from app_files.config import constants
import sqlite3
from app_files.db_interface import DBInterface


class AddUserRouteHandler:
    def __init__(self, request):
        self.request = request
        self.ret_val = None
        self.user = request.json

    def add_user(self):
        DBInterface().add_user(user=self.user)
        self.ret_val = ({"status": "User added"}, status.HTTP_200_OK)
        return self.ret_val


class AddBookRouteHandler:
    def __init__(self, request):
        self.request = request
        self.ret_val = None
        self.book = request.json

    def add_book(self):
        DBInterface().add_book(book=self.book)
        self.ret_val = ({"status": "Book added"}, status.HTTP_200_OK)
        return self.ret_val


class GetUserRouteHandler:
    def __init__(self, request):
        self.request = request
        self.ret_val = None
        self.user_email = request.args["email"]

    def get_user(self):
        user_data = DBInterface().get_user(user_email=self.user_email)
        if user_data:
            self.ret_val = ({"status": "User returned", "data": user_data}, status.HTTP_200_OK)
        else:
            self.ret_val = ({"status": "User not found"}, status.HTTP_404_NOT_FOUND)
        return self.ret_val


class GetBookRouteHandler:
    def __init__(self, request):
        self.request = request
        self.ret_val = None
        self.isbn = request.args["isbn"]

    def get_book(self):
        book_data = DBInterface().get_book(isbn=self.isbn)
        if book_data:
            self.ret_val = ({"status": "Book returned", "data": book_data}, status.HTTP_200_OK)
        else:
            self.ret_val = ({"status": "Book not found"}, status.HTTP_404_NOT_FOUND)
        return self.ret_val


class GetListRouteHandler:
    def __init__(self, request):
        self.request = request
        self.ret_val = None
        self.email = request.args["email"]

    def get_list(self):
        wishlist = DBInterface().get_list(email=self.email)
        self.ret_val = ({"status": "List returned", "data": wishlist}, status.HTTP_200_OK)
        return self.ret_val


class UpdateUserRouteHandler:
    def __init__(self, request):
        self.request = request
        self.ret_val = None

    def update_user(self):
        self.ret_val = ({"status": "User updated"}, status.HTTP_200_OK)
        return self.ret_val


class UpdateBookRouteHandler:
    def __init__(self, request):
        self.request = request
        self.ret_val = None

    def update_book(self):
        self.ret_val = ({"status": "Book updated"}, status.HTTP_200_OK)
        return self.ret_val


class AddBookToListRouteHandler:
    def __init__(self, request):
        self.request = request
        self.ret_val = None
        self.email = request.json["email"]
        self.isbn = request.json["isbn"]

    def add_book_to_list(self):
        DBInterface().add_book_to_list(email=self.email, isbn=self.isbn)
        self.ret_val = ({"status": "Book added to list"}, status.HTTP_200_OK)
        return self.ret_val


class RemoveBookFromListRouteHandler:
    def __init__(self, request):
        self.request = request
        self.ret_val = None
        self.email = request.json["email"]
        self.isbn = request.json["isbn"]

    def remove_book_from_list(self):
        DBInterface().remove_book_from_list(email=self.email, isbn=self.isbn)
        self.ret_val = ({"status": "Book removed from list"}, status.HTTP_200_OK)
        return self.ret_val


class DeleteUserRouteHandler:
    def __init__(self, request):
        self.request = request
        self.ret_val = None
        self.email = request.json["email"]

    def delete_user(self):
        DBInterface().delete_user(email=self.email)
        self.ret_val = ({"status": "User deleted"}, status.HTTP_200_OK)
        return self.ret_val


class DeleteBookRouteHandler:
    def __init__(self, request):
        self.request = request
        self.ret_val = None
        self.isbn = request.json["isbn"]

    def delete_book(self):
        DBInterface().delete_book(isbn=self.isbn)
        self.ret_val = ({"status": "Book deleted"}, status.HTTP_200_OK)
        return self.ret_val
