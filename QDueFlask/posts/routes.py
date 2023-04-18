from flask import render_template,request,redirect, url_for,Blueprint, abort
from QDueFlask import db, customTZ
from QDueFlask.models import Todo
from flask_login import current_user, login_required

from datetime import datetime

posts = Blueprint("posts", __name__)

@posts.route('/', methods=['GET','POST'])
@login_required
def insert():
    if request.method == 'POST':
        title = str(request.form["title"]).strip()
        desc= str(request.form["desc"]).replace("  ", " ")
        username = current_user.id
        todo = Todo(title= title, description= desc, user_id =username)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for("posts.insert"))
    return render_template("insert.html", posts = Todo.query.filter_by(user_id=current_user.id).order_by(Todo.date_created).all())

@posts.route("/delete/<int:id>")
@login_required
def delete(id):
    if current_user.id == (Todo.query.filter_by(id=id).first()).user_id :
        db.session.delete(Todo.query.filter_by(id=id).first())
        db.session.commit()
        return redirect(url_for("posts.insert")) #here home is def of home route
    else:
        abort(403)

@posts.route("/update/<int:id>" , methods=['GET','POST'])
@login_required
def update(id):
    if current_user.id == (Todo.query.filter_by(id=id).first()).user_id :
        if request.method == "POST":
            todo = Todo.query.filter_by(id=id).first()
            todo.title = str(request.form["title"]).strip()
            todo.description = str(request.form["desc"]).replace("  ", " ")
            todo.date_updated = datetime.now(customTZ).strftime('%Y-%m-%d %I:%M:%S %p')
            db.session.add(todo)
            db.session.commit()
            return redirect(url_for("posts.insert")) #here home is def of home route
        return render_template("update.html", post = Todo.query.filter_by(id=id).first())
    else:
        abort(403)

@posts.route("/update-color/<int:id>", methods=["POST"])
@login_required
def changeColor(id):
    color = request.json['color']
    todo = Todo.query.filter_by(id=id).first()
    todo.backcolor = color
    db.session.add(todo)
    db.session.commit()
    return "success"

@posts.route("/pin/<int:id>" , methods=['GET','POST'])
@login_required
def pinned(id):
    if current_user.id == (Todo.query.filter_by(id=id).first()).user_id :
        todo = Todo.query.filter_by(id=id).first()
        if todo.pinned == 0:
            todo.pinned = 1
        else:
            todo.pinned = 0
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for("posts.insert")) #here home is def of home route
    else:
        abort(403)
    