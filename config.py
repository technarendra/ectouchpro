import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DB_CONFIG = {
        'host': 'localhost',
        'port': '5432',
        'database': 'postgresdb',
        'user': 'postgres',
        'password': 'root',
    }

    # class Config(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s" % DB_CONFIG
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    CSRF_ENABLED = True

    CSRF_SESSION_KEY = "secret"

    SECRET_KEY = "secret"



class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True