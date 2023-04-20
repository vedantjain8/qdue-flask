from datetime import datetime
from QDueFlask import db, login_manager, customTZ
from flask_login import UserMixin
import uuid

def getCurrentTime():
    return datetime.now(customTZ).strftime('%d-%m-%Y %I:%M:%S %p')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(200), nullable = False)
    description = db.Column(db.String(500), nullable= False)
    date_created = db.Column(db.String(22), default= getCurrentTime)
    date_updated = db.Column(db.String(22), default= getCurrentTime)
    pinned = db.Column(db.Integer(),nullable= False, default= 0)
    backcolor = db.Column(db.String(),nullable= False, default= "#ffffff")
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable = False)

    def __repr__(self) -> str:
        return f"{self.title}><:SPLITFROMHERE:><{self.description}"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), nullable= False, unique=True)
    password = db.Column(db.String(60), nullable = False)
    todos = db.relationship("Todo", backref= "author", lazy=True)
    admin = db.Column(db.Boolean, nullable= False, default=False)
    api = db.Column(db.String(), nullable=False, default= str(uuid.uuid4()))


    def __repr__(self) -> str:
        return f"{self.username}"
