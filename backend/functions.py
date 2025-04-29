from flask import request, jsonify, render_template, session, redirect, url_for
from .models import db, User, ExerciseLog, Achievement
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

def init_dashboard():
    if request.method == 'GET':
        return render_template('dashboard.html')
    return render_template('login.html')

def init_profile():
    if request.method == 'GET':
        return render_template('profile.html')
    return render_template('login.html')

def init_sharing():
    if request.method == 'GET':
        return render_template('sharing.html')
    return render_template('login.html')


def handle_exercise_log():
    user_id = session['user_id']

    if request.method == 'POST':
        exercise_type = request.form['exercise_type']
        duration = int(request.form['duration'])
        calories = int(request.form['calories'])

        log = ExerciseLog(user_id=user_id, exercise_type=exercise_type, duration=duration, calories=calories)
        db.session.add(log)
        db.session.commit()

        # achievement for each type
        thresholds = range(500, 5001, 500)
        sum_type_duration = db.session.query(db.func.sum(ExerciseLog.duration))\
            .filter_by(user_id=user_id, exercise_type=exercise_type).scalar() or 0

        for threshold in thresholds:
            # check if the achievement already exists
            existing = Achievement.query.filter_by(
                user_id=user_id,
                exercise_type=exercise_type,
                description=f"Accumulate {threshold} minutes of {exercise_type}!"
            ).first()

            if sum_type_duration >= threshold and not existing:
                achievement = Achievement(
                    user_id=user_id,
                    exercise_type=exercise_type,
                    description=f"Accumulate {threshold} minutes of {exercise_type}!"
                )
                db.session.add(achievement)

        # achievement for all types
        # calculate the total duration for all exercise types
        # check if the achievement already exists
        sum_all_duration = db.session.query(db.func.sum(ExerciseLog.duration))\
            .filter_by(user_id=user_id).scalar() or 0

        for threshold in thresholds:
            existing_all = Achievement.query.filter_by(
                user_id=user_id,
                exercise_type='ALL',
                description=f"Accumulate {threshold} total minutes of all exercise types!"
            ).first()

            if sum_all_duration >= threshold and not existing_all:
                achievement = Achievement(
                    user_id=user_id,
                    exercise_type='ALL',
                    description=f"Accumulate {threshold} total minutes of all exercise types!"
                )
                db.session.add(achievement)

        db.session.commit()
        return redirect(url_for('exercise_log'))

    logs = ExerciseLog.query.filter_by(user_id=user_id).order_by(ExerciseLog.date.desc()).all()
    return render_template('exercise_log.html', logs=logs)



def handle_achievement():
        user_id = session['user_id']
        achievements = Achievement.query.filter_by(user_id=user_id)\
            .order_by(Achievement.achieved_at.desc()).all()
        return render_template('achievement.html', achievements=achievements)