from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Import Migrate
from .models import db
import os

def create_app():
    app = Flask(
        __name__,
        template_folder='../frontend',  # Path to the frontend static files
        static_folder='../frontend',    # Path to the frontend templates
    )
    
    # Setting Database
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exercise_tracker.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Ensure the instance file exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Initialize the Database
    db.init_app(app)
    migrate = Migrate(app, db)  # Initialize Migrate
    
    
    return app

