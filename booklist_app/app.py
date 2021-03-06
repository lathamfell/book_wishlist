# -*- coding: utf-8 -*-
import logging

from flask import Flask

from booklist_app import public
from app_files.db_interface import DBInterface


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
    DBInterface.setup_database()
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
