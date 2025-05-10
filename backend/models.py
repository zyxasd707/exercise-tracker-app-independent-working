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

    avatar_path = db.Column(db.String(255), nullable=True)
    full_name = db.Column(db.String(120), nullable=True)
    dob = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    height_cm = db.Column(db.Float, nullable=True)
    weight_kg = db.Column(db.Float, nullable=True)
    phone = db.Column(db.String(15), unique=True, nullable=True)  # Handle phone number as string to allow for the page of register

    # Stores the hashed password (not the actual password)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # Timestamp when the user account was created
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Timestamp for the last time the user logged in
    last_login = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    
    # Method to update the last login timestamp
    def update_last_login(self):
        """
        Update the last login timestamp to the current time.
        """
        self.last_login = datetime.utcnow()
        db.session.commit()

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
    
class ExerciseLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise_type = db.Column(db.String(50), nullable=False)  
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    calories = db.Column(db.Integer, nullable=False) 
    date = db.Column(db.DateTime, default=datetime.utcnow)  # Date of the exercise 


class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    achieved_at = db.Column(db.DateTime, default=datetime.utcnow)
