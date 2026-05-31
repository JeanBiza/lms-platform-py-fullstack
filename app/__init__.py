from flask import Flask
from app.extensions import db, migrate, login_manager
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # registrar blueprints (rutas) — los iremos agregando
    # from app.routes.auth import auth_bp
    # app.register_blueprint(auth_bp)

    return app