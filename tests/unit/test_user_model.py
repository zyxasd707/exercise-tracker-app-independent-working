import unittest
from backend import create_app
from backend.models import db, User
from werkzeug.security import check_password_hash

class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_password_hashing(self):
        """测试密码哈希功能是否正常工作"""
        u = User(username='test', email='test@example.com')
        u.set_password('password123')
        self.assertTrue(check_password_hash(u.password_hash, 'password123'))
        self.assertFalse(check_password_hash(u.password_hash, 'wrongpassword'))