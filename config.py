import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///../tests/database/voca.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    WORDS_PER_PAGE = 30
    SESSION_COOKIE_SECURE = True


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    TEMPLATES_AUTO_RELOAD = True
    DEVELOPMENT = True
    DEBUG = True
    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    DEBUG_TB_ENABLED = False
    WORDS_PER_PAGE = 5
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../tests/test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'null'
    WTF_CSRF_ENABLED = False
