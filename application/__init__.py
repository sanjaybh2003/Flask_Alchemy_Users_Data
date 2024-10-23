from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from .config import Config
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  

def create_app(app_config=None):
    app = Flask(__name__, instance_relative_config=False, static_folder='static')

    if app_config is not None:
        app.config.from_object(app_config)
    else:
        app.config.from_object(Config)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_default_secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///default.db') 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True

    print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from application.auth import auth as auth_blueprint  
    app.register_blueprint(auth_blueprint, url_prefix='/auth')  
    
    from application.routes import main as main_blueprint 
    app.register_blueprint(main_blueprint) 

    return app
