from flask import render_template, Blueprint, redirect, url_for

main = Blueprint("main", __name__)

@main.route('/')
def routeThepage():
    return redirect(url_for("posts.insert"))

@main.route('/about')
def about():
    return render_template("about.html")

@main.route('/docs')
def docs():
    return render_template("docs.html")