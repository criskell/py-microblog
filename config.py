import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'COLOQUE-UMA-CHAVE-SUPERSECRETA-AQUI')