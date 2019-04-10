from flask import Flask
from .db import init_mongodb

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
client, db = init_mongodb(app.config["DB_NAME"], app.config["DB_PORT"])

#import views
from . import views
