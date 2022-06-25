# This bluepint contains APIs to talk to ServiceNow instance

from flask import Blueprint
from . import api

servicenow_blueprint = Blueprint("servicenow", __name__)
