from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from .config import DevelopmentConfig


app = Flask(__name__)
app.secret_key = 'zzz -- 3r 4 gggg4 jjj fw0fj'
app.config.from_object(DevelopmentConfig)

sqldb = SQLAlchemy(app)

login_manager = LoginManager(app)
