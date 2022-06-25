from flask import Blueprint
from . import api

main_blueprint = Blueprint("main", __name__, template_folder="templates")
