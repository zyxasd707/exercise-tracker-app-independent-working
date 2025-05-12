import unittest
from backend import create_app
from backend.models import db, User, ExerciseLog
from werkzeug.security import generate_password_hash
from flask_login import login_user
from datetime import datetime

class TestExerciseRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False  # 禁用CSRF以便测试
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create test user.
        self.user = User(
            username='testuser',
            email='test@example.com',
            password_hash=generate_password_hash('password123'),
            is_active=True
        )
        db.session.add(self.user)
        db.session.commit()
        
        # Log-in user
        with self.client.session_transaction() as session:
            session['user_id'] = self.user.id
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_add_exercise_log(self):
        """Testing the addition of exercise logs."""
        # log in first.
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
        # Add exercise log
        response = self.client.post('/exercise_log', data={
            'exercise_type': 'Running',
            'duration': 30,
            'calories': 300,
            'date': datetime.utcnow().strftime('%Y-%m-%d')
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        
        # Verification logs have been added to the database.
        log = ExerciseLog.query.filter_by(user_id=self.user.id).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.exercise_type, 'Running')
        self.assertEqual(log.duration, 30)
        self.assertEqual(log.calories, 300)