# -*- coding: utf-8 -*-
from flask import Blueprint, request

blueprint = Blueprint("public", __name__)


@blueprint.route("/", methods=["GET"])
@blueprint.route("/index", methods=["GET"])
def index():
    return {"status": "OK"}


@blueprint.route("/add")
def add():
    ret_val = AddRouteHandler(request=request).add()
    current_app.logger.debug(f"Returning to client: {ret_val}")
    return ret_val


@blueprint.route("/update")
def update():
    ret_val = UpdateRouteHandler(request=request).update()
    current_app.logger.debug(f"Returning to client: {ret_val}")
    return ret_val


@blueprint.route("/delete")
def delete():
    ret_val = DeleteRouteHandler(request=request).delete()
    current_app.logger.debug(f"Returning to client: {ret_val}")
    return ret_val
