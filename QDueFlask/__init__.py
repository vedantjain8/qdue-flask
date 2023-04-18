from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os, pytz

# from QDueFlask.ngrokRun import run_with_ngrok

# ========================== LOGGING ====================
# import logging
# from flask import current_app
# current_app.logger.info('info level log')
# logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
# ========================== LOGGING ====================

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
app.config['TIMEZONE'] = customTZ

# run_with_ngrok(app)

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

app.app_context().push()
db.create_all()