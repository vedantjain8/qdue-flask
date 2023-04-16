from flask import render_template,request,redirect,flash, url_for, Blueprint, Response
from QDueFlask import app, db, bcrypt
from QDueFlask.models import User, Todo
from QDueFlask.user.forms import RegistrationForm, LoginForm, UpdateAccountForm, DeleteAllPostsForm
from flask_login import login_user, current_user, logout_user, login_required

users = Blueprint("users", __name__)

@users.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("posts.insert"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created! Ready to login", "success")
        return redirect(url_for("users.login")) #here home is def of home route
    return render_template("register.html", title ="Register", form= form)

@users.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("posts.insert"))
    form = LoginForm()
    if form.validate_on_submit():
        # if successful login then this
        with app.app_context():
            user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("posts.insert")) #here home is def of home route
        # else this
        else:
            flash(f"Log in Unsuccessfully! Please check your username and password", "danger")
    return render_template("login.html", title ="login", form= form)
 
@users.route("/logout")
def logout():
    logout_user()
    flash(f"Logout was Successfull.", "success")
    return redirect(url_for("posts.insert"))

@users.route("/account", methods=['GET','POST'])
@login_required
def account():
    user = User.query.filter_by(username=current_user.username).first()
    form= UpdateAccountForm()
    deletePostsr = DeleteAllPostsForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash("Update saved successfully!", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
    return render_template("account.html", title ="account", current_user= current_user, form=form, api_key=user.api, deletePostsr=deletePostsr)

@users.route("/account-deleteAllposts", methods=['GET','POST'])
@login_required
def account_deleteAllPosts():
    if request.method == "GET":
        return redirect(url_for("posts.insert"))
    while True:
        try:
            db.session.delete(Todo.query.filter_by(user_id=current_user.id).first())
        except:
            break
        finally:
            db.session.commit()
            flash("All posts were deleted!", "success")
    return Response(status=200)