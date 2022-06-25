from flask import render_template

from . import servicenow_blueprint


@servicenow_blueprint.route("/register")
def register(email):
    message_data = {
        "subject": "Hello from the flask app!",
        "body": "This email was sent asynchronously using Celery.",
        "recipients": email,
    }
    return render_template("auth/register.html", email=email)
