from flask import Blueprint,render_template, abort, request, jsonify, url_for, redirect
from QDueFlask.models import User
from QDueFlask import db
from flask_login import  login_required, current_user

admin = Blueprint("admin", __name__, url_prefix="/admin")

@admin.route("/")
@login_required
def AdminfrontPage():
    if User.query.filter_by(username = current_user.username).first().admin:
        return render_template("admin/startpage.html", users= User.query.all())
    else:
        abort(403)

@admin.route('/changeAdmin', methods=['POST'])
@login_required
def update_boolean():
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
    if request.method == "POST" and User.query.filter_by(username = current_user.username).first().admin:
        data = request.get_json()
        username = data['username']
        db.session.delete(User.query.filter_by(username = username).first())
        db.session.commit()
        return redirect(url_for("admin.AdminfrontPage"))
    else:
        abort(403)