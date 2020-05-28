# -*- coding: utf-8 -*-
from flask import Blueprint, current_app, request

from app_files.route_handlers import (AddBookRouteHandler,
                                      AddBookToListRouteHandler,
                                      AddUserRouteHandler,
                                      DeleteBookRouteHandler,
                                      DeleteUserRouteHandler,
                                      GetBookRouteHandler, GetListRouteHandler,
                                      GetUserRouteHandler,
                                      RemoveBookFromListRouteHandler,
                                      UpdateBookRouteHandler,
                                      UpdateUserRouteHandler)

blueprint = Blueprint("public", __name__)


@blueprint.route("/", methods=["GET"])
@blueprint.route("/index", methods=["GET"])
def index():
    return {"status": "OK"}


@blueprint.route("/add_user", methods=["POST"])
def add_user():
    ret_val = AddUserRouteHandler(request=request).add_user()
    current_app.logger.debug(f"Returning to client: {ret_val}")
    return ret_val


@blueprint.route("/get_user", methods=["GET"])
def get_user():
    ret_val = GetUserRouteHandler(request=request).get_user()
    current_app.logger.debug(f"Returning to client: {ret_val}")
    return ret_val


@blueprint.route("/get_list", methods=["GET"])
def get_list():
    ret_val = GetListRouteHandler(request=request).get_list()
    current_app.logger.debug(f"Returning to client: {ret_val}")
    return ret_val


@blueprint.route("/update_user", methods=["POST"])
def update_user():
    ret_val = UpdateUserRouteHandler(request=request).update_user()
    current_app.logger.debug(f"Returning to client: {ret_val}")
    return ret_val


@blueprint.route("/delete_user", methods=["POST"])
def delete_user():
    ret_val = DeleteUserRouteHandler(request=request).delete_user()
    current_app.logger.debug(f"Returning to client: {ret_val}")
    return ret_val


@blueprint.route("/add_book", methods=["POST"])
def add_book():
    ret_val = AddBookRouteHandler(request=request).add_book()
    current_app.logger.debug(f"Returning to client: {ret_val}")
    return ret_val


@blueprint.route("/get_book", methods=["GET"])
def get_book():
    ret_val = GetBookRouteHandler(request=request).get_book()
    current_app.logger.debug(f"Returning to client: {ret_val}")
    return ret_val


@blueprint.route("/update_book", methods=["POST"])
def update_book():
    ret_val = UpdateBookRouteHandler(request=request).update_book()
    current_app.logger.debug(f"Returning to client: {ret_val}")
    return ret_val


@blueprint.route("/delete_book", methods=["POST"])
def delete_book():
    ret_val = DeleteBookRouteHandler(request=request).delete_book()
    current_app.logger.debug(f"Returning to client: {ret_val}")
    return ret_val


@blueprint.route("/add_book_to_list", methods=["POST"])
def add_book_to_list():
    ret_val = AddBookToListRouteHandler(request=request).add_book_to_list()
    current_app.logger.debug(f"Returning to client: {ret_val}")
    return ret_val


@blueprint.route("/remove_book_from_list", methods=["POST"])
def remove_book_from_list():
    ret_val = RemoveBookFromListRouteHandler(request=request).remove_book_from_list()
    current_app.logger.debug(f"Returning to client: {ret_val}")
    return ret_val
