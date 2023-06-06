from flask import Blueprint,render_template, abort, request, jsonify, url_for, redirect
from QDueFlask.models import User
from QDueFlask import db, customTZ
from flask_login import  login_required, current_user
from QDueFlask import app_logger
from datetime import timedelta, datetime

admin = Blueprint("admin", __name__, url_prefix="/admin")

@admin.route("/")
@login_required
def AdminfrontPage():
    app_logger.info('Request received: %s %s by UserID: %s', request.method, request.url, current_user.id)
    if User.query.filter_by(username = current_user.username).first().admin:
        return render_template("admin/startpage.html", users= User.query.all())
    else:
        abort(403)

@admin.route('/changeAdmin', methods=['POST'])
@login_required
def update_boolean():
    app_logger.info('Request received: %s %s by UserID: %s', request.method, request.url, current_user.id)
    if request.method == 'POST' and User.query.filter_by(username = current_user.username).first().admin:
        data = request.get_json()
        value = data['value']
        username = data['username']
        User.query.filter_by(username = username).first().admin= value
        db.session.commit()
        return jsonify({'success': True})
    else:
        abort(403)

@admin.route("/deleteUser", methods=['POST'])
@login_required
def deleteUser():
    app_logger.info('Request received: %s %s by UserID: %s', request.method, request.url, current_user.id)
    if request.method == "POST" and User.query.filter_by(username = current_user.username).first().admin:
        data = request.get_json()
        username = data['username']
        db.session.delete(User.query.filter_by(username = username).first())
        db.session.commit()
        return redirect(url_for("admin.AdminfrontPage"))
    else:
        abort(403)

@admin.route("/dashboard")
@login_required
def adminDashboard():
    app_logger.info('Request received: %s %s by UserID: %s', request.method, request.url, current_user.id)
    if User.query.filter_by(username = current_user.username).first().admin:
        current_time = datetime.now(customTZ)

        active_users = User.query.filter(User.last_activity > current_time - timedelta(minutes=1)).all()

        return render_template("admin/dashboard.html")
    else:
        abort(403)