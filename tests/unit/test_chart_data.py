import unittest
import json
from datetime import datetime, timedelta
from backend import create_app
from backend.models import db, User, ExerciseLog
from werkzeug.security import generate_password_hash

class TestChartData(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing purposes.
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
        
        # Add workout log data
        today = datetime.utcnow()
        for i in range(7):
            log = ExerciseLog(
                user_id=self.user.id,
                exercise_type='Running' if i % 2 == 0 else 'Cycling',
                duration=30 + i * 5,
                calories=300 + i * 50,
                date=today - timedelta(days=i)
            )
            db.session.add(log)
        db.session.commit()
        
        # Log in user
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_chart_data_endpoint(self):
        """Testing chart data API endpoints"""
        response = self.client.get('/charts')
        self.assertEqual(response.status_code, 200)
        
        # Parse JSON response.
        data = json.loads(response.data)
        
        # Validate data structures
        self.assertIn('bubble_data', data)
        self.assertTrue(isinstance(data['bubble_data'], list))
        self.assertGreaterEqual(len(data['bubble_data']), 7)  # Should have at least seven entries.
        
        # "Validate the format of the first data entry."
        first_item = data['bubble_data'][0]
        self.assertIn('x', first_item)
        self.assertIn('y', first_item)
        self.assertIn('r', first_item)