from flask import request, jsonify, render_template, session, redirect, url_for
from .models import db, User
from functools import wraps

def handle_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return jsonify(success=True)
        
        # For backward compatibility, check admin hardcoded credentials
        admin = is_admin(username, password)
        if admin:
            return jsonify(success=True, is_admin=True)
            
        return jsonify(success=False)
    
    return render_template('login.html')

def handle_register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if username or email already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            # Determine which field is duplicate
            if existing_user.username == username:
                return jsonify(success=False, message="Username already exists")
            else:
                return jsonify(success=False, message="Email already exists")
        
        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify(success=True)
        except Exception as e:
            db.session.rollback()
            return jsonify(success=False, message="Registration failed: " + str(e))
    
    return render_template('register.html')

# This function checks if the user is an admin.
def is_admin(username, password):
    return username == "admin" and password == "admin"

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function