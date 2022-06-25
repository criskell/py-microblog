import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from logging.handlers import SMTPHandler, RotatingFileHandler

from config import Config


app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)

# O nome da view function que o Flask-Login utiliza para, por exemplo,
# proteger páginas de serem acessadas por usuários anonônimos.
login.login_view = 'login'

if not app.debug:
    if app.config['MAIL_SERVER']:
        credentials = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            credentials = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()

        mailhost = (app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
        
        handler = SMTPHandler(
            mailhost=mailhost,
            fromaddr=app.config['MAIL_FROM_ADDR'],
            toaddrs=app.config['ADMINS'],
            subject='[py-microblog] Erro',
            credentials=credentials,
            secure=secure
        )
        
        handler.setLevel(logging.ERROR)
        app.logger.addHandler(handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')

    handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info("Inicialização do aplicativo")

from app import routes, models, errors