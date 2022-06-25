from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config


app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)

# O nome da view function que o Flask-Login utiliza para, por exemplo,
# proteger páginas de serem acessadas por usuários anonônimos.
login.login_view = 'login'

from app import routes, models, errors