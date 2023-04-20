from flask import render_template, Blueprint, request
from QDueFlask import app_logger

main = Blueprint("main", __name__)

@main.route('/about')
def about():
    app_logger.info('Request received: %s %s', request.method, request.url)
    return render_template("about.html")

@main.route('/docs')
def docs():
    app_logger.info('Request received: %s %s', request.method, request.url)
    return render_template("docs.html")