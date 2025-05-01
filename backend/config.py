import os

basedir = os.path.abspath(os.path.dirname(__file__))
instance_dir = os.path.abspath(os.path.join(basedir, '..', 'instance'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(instance_dir, 'exercise_tracker.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
