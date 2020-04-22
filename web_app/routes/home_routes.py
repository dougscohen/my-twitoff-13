# web_app/routes/home_routes.py

from flask import Blueprint, render_template

home_routes = Blueprint("home_routes", __name__)

# @home_routes.route("/")
# def index():
#     return "Hello Twitoff!"

@home_routes.route("/about")
def about():
    return "About me"

@home_routes.route("/poll")
def poll():
    return render_template("poll.html")