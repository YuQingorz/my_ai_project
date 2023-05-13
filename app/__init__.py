from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, static_folder="../static", template_folder="templates")
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    return app
    
from app import models
