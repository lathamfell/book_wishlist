# -*- coding: utf-8 -*-
from flask import Blueprint, current_app, request

from app_files.route_handlers import (AddBookRouteHandler,
                                      AddBookToListRouteHandler,
                                      AddUserRouteHandler,
                                      DeleteBookRouteHandler,
                                      DeleteUserRouteHandler,
                                      GetListRouteHandler,
                                      RemoveBookRouteHandler,
                                      UpdateBookRouteHandler,
                                      UpdateUserRouteHandler)

blueprint = Blueprint("public", __name__)


@blueprint.route("/", methods=["GET"])
@blueprint.route("/index", methods=["GET"])
def index():
    return {"status": "OK"}


@blueprint.route("/add_user")
def add_user():
    ret_val = AddUserRouteHandler(request=request).add_user()
    current_app.logger.debug(f"Returning to client: {ret_val}")
    return ret_val


@blueprint.route("/get_list")
def get_list():
    ret_val = GetListRouteHandler(request=request).get_list()
    current_app.logger.debug(f"Returning to client: {ret_val}")
    return ret_val


@blueprint.route("/update_user")
def update_user():
    ret_val = UpdateUserRouteHandler(request=request).update_user()
    current_app.logger.debug(f"Returning to client: {ret_val}")
    return ret_val


@blueprint.route("/delete_user")
def delete_user():
    ret_val = DeleteUserRouteHandler(request=request).delete_user()
    current_app.logger.debug(f"Returning to client: {ret_val}")
    return ret_val


@blueprint.route("/add_book")
def add_book():
    ret_val = AddBookRouteHandler(request=request).add_book()
    current_app.logger.debug(f"Returning to client: {ret_val}")
    return ret_val


@blueprint.route("/delete_book")
def delete_book():
    ret_val = DeleteBookRouteHandler(request=request).delete_book()
    current_app.logger.debug(f"Returning to client: {ret_val}")
    return ret_val


@blueprint.route("/update_book")
def update_book():
    ret_val = UpdateBookRouteHandler(request=request).update_book()
    current_app.logger.debug(f"Returning to client: {ret_val}")
    return ret_val


@blueprint.route("/add_book_to_list")
def add_book_to_list():
    ret_val = AddBookToListRouteHandler(request=request).add_book_to_list()
    current_app.logger.debug(f"Returning to client: {ret_val}")
    return ret_val


@blueprint.route("/remove_book")
def remove_book():
    ret_val = RemoveBookRouteHandler(request=request).remove_book()
    current_app.logger.debug(f"Returning to client: {ret_val}")
    return ret_val
