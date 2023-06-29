import os

class Config:

    PG_HOST = os.environ.get('PG_HOST')
    PG_USER = os.environ.get('PG_USER')
    PG_PASSWORD = os.environ.get('PG_PASSWORD')
    PG_DATABASE = os.environ.get('PG_DATABASE')
    PG_PORT = os.environ.get('PG_PORT')
    API_KEY = os.environ.get('API_KEY')
    CACHE_TYPE = os.environ.get('CACHE_TYPE')
    CACHE_REDIS_HOST = os.environ.get('CACHE_REDIS_HOST')
    CACHE_REDIS_PORT = os.environ.get('CACHE_REDIS_PORT')
    CACHE_REDIS_DB = os.environ.get('CACHE_REDIS_DB')
    CACHE_REDIS_URL = os.environ.get('CACHE_REDIS_URL')
    CACHE_DEFAULT_TIMEOUT = os.environ.get('CACHE_DEFAULT_TIMEOUT')
    CACHE_REDIS_PASSWORD = os.environ.get('CACHE_REDIS_PASSWORD')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    Debug = True

class TestingConfig(Config):
    TESTING = True

config = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'default': DevelopmentConfig
        }
