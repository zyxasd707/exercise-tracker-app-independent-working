import unittest
from datetime import datetime
from backend import create_app
from backend.models import db, User, ExerciseLog

class TestExerciseLog(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create test users
        self.user = User(username='testuser', email='test@example.com')
        self.user.set_password('password123')
        db.session.add(self.user)
        db.session.commit()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_create_exercise_log(self):
        """Testing the creation of workout log entries"""
        log = ExerciseLog(
            user_id=self.user.id,
            exercise_type='Running',
            duration=30,
            calories=300,
            date=datetime.utcnow()
        )
        db.session.add(log)
        db.session.commit()
        
        # Verification record created:
        saved_log = ExerciseLog.query.filter_by(user_id=self.user.id).first()
        self.assertIsNotNone(saved_log)
        self.assertEqual(saved_log.exercise_type, 'Running')
        self.assertEqual(saved_log.duration, 30)
        self.assertEqual(saved_log.calories, 300)