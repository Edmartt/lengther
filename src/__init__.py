from flask import Flask
from config import config
from .locations.cache.cache_redis import cache


def create_app(config_name: str) -> Flask:
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)


    from .database import postgres

    postgres.init_app(app)
    cache.init_app(app)
    
    from src.locations import locations_routes as locations_blueprint

    app.register_blueprint(locations_blueprint)
    return app
