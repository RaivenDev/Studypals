from flask import Flask
# Importamos a classe Migrate
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Importamos a classe SpecTree
from spectree import SecurityScheme, SpecTree

# Importamos a classe JWTManager
from flask_jwt_extended import JWTManager


from config import Config

db = SQLAlchemy()

# Criamos uma instância da classe Migrate
migrate = Migrate()

# Criamos uma instância da classe importada
jwt = JWTManager()

# Criamos uma instância da classe, dizendo que é uma aplicação Flask
api = SpecTree(
    "flask",
    title="Study Pals API",
    version="v.1.0",
    path="docs",
    security_schemes=[
        SecurityScheme(
            name="api_key",
            data={"type": "apiKey", "name": "Authorization", "in": "header"},
        )
    ],
    security={"api_key": []},
)

def create_app(ConfigClass):
    app = Flask(__name__)

    app.config.from_object(ConfigClass)
    
    # Inicializamos com as configurações da aplicação
    jwt.init_app(app)

    db.init_app(app)

    # Importamos os modelos criados
    from models import User, Post
    # Inicializamos o Flask-Migrate com nossa aplicação
    migrate.init_app(app, db)

    @jwt.user_lookup_loader
    def user_load(header, data):
        current_user = User.query.filter_by(username=data["sub"]).first()

        return current_user
    
    # Controllers
    from controllers import user_controller
    app.register_blueprint(user_controller)
    from controllers import auth_controller
    app.register_blueprint(auth_controller)
    from controllers import posts_controller
    app.register_blueprint(posts_controller)

    
    # Registramos nossa aplicação na api (apos todos os registros de blueprints)
    api.register(app)

    return app