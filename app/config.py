import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'chave_secreta_segura')
    # Se DATABASE_URL estiver vazia ou não definida, utiliza o SQLite padrão
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///procuracao.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
