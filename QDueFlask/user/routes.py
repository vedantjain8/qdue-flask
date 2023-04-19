from flask import render_template,request,redirect,flash, url_for, Blueprint, Response
from QDueFlask import app, db, bcrypt
from QDueFlask.models import User, Todo
from QDueFlask.user.forms import RegistrationForm, LoginForm, UpdateAccountForm, DeleteAllPostsForm, UpdateAccountPasswordForm
from flask_login import login_user, current_user, logout_user, login_required
from wtforms.validators import ValidationError

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
    passwordForm = UpdateAccountPasswordForm()
    
    # username change validation
    if form.validate_on_submit() and form.username.data:
        if len(form.username.data) >=3 and len(form.username.data) <=20:
            current_user.username = form.username.data
            db.session.commit()
            flash("Update saved successfully!", "success")
            return redirect(url_for("users.account"))
        else:
            form.username.errors.append(ValidationError("Username should be more than 3 letters and less than 20 letters"))
    else:
        form.username.data = current_user.username

    # password change validation
    if passwordForm.validate_on_submit() and passwordForm.CurrentPassword.data:
        if passwordForm.CurrentPassword.data:
            if passwordForm.NewPassword.data and len(passwordForm.NewPassword.data) >=6:
                if passwordForm.ConfirmPassword.data and len(passwordForm.ConfirmPassword.data) >=6:
                    if bcrypt.check_password_hash(current_user.password, passwordForm.CurrentPassword.data):
                        if passwordForm.NewPassword.data == passwordForm.ConfirmPassword.data:
                            current_user.password = bcrypt.generate_password_hash(passwordForm.ConfirmPassword.data).decode("utf-8")
                            db.session.commit()
                            flash("Password Updated successfully!", "success")
                        else:
                            passwordForm.ConfirmPassword.errors.append(ValidationError("Password does not match"))    
                            passwordForm.NewPassword.errors.append(ValidationError("Password does not match"))
                    else:
                        passwordForm.CurrentPassword.errors.append(ValidationError("Old Password does not match"))
                else:
                    passwordForm.ConfirmPassword.errors.append(ValidationError("This field is required and should contain more than 6 characters and less than 20"))    
            else:
                passwordForm.NewPassword.errors.append(ValidationError("This field is required and should contain more than 6 characters and less than 20"))
        else:
            passwordForm.CurrentPassword.errors.append(ValidationError("This field is required"))

    return render_template("account.html", title ="account", current_user= current_user, form=form, passwordForm=passwordForm, api_key=user.api, deletePostsr=deletePostsr)

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