from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    """Base configuration."""
    APP_NAME = "Flask_SQLAlchemy_Users_Data"
    SECRET_KEY = environ.get('SECRET_KEY', 'default_secret_key')    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI', 'mysql+pymysql://Sanjay:bhagi1234@localhost:3306/MyDatabase')

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_DEBUG = environ.get('FLASK_DEBUG', '1') in ['true', '1', 'yes']

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_TEST_DATABASE_URI', 'sqlite:///:memory:')

class ProductionConfig(Config):
    DEBUG = False
    FLASK_DEBUG = environ.get('FLASK_DEBUG', '0') in ['true', '1', 'yes']

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

app_config = config.get(environ.get('FLASK_ENV', 'default'))
