from flask import Flask
from .db import init_mongodb
from flask_login import LoginManager

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
client, db = init_mongodb(app.config["DB_NAME"], app.config["DB_PORT"])
app.secret_key = 'richard'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

#import views
from . import views
from . import forms
