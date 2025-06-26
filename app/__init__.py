import os
from flask import Flask

from .config import DevConfig, ProdConfig, TestConfig
from .extensions import db, migrate, login_manager

from .routes.auth.views import auth_bp
from .routes.anime.views import anime_bp
from .routes.public.views import public_bp

config_mapping = {
    'development': DevConfig,
    'production': ProdConfig,
    'testing': TestConfig
}

def create_app(config_name='development'):
    app = Flask(__name__, instance_relative_config=True)

    config_class = config_mapping.get(config_name, DevConfig)
    app.config.from_object(config_class)

    app.config.from_pyfile('config.py')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='')
    app.register_blueprint(anime_bp, url_prefix='')
    app.register_blueprint(public_bp, url_prefix='')

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app



