from flask_api import status


class AddUserRouteHandler:
    def __init__(self, request):
        self.request = request
        self.ret_val = None

    def add_user(self):
        self.ret_val = ({"status": "User added"}, status.HTTP_200_OK)
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


class DeleteBookRouteHandler:
    def __init__(self, request):
        self.request = request
        self.ret_val = None

    def delete_book(self):
        self.ret_val = ({"status": "Book deleted"}, status.HTTP_200_OK)
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
