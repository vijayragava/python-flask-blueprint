"""This contains the application factory for creating flask application
instances. Using the application factory allows for the creation of flask
applications configured for different environments based on the value of the
CONFIG_TYPE environment variable """

import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template
from flask.logging import default_handler


# Application Factory #
def create_app():

    app = Flask(__name__)

    # Configure the flask app instance
    config_type = os.getenv("CONFIG_TYPE", default="config.DevelopmentConfig")
    app.config.from_object(config_type)

    # Register blueprints
    register_blueprints(app)

    # Configure logging
    configure_logging(app)

    # Register error handlers
    register_error_handlers(app)

    return app


# Helper Functions #
def register_blueprints(app):
    from app.main import main_blueprint
    from app.servicenow import servicenow_blueprint

    app.register_blueprint(servicenow_blueprint, url_prefix="/api")
    app.register_blueprint(main_blueprint)


def register_error_handlers(app):

    # 400 - Bad Request
    @app.errorhandler(400)
    def bad_request(e):
        return render_template("400.html"), 400

    # 403 - Forbidden
    @app.errorhandler(403)
    def forbidden(e):
        return render_template("403.html"), 403

    # 404 - Page Not Found
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    # 405 - Method Not Allowed
    @app.errorhandler(405)
    def method_not_allowed(e):
        return render_template("405.html"), 405

    # 500 - Internal Server Error
    @app.errorhandler(500)
    def server_error(e):
        return render_template("500.html"), 500


def configure_logging(app):

    # Deactivate the default flask logger so that log messages don't get
    # duplicated
    app.logger.removeHandler(default_handler)

    # Create a file handler object
    file_handler = RotatingFileHandler(
        "logs/flaskapp.log", maxBytes=16384, backupCount=20
    )

    # Set the logging level of the file handler object so that it logs INFO
    # and up
    file_handler.setLevel(logging.INFO)

    # Create a file formatter object
    file_formatter = logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s [in %(filename)s: %(lineno)d]"
    )

    # Apply the file formatter object to the file handler object
    file_handler.setFormatter(file_formatter)

    # Add file handler object to the logger
    app.logger.addHandler(file_handler)
