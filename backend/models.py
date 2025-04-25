# Import required libraries
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy for ORM database operations
from datetime import datetime  # For timestamp functionality
from werkzeug.security import generate_password_hash, check_password_hash  # For password security

# Initialize the SQLAlchemy instance
db = SQLAlchemy()

class User(db.Model):
    """
    User model representing application users.
    Stores user credentials and account information.
    """
    # Primary key for the user
    id = db.Column(db.Integer, primary_key=True)
    
    # Username field - must be unique and is required
    username = db.Column(db.String(80), unique=True, nullable=False)
    
    # Email field - must be unique and is required
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # Stores the hashed password (not the actual password)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # Timestamp when the user account was created
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        """
        Set the user's password by generating a hash.
        
        Args:
            password (str): The plain text password to be hashed
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Verify if the provided password matches the stored hash.
        
        Args:
            password (str): The plain text password to check
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)
