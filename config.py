import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

# Classe geral
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")

    APP_TITLE = "Flask REST API Course"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = ["headers"]

    @staticmethod
    def init_app(app):
        pass


# Configuração para Desenvolvimento
class DevelopmentConfig(Config):
    # Conexão com o SQLite
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")


# Configuração para Produção
class ProductionConfig(Config):
    # URL do Banco de Dados
    uri = os.getenv("DATABASE_URL")
  
    # Checagem se a URL existe e se começa com "postgres://"
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://")

    # Conexão com o PostegreSQL
    SQLALCHEMY_DATABASE_URI = uri