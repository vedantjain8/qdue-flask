from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flaskblog.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username not available')


class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=3, max=20)])
    submit = SubmitField('Update')

    def validate_username(self,username):
        if current_user.username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username not available')

        if current_user.username == username.data:
            raise ValidationError('Username can not be same as before')

class UpdateAccountPasswordForm(FlaskForm):
    CurrentPassword = StringField('Current Password', validators=[DataRequired()])
    NewPassword = StringField('New Password', validators=[DataRequired()])
    ConfirmPassword = StringField('Confirm Password', validators=[DataRequired()])
    PasswordSubmit = SubmitField('Update Password')

class DeleteAllPostsForm(FlaskForm):
    DeleteAllPosts = SubmitField('Delete all posts')