import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from app import app

def register_mail_logger():
    if not app.config['MAIL_SERVER']:
        return

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

def register_file_logger():
    if not os.path.exists('logs'):
        os.mkdir('logs')

    handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)

    app.logger.addHandler(handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info("Inicialização do aplicativo")

if not app.debug:
    register_file_logger()
    register_mail_logger()