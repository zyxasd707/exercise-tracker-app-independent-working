from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from .models import User

class LoginForm(FlaskForm): # Defines a login form class, inheriting from FlaskForm.
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm): # Defines a registration form class
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=35)])
    phone = StringField('Phone', validators=[Length(max=15)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username): # Custom validation method for username
        user = User.query.filter_by(username=username.data).first() # Check if username already exists
        if user:
            raise ValidationError('Username already exists.')
            
    def validate_email(self, email): # Custom validation method for email
        user = User.query.filter_by(email=email.data).first() # Check if email already exists
        if user:
            raise ValidationError('Email already exists.')
            
    def validate_phone(self, phone): # Custom validation method for phone
        if phone.data: # Check if phone number is provided
            user = User.query.filter_by(phone=phone.data).first() # Check if phone number already exists
            if user:
                raise ValidationError('Phone number already exists.')