from flask import current_app, render_template

from . import main_blueprint


@main_blueprint.route("/")
def index():
    current_app.logger.info("Index page loading")
    return render_template("main/index.html")
