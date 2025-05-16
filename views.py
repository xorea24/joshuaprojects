from flask import Blueprint, render_template

views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template("index.html",name = "Joe", age = "12")

@views.route("/profile/<username>")
def profile(username):
    return render_template("index.html", name=username)
