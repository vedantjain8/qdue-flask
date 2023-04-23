import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os, pytz
from datetime import datetime

if os.environ.get("db_username") and os.environ.get("db_password") and os.environ.get("db_host") and os.environ.get("db_database"):
    username = os.environ.get("db_username")
    password = os.environ.get("db_password")
    host = os.environ.get("db_host", "127.0.0.1")
    port = os.environ.get("db_port", "5432")
    database = os.environ.get("db_database")

    dbPath = f"postgresql://{username}:{password}@{host}:{port}/{database}"
else: 
    dbPath= "sqlite:///todo.db"

if os.environ.get("TZ"):
    customTZ = pytz.timezone(os.environ.get("TZ"))
else:
    customTZ = pytz.timezone('UTC')

app = Flask(__name__,static_url_path='/QDueFlask', static_folder='static')
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "default_secret_key")
app.config['SQLALCHEMY_DATABASE_URI'] = dbPath
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# logginng
try:
    os.mkdir('log')
except Exception as e:
    print(e)
    
app_logger = logging.getLogger(__name__)
log_filename = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), r"log\app.log")
log_formatter = logging.Formatter(f"{datetime.now(customTZ).strftime('%d-%m-%Y %I:%M:%S %p')} %(levelname)s %(name)s %(threadName)s : %(message)s")
file_handler = RotatingFileHandler(log_filename, maxBytes=int(os.environ.get("logSize", 3221225472)) , backupCount=int(os.environ.get("logSize", 5)))
file_handler.setFormatter(log_formatter)
app_logger.addHandler(file_handler)
app_logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)
app_logger.addHandler(stream_handler)
# end logging

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "users.login"
login_manager.login_message_category="info"
login_manager.session_protection = "strong"

# Register blueprints
from QDueFlask.user.routes import users
from QDueFlask.posts.routes import posts
from QDueFlask.errors.handlers import errors
from QDueFlask.api.routes import apis
from QDueFlask.admin.routes import admin
from QDueFlask.main.routes import main

app.register_blueprint(users, url_prefix='/QDueFlask')
app.register_blueprint(posts, url_prefix='/QDueFlask')
app.register_blueprint(errors, url_prefix='/QDueFlask')
app.register_blueprint(apis, url_prefix='/QDueFlask/api')
app.register_blueprint(admin, url_prefix='/QDueFlask/admin')
app.register_blueprint(main, url_prefix='/QDueFlask')

users.logger = app_logger
posts.logger = app_logger
errors.logger = app_logger
apis.logger = app_logger
admin.logger = app_logger
main.logger = app_logger

app.app_context().push()
db.create_all()