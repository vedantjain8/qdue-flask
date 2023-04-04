from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from prometheus_flask_exporter import PrometheusMetrics

# from flaskblog.ngrokRun import run_with_ngrok

# ========================== LOGGING ====================
# import logging
# from flask import current_app
# current_app.logger.info('info level log')
# logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
# ========================== LOGGING ====================

app = Flask(__name__)
app.config["SECRET_KEY"] = "YOUR_SECRET_KEY_HERE"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# run_with_ngrok(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "users.login"
login_manager.login_message_category="info"
login_manager.session_protection = "strong"

# Register blueprints
from flaskblog.user.routes import users
from flaskblog.posts.routes import posts
from flaskblog.errors.handlers import errors
from flaskblog.api.routes import apis
from flaskblog.admin.routes import admin
from flaskblog.main.routes import main

app.register_blueprint(users, url_prefix='/QDueFlask')
app.register_blueprint(posts, url_prefix='/QDueFlask')
app.register_blueprint(errors, url_prefix='/QDueFlask')
app.register_blueprint(apis, url_prefix='/QDueFlask/api')
app.register_blueprint(admin, url_prefix='/QDueFlask/admin')
app.register_blueprint(main, url_prefix='/QDueFlask')

# # Configure Prometheus metrics
# metrics = PrometheusMetrics(app)
# metrics.info("app_info", "Prometheus export", version="1.0.0")