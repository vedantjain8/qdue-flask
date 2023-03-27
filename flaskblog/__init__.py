from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from prometheus_flask_exporter import PrometheusMetrics
# import logging
# from flaskblog.ngrokRun import run_with_ngrok

# ========================== LOGGING ====================
# from flask import current_app
# current_app.logger.info('info level log')
# ========================== LOGGING ====================

# logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
 
app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.info("app_info", "Prometheus export", version="1.0.0")

# run_with_ngrok(app)

app.config["SECRET_KEY"] = "YOUR_SECRET_KEY_HERE"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "users.login"
login_manager.login_message_category="info"
login_manager.session_protection = "strong"

from flaskblog.user.routes import users
from flaskblog.posts.routes import posts
from flaskblog.main.routes import main
from flaskblog.errors.handlers import errors
from flaskblog.api.routes import apis
from flaskblog.admin.routes import admin

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
app.register_blueprint(errors)
app.register_blueprint(apis)
app.register_blueprint(admin)